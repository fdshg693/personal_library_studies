from smolagents.default_tools import (
    PythonInterpreterTool,
)

py_tool = PythonInterpreterTool(authorized_imports=["numpy"])

result = py_tool("(2 / 2) * 4")
print(result)