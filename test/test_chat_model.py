from langchain_core.output_parsers import PydanticToolsParser
from langchain_ollama import ChatOllama


def test_init_with_valid_params():
    model = ChatOllama(
        model="gemma3:1b",
        temperature=0.7,
        base_url="http://localhost:11434",
        validate_model_on_init=True,
    )
    assert model is not None


def test_init_with_calculator_and_system_date_tools():
    llm = ChatOllama(
        model="gemma3:1b",
        temperature=0.7,
        base_url="http://localhost:11434",
        validate_model_on_init=True,
    )

    tools = [
        {
            "title": "add",
            "description": "Add two integers",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "integer", "description": "First integer"},
                    "b": {"type": "integer", "description": "Second integer"},
                },
                "required": ["a", "b"],
            },
        },
        {
            "title": "multiply",
            "description": "Multiply two integers",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "integer", "description": "First integer"},
                    "b": {"type": "integer", "description": "Second integer"},
                },
                "required": ["a", "b"],
            },
        },
    ]

    llm_with_tools = llm.bind_tools(tools)

    # response = llm_with_tools.invoke("What is 2 + 2?").tool_calls
    # print(response)
