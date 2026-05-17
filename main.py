
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

load_dotenv()


def main():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    tools = [TavilySearch(max_results=3)]

    agent = create_agent(model=llm, tools=tools)

    result = agent.invoke(
        {"messages": [HumanMessage(content="What is the latest news about LangChain?")]}
    )
    print("\nFinal answer:", result["messages"][-1].content)


if __name__ == "__main__":
    main()
