from pprint import pprint

from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

# from langchain.chat_models import init_chat_model
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent


from third_parties.linkedin import scrape_linkedin_profile


def ice_break_with(name: str) -> str:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_username, mock=True
    )

    summary_template = """
    given the Linkedin information {information} about a person I want you to create:
    1. A short summary
    2. two interesting facts about them
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    model = ChatOllama(
        model="gemma3:1b",
        temperature=0.7,
        base_url="http://localhost:11434",
        validate_model_on_init=True,
    )
    # model = init_chat_model(
    #     "gemma3:1b",
    #     model_provider="ollama",
    #     base_url="http://localhost:11434", temperature=0.7
    # )

    chain = summary_prompt_template | model | StrOutputParser()

    res = chain.invoke(input={"information": linkedin_data})

    pprint(res)


if __name__ == "__main__":
    load_dotenv()

    print("Ice Breaker Enter")
    ice_break_with(name="Pankaj Jaiswal Fiserv Noida")
    print("Ice Breaker Exit")
