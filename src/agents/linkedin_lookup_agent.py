from dotenv import load_dotenv

from src.tools.tools import get_profile_url_tavily

load_dotenv()

from langchain_ollama import ChatOllama
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
from langchain import hub


def lookup(name: str) -> str:
    llm = ChatOllama(
        temperature=0,
        model="llama3.2:latest",
    )
    template = (
        "Given the full name {name_of_person}, return ONLY the LinkedIn profile page URL for this person. "
        "Do not include any explanation, markdown, or extra text. If you find the URL, output it and STOP."
    )

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )
    tools_for_agent = [
        Tool(
            name="linkedin_profile_page",
            func=get_profile_url_tavily,
            description="useful for when you need get the Linkedin Page URL",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools_for_agent,
        verbose=True,
        return_intermediate_steps=False,  # Prevent repeated tool calls
    )

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)},
        handle_parsing_errors=True,  # Add this argument
    )

    linked_profile_url = result["output"]
    return linked_profile_url


if __name__ == "__main__":
    print(lookup(name="Pankaj Jaiswal Fiserv Noida"))
