import json
from utils import Config
from enum import Enum
from llm import LLM
from utils import Memory
from logger import logger
from tools import ToolCollection, PythonExecute, Terminate, AskHuman, WriteFile 

config = Config()

MANUS_SYSTEM_PROMPT = (
"You are OpenManus, an all-capable AI assistant, aimed at solving any task presented by the user. You have various tools at your disposal that you can call upon to efficiently complete complex requests. Whether it's programming, information retrieval, file processing, web browsing, or human interaction (only for extreme cases), you can handle it all."
"The initial directory is: {directory}"
)

MANUS_NEXT_STEP_PROMPT = """
Based on user needs, proactively select the most appropriate tool or combination of tools. For complex tasks, you can break down the problem and use different tools step by step to solve it. After using each tool, clearly explain the execution results and suggest the next steps.

If you want to stop the interaction at any point, use the `terminate` tool/function call.
"""

class AgentState(str, Enum):
    # 空闲
    IDLE = "IDLE"
    FINISHED = "FINISHED"
    ERROR = "ERROR"


class Manus:
    def __init__(self):
        self.name = "Manus"
        self.system_prompt = MANUS_SYSTEM_PROMPT.format(directory=config.workspace_workspace_dir)
        self.next_step_prompt = MANUS_NEXT_STEP_PROMPT
        self.state = AgentState.IDLE
        self.current_step = 0
        self.max_steps = 10
        self.llm = LLM()
        self.memory = Memory()
        self.memory.add_message(role="system",
                                content=self.system_prompt) 
        self.available_tools = ToolCollection(
           PythonExecute(),
           WriteFile(),
           AskHuman(),
           Terminate()
        )
        self.tool_choices = "auto"
    
    @property
    def messages(self):
        return self.memory.messages 
    
    async def run(self, user_request):
        results = []
        if not user_request:
            return
        self.memory.add_message(role="user", content=user_request)
        while(self.current_step < self.max_steps and
              self.state != AgentState.FINISHED):
            self.current_step += 1
            logger.info(f"Executing step {self.current_step}/{self.max_steps}")
            step_result = await self.step()
            results.append(f"Step {self.current_step}: {step_result}")
            
            if self.current_step >= self.max_steps:
                self.current_step = 0
                self.state = AgentState.IDLE
                results.append(f"Terminated: Reached max steps ({self.max_steps})")
            
        return "\n".join(results) if results else "No steps executed"
            
    
    async def step(self):
        should_act = await self.think()
        if not should_act:
            return "Thinking complete - no action needed"
        return await self.act()
    
    async def think(self):
        self.memory.add_message(role="user",
                                content=self.next_step_prompt)

        response = await self.llm.chat_client.chat.completions.create(
            model=config.model_name,
            messages=self.messages,
            tools=self.available_tools.to_params(),
            tool_choice=self.tool_choices
        )
        
        if not response.choices or not response.choices[0].message:
            print(response)
            return None
        
        response = response.choices[0].message
        
        self.tool_calls = (
            response.tool_calls if response and response.tool_calls else []
        )
        content = response.content if response and response.content else ""

        logger.info(f"✨ {self.name}'s thoughts: {content}")
        logger.info(
            f"🛠️ {self.name} selected {len(self.tool_calls) if self.tool_calls else 0} tools to use"
        )
        if self.tool_calls:
            logger.info(
                f"🧰 Tools being prepared: {[call.function.name for call in self.tool_calls]}"
            )
            logger.info(f"🔧 Tool arguments: {self.tool_calls[0].function.arguments}")
        if self.tool_calls:
            formatted_calls = [
                {"id": call.id, "function": call.function.model_dump(), "type": "function"}
            for call in self.tool_calls]
            message = {"role": "assistant",
                       "content": content,
                       "tool_calls": formatted_calls}
            self.memory.add_message(**message)
        else:
            message = {"role": "assistant", "content": content}
            self.memory.add_message(**message)
            
        if self.tool_choices == "auto" and not self.tool_calls:
                return bool(content)

        return bool(self.tool_calls)    
                
        
    async def act(self):
        if not self.tool_calls:
            return "No content or commands to execute"
        
        results = []
        for command in self.tool_calls:
            result = await self.execute_tool(command)

            logger.info(
                f"🎯 Tool '{command.function.name}' completed its mission! Result: {result}"
            )
            tool_msg = {"role": "tool", "content":result, "tool_call_id": command.id, "name":command.function.name}
            
            self.memory.add_message(**tool_msg)
            results.append(result)

        return "\n\n".join(results)
    
    async def execute_tool(self, command) -> str:
        name = command.function.name
        try:
            args = json.loads(command.function.arguments or "{}")

            logger.info(f"🔧 Activating tool: '{name}'...")
            result = await self.available_tools.execute(name=name, tool_input=args)

            observation = (
                f"Observed output of cmd `{name}` executed:\n{str(result)}"
                if result
                else f"Cmd `{name}` completed with no output"
            )
            
            if name.lower() == "terminate" and result:
                self.state = AgentState.FINISHED

            return observation
        except json.JSONDecodeError:
            error_msg = f"Error parsing arguments for {name}: Invalid JSON format"
            logger.error(
                f"📝 Oops! The arguments for '{name}' don't make sense - invalid JSON, arguments:{command.function.arguments}"
            )
            return f"Error: {error_msg}"
        except Exception as e:
            error_msg = f"⚠️ Tool '{name}' encountered a problem: {str(e)}"
            logger.exception(error_msg)
            return f"Error: {error_msg}"