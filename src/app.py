from pprint import pprint

from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

load_dotenv()


def crack_joke(topic: str) -> str:
    summary_template = """
        give me joke of the day about {information}!!!
    """
    joke_prompt = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    model = ChatOllama(
        model="gemma3:1b", temperature=0.7, base_url="http://localhost:11434"
    )

    chain = joke_prompt | model | StrOutputParser()
    res = chain.invoke(input={"information": topic})

    pprint(res)


if __name__ == "__main__":

    crack_joke(topic="Software Engineer")
