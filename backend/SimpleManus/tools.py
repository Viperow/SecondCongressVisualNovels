import os
import multiprocessing
import sys
from io import StringIO

class ToolCollection:
    """A collection of defined tools."""

    def __init__(self, *tools):
        self.tools = tools
        self.tool_map = {tool.name: tool for tool in tools}

    def __iter__(self):
        return iter(self.tools)

    def to_params(self):
        return [tool.to_param() for tool in self.tools]

    async def execute(
        self, *, name: str, tool_input = None
    ):
        tool = self.tool_map.get(name)
        
        result = await tool(**tool_input)
        return result
    
    def get_tool(self, name: str):
        return self.tool_map.get(name)

class BaseTool:
    def to_param(self):
    
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }    
    
    async def __call__(self, **kwargs):
        """Execute the tool with given parameters."""
        return await self.execute(**kwargs)

class Terminate(BaseTool):
    name: str = "terminate"
    description: str = """Terminate the interaction when the request is met OR if the assistant cannot proceed further with the task.
When you have finished all the tasks, call this tool to end the work."""
    parameters: dict = {
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "description": "The finish status of the interaction.",
                "enum": ["success", "failure"],
            }
        },
        "required": ["status"],
    }

    async def execute(self, status: str) -> str:
        """Finish the current execution"""
        return f"The interaction has been completed with status: {status}"
    
class WaitInput(BaseTool):
    name: str = "wait_input"
    description: str = """如果用户上一个输入已经得到回复，调用'等待用户输入'工具，等待用户进一步的输入或反馈"""
    parameters: dict = {
    }

    async def execute(self) -> str:
        """Finish the current execution"""
        return ""

# class UnrelatedContentResponse1(BaseTool):
#     name: str = "unrelated_content_response"
#     description: str = """当用户输入与中共二大会议的内容无关时，表达往中共二大会议的内容上靠。"""
#     parameters: dict = {
#         "type": "object",
#         "properties": {
#             "response": {
#                 "type": "string",
#                 "description": "当用户输入的内容与中共二大会议的内容无关时，表达往中共二大会议的内容上靠的回应",
#             }
#         },
#         "required": ["response"],
#     }

#     async def execute(self, response: str) -> str:
#         return response
#     # "我听不懂你在说什么，请说和会议相关的内容"


class GuideToRelevantContent1(BaseTool):
    name: str = "guide_to_relevant_content"
    description: str = """当用户输入与选陈独秀担任中央执行委员会委员长的内容无关时，用命令语气来表达往选陈独秀担任中央执行委员会委员长的内容上靠。"""
    parameters: dict = {
        "type": "object",
        "properties": {
            "response": {
                "type": "string",
                "description": "当用户输入与选陈独秀担任中央执行委员会委员长的内容无关时，用命令语气来表达往选陈独秀担任中央执行委员会委员长的内容上靠的回应。",
            }
        },
        "required": ["response"],
    }

    async def execute(self, response: str) -> str:
        return response
    # "你提到的内容与党的相关事务有关，但与我们当前讨论的选陈独秀担任中央执行委员会委员长的内容不太相关。请你围绕这个主题发表看法。"


class ConfirmRelevantContent1(BaseTool):
    name: str = "confirm_relevant_content"
    description: str = """当用户正确说出选陈独秀担任中央执行委员会委员长的内容 或者 助手无法继续进行任务时，结束回答。"""
    parameters: dict = {
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "description": "互动的完成状态。",
                "enum": ["success", "failure"],
            }
        },
        "required": ["status"],
    }

    async def execute(self, status: str) -> str:
        return f"互动已经完成，状态为：{status}"


# class UnrelatedContentResponse2(BaseTool):
#     name: str = "unrelated_content_response"
#     description: str = """当用户输入与确定中国共产党第二次全国代表大会宣言无关时，来引导用户往确定中国共产党第二次全国代表大会宣言上靠。"""
#     parameters: dict = {
#         "type": "object",
#         "properties": {
#             "response": {
#                 "type": "string",
#                 "description": "当用户输入的内容与中共二大会议的内容无关时，manus给出的用于引导用户往确定中国共产党第二次全国代表大会宣言的内容上靠的回应",
#             }
#         },
#         "required": ["response"],
#     }

