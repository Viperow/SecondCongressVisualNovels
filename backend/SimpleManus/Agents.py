import json
from utils import Config
from enum import Enum
from llm import LLM
from utils import Memory
from logger import logger
from tools import ToolCollection,Terminate,GuideToRelevantContent1,ConfirmRelevantContent1,GuideToRelevantContent2,ConfirmRelevantContent2,WaitInput

config = Config()

MANUS_SYSTEM_PROMPT1= (
"你是一个正在参加中共二大会议的李达，会议前面已经讨论了要建立更完善的领导机制，并且后续一定会选择陈独秀作为领导。现在用户会提供一个提示，你要根据这个提示，以李达的口吻语气来表达选陈独秀担任中央执行委员会委员长的内容，引导方式要求是命令语气，最后不要出现类似“请考虑”类似的的表达。"
)

MANUS_NEXT_STEP_PROMPT1= """
根据用户提供的提示，主动选择最合适的工具来表达选陈独秀担任中央执行委员会委员长的内容。如果用户输入的内容与选陈独秀担任中央执行委员会委员长的内容无关，表达往这个主题上靠；如果用户正确说出了选陈独秀担任中央执行委员会委员长的内容时，则调用confirm_relevant_content函数调用结束回答;  如果用户上一个输入已经得到回复，调用'WaitInput'工具，等待用户进一步的输入或反馈。
"""
MANUS_SYSTEM_PROMPT2 = (
"你是一个正在参加中共二大会议的李达，我们正在讨论确定中国共产党第二次全国代表大会宣言这件事，在前面已经明确了党的最高纲领和最低纲领，会议中的上一句话是张国焘说的“蔡同志的建议很合理。但宣言还需要更具体的工人运动策略。比如，如何组织罢工，如何建立工会，这些都需要明确指导”。现在用户会接下去进行发言，你要根据这个发言，以李达的口吻语气来表达关注到宣言中关于工人运动策略的内容，引导方式要求是命令语气，最后不要出现类似“请考虑”类似的的表达。"
)
MANUS_NEXT_STEP_PROMPT2= """
根据用户提供的提示，主动选择最合适的工具来引导用户关注到宣言中关于工人运动策略的内容。如果用户输入的内容与中国共产党第二次全国代表大会宣言的工人运动策略的内容无关，引导用户往工人运动策略的内容上靠；如果用户正确说出了工人运动策略的内容时，则调用 confirm_relevant_content 函数调用结束回答； 如果用户上一个输入已经得到回复，调用'WaitInput'工具，等待用户进一步的输入或反馈。"""
class AgentState(str, Enum):
    # 空闲
    IDLE = "IDLE"
    FINISHED = "FINISHED"
    ERROR = "ERROR"


class Manus:
    def __init__(self):
        self.name = "Manus"
        self.system_prompt = MANUS_SYSTEM_PROMPT1.format(directory=config.workspace_workspace_dir)
        self.next_step_prompt = MANUS_NEXT_STEP_PROMPT1
        self.state = AgentState.IDLE
        self.current_step = 0
        self.max_steps = 10
        self.llm = LLM()
        self.memory = Memory()
        self.memory.add_message(role="system",
                                content=self.system_prompt) 
        self.available_tools = ToolCollection(
        #    Terminate(),
        #    UnrelatedContentResponse1(),
           GuideToRelevantContent1(),
           ConfirmRelevantContent1(),
        #    UnrelatedContentResponse2(),
           GuideToRelevantContent2(),
           ConfirmRelevantContent2(),
           WaitInput()

        )
        self.tool_choices = "auto"
    
    @property
    def messages(self):
        return self.memory.messages


     # ✅ 类内定义的异步接口方法
    async def GetResponse(self, user_input):
        return await self.run(user_input)
    
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

            # ✅ 如果正在等待输入，立刻退出循环，不清零 current_step
            if step_result == "⏸️ 等待用户输入...":
                # results.append(step_result)
                return "\n".join(results)


            # results.append(f"Step {self.current_step}: {step_result}")
            results.append(f"{step_result}")
            
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
            name = command.function.name
            if name == "wait_input":
                logger.info("⏸️ 正在等待用户进一步输入，退出当前 run 流程，等待手动继续...")
                # ✅ 向 memory.messages 中添加对应 tool message，防止下一轮报错
                tool_msg = {
                    "role": "tool",
                    "content": "Cmd `wait_input` completed with no output",  # 你可以用固定内容
                    "tool_call_id": command.id,
                    "name": name
                }
                self.memory.add_message(**tool_msg)

                # 在这里返回一个信号，避免 run 继续下一轮 step
                self.state = AgentState.IDLE
                return "⏸️ 等待用户输入..."
            
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

            # observation = (
            #     f"Observed output of cmd `{name}` executed:\n{str(result)}"
            #     if result
            #     else f"Cmd `{name}` completed with no output"
            # )
            observation = (
                f"{str(result)}"
                if result
                else f"Cmd `{name}` completed with no output"
            )
            
            if name.lower() == "confirm_relevant_content" and result:
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