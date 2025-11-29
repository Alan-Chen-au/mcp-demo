import asyncio
import os

# 1. Load environment variables
# This will read OPENAI_API_KEY from your .env file

from dotenv import load_dotenv

load_dotenv()

# Requirements: langchain>=0.3, langchain-openai, mcp
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools


async def main():
    # 1. Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found. Please create a .env file with OPENAI_API_KEY=sk-...")
        return

    # 2. MCP Server (local)
    server_params = StdioServerParameters(
        command="python",
        args=["/Users/alanchen/PycharmProjects/mcp-demo/weather_server.py"],
    )

    print("Connecting to MCP Server...")

    # 3. Create connection
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            # Initialize MCP session
            await session.initialize()
            print("session initialized")

            # 4. Auto-load MCP tools (this replaces manual tool wrapper)
            tools = await load_mcp_tools(session)
            print(f"Loaded MCP tools: {[t.name for t in tools]}")

            # 5. Setup LLM (gpt-4o-mini as requested)
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

            # 6. Create the LangChain Agent with the loaded tools
            agent = create_react_agent(llm, tools)
            print("Agent ready.")

            # 7. Ask the question
            query = "What is the weather in New York?"
            print(f"\nUser: {query}")
            print("Agent is thinking...")

            result = await agent.ainvoke({"messages": [("user", query)]})

            # 8. Final answer
            print(f"\nFinal Answer: {result['messages'][-1].content}")

if __name__ == "__main__":
    # Python 3.12+ recommended
    asyncio.run(main())