#     async def execute(self, response: str) -> str:
#         return response
#     # "我听不懂你在说什么，请说和会议相关的内容"


class GuideToRelevantContent2(BaseTool):
    name: str = "guide_to_relevant_content"
    description: str = """当与中国共产党第二次全国代表大会宣言的工人运动策略无关时，来引导用户往工人运动策略上靠。"""
    parameters: dict = {
        "type": "object",
        "properties": {
            "response": {
                "type": "string",
                "description": "当用户输入与中国共产党第二次全国代表大会宣言的工人运动策略无关时，manus给出的用于引导用户往工人运动策略的内容上靠的回应。",
            }
        },
        "required": ["response"],
    }

    async def execute(self, response: str) -> str:
        return response
    # "你提到的内容与中共二大会议的内容有关，但与我们当前讨论的工人运动策略不太相关。请围绕工人运动策略发表看法。"


class ConfirmRelevantContent2(BaseTool):
    name: str = "confirm_relevant_content"
    description: str = """当用户正确说出工人运动策略的内容 或者 助手无法继续进行任务时，结束回答。"""
    parameters: dict = {
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "description": "互动的完成状态。",
                "enum": ["success", "failure"],
            }
        },
        "required": ["status"],
    }

    async def execute(self, status: str) -> str:
        return f"互动已经完成，状态为：{status}"


class WriteFile(BaseTool):
    name: str = "writefile"
    description: str = """A tool for writing content to a specified file."""
    parameters: dict = {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "The file name.",
            },
            "content":{
                "type": "string",
                "description": "Content to be written to the file"
                }
        },
        "required": ["path", "content"],
    }

    async def execute(self, path, content) -> str:
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
        except:
            pass
        with open(path, 'w', encoding='utf8') as f:
            f.write(content)
            
class AskHuman(BaseTool):
    """Add a tool to ask human for help."""

    name: str = "ask_human"
    description: str = "Use this tool to ask human for help."
    parameters: str = {
        "type": "object",
        "properties": {
            "inquire": {
                "type": "string",
                "description": "The question you want to ask human.",
            }
        },
        "required": ["inquire"],
    }

    async def execute(self, inquire: str) -> str:
        return input(f"""Bot: {inquire}\n\nYou: """).strip()
    
class PythonExecute(BaseTool):
    """A tool for executing Python code with timeout and safety restrictions."""

    name: str = "python_execute"
    description: str = "Executes Python code string. Note: Only print outputs are visible, function return values are not captured. Use print statements to see results."
    parameters: dict = {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "The Python code to execute.",
            },
        },
        "required": ["code"],
    }

    def _run_code(self, code: str, result_dict: dict, safe_globals: dict) -> None:
        original_stdout = sys.stdout
        try:
            output_buffer = StringIO()
            sys.stdout = output_buffer
            exec(code, safe_globals, safe_globals)
            result_dict["observation"] = output_buffer.getvalue()
            result_dict["success"] = True
        except Exception as e:
            result_dict["observation"] = str(e)
            result_dict["success"] = False
        finally:
            sys.stdout = original_stdout

    async def execute(
        self,
        code: str,
        timeout: int = 5,
    ):
        """
        Executes the provided Python code with a timeout.

        Args:
            code (str): The Python code to execute.
            timeout (int): Execution timeout in seconds.

        Returns:
            Dict: Contains 'output' with execution output or error message and 'success' status.
        """

        with multiprocessing.Manager() as manager:
            result = manager.dict({"observation": "", "success": False})
            if isinstance(__builtins__, dict):
                safe_globals = {"__builtins__": __builtins__}
            else:
                safe_globals = {"__builtins__": __builtins__.__dict__.copy()}
            proc = multiprocessing.Process(
                target=self._run_code, args=(code, result, safe_globals)
            )
            proc.start()
            proc.join(timeout)

            # timeout process
            if proc.is_alive():
                proc.terminate()
                proc.join(1)
                return {
                    "observation": f"Execution timeout after {timeout} seconds",
                    "success": False,
                }
            return dict(result)
    