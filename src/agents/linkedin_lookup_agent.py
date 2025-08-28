from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableLambda

from src.prompts.prompt import REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS
from src.schema.schemas import AgentResponse
from src.tools.tools import get_tools

load_dotenv()

from langchain_ollama import ChatOllama
from langchain.prompts.prompt import PromptTemplate
from langchain.agents import AgentExecutor
from langchain.agents.react.agent import create_react_agent


def lookup() -> str:
    llm = ChatOllama(
        temperature=0, model="llama3.2:latest", base_url="http://localhost:11434"
    )
    output_parser = PydanticOutputParser(pydantic_object=AgentResponse)

    react_prompt_with_format_instructions = PromptTemplate(
        template=REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS,
        input_variables=["input", "agent_scratchpad", "tool_names"],
    ).partial(format_instructions=output_parser.get_format_instructions())

    agent = create_react_agent(
        llm=llm, tools=get_tools(), prompt=react_prompt_with_format_instructions
    )
    agent_executor = AgentExecutor(agent=agent, tools=get_tools(), verbose=True)
    extract_output = RunnableLambda(lambda x: x["output"])
    parse_output = RunnableLambda(lambda x: output_parser.parse(x))

    chain = agent_executor | extract_output | parse_output

    result = chain.invoke(
        input={
            "input": "search for 3 job postings for an ai engineer using langchain in the Noida, India on linkedin and list their details",
        }
    )

    print(result)
    return result


if __name__ == "__main__":
    lookup()
