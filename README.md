# mcp-demo
how to create mcp and use it.

1, add your OPENAI_API_KEY in .env file

2, Update the args in StdioServerParameters; so it points to the correct location of weather_server.py. 
    server_params = StdioServerParameters(
        command="python",
        args=["/Users/alanchen/PycharmProjects/mcp-demo/weather_server.py"],
    )

3, run: python client.py
