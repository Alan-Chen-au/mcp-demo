# mcp-demo
how to create mcp and use it.

1, add your OPENAI_API_KEY in .env file

2, update the args in StdioServerParameters, which points to weather_server.py location. 
    server_params = StdioServerParameters(
        command="python",
        args=["/Users/alanchen/PycharmProjects/mcp-demo/servers/weather_server.py"],
    )

3, run the 
