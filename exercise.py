from dotenv import load_dotenv

load_dotenv()

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

@tool
def search(query: str) -> str:
    """
    Tool that searches the web for the given query and returns the results.
    Args:
        query: The search query.
    Returns:
        A string containing the search results.
    """
    # In a real implementation, this would call an external search API.
    print(f"Search results for '{query}'")
    return "Tokyo is the capital of Japan. It is known for its modern architecture, vibrant culture, and delicious food."

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = [search]
agent = create_agent(model=llm,tools=tools)


def main():
    print("What is the capital of Japan?")
    result = agent.invoke({"messages": [HumanMessage(content="What is the capital of Japan?")]})
    print(result)

if __name__ == "__main__":
    main()
