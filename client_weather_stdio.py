import asyncio
import os
import sys

# 1. Load environment variables
# This will read OPENAI_API_KEY from your .env file
from dotenv import load_dotenv

load_dotenv()

# Requirements: langchain>=0.3, langchain-openai, mcp
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    # Check if API key is loaded
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found. Please create a .env file containing OPENAI_API_KEY=sk-...")
        return

    # 2. Configuration for the local MCP server
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["/Users/alanchen/PycharmProjects/mcp-demo/servers/weather_server.py"],
    )

    print("Connecting to MCP Server...")

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()

            # List available tools from the server
            tools_list = await session.list_tools()
            print(f"Connected! Found tools: {[t.name for t in tools_list.tools]}")

            # 3. Bridge MCP to LangChain
            # We wrap the dynamic MCP tool call in a LangChain @tool
            # NOTE: For production, you might want to dynamically generate Pydantic models
            # from the MCP tool schema. For this demo, we manually wrap the known tool.

            @tool
            async def get_weather(city: str) -> str:
                """Get the weather for a specific city name."""
                # Call the tool on the MCP server
                # MCP results are a list of content blocks (Text or Image)
                result = await session.call_tool("get_weather", arguments={"city": city})
                return result.content[0].text

            # 4. Create the LangChain Agent
            # User requested gpt-4o-mini
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

            tools = [get_weather]
            agent = create_react_agent(llm, tools)

            # 5. Run the Agent
            query = "What is the weather in Chicago?"
            print(f"\nUser: {query}")
            print("Agent is thinking... (calling gpt-4o-mini)")

            # 'ainvoke' returns a dictionary with 'messages'
            response = await agent.ainvoke({"messages": [("user", query)]})

            # The last message is the AI's final answer
            print(f"\nFinal Answer: {response['messages'][-1].content}")


if __name__ == "__main__":
    # Python 3.12+ recommended
    asyncio.run(main())
