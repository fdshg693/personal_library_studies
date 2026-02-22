from smolagents.default_tools import (
    VisitWebpageTool,
    DuckDuckGoSearchTool
)

arguments = {"url": "https://huggingface.co/"}
result = VisitWebpageTool()(arguments)
print (type(result))
print("Hugging Face – The AI community building the future" in result)
print(result)

result = DuckDuckGoSearchTool(timeout=20)("DeepSeek parent company")
print (type(result))
print(result)