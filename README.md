# mcp-demo
create a weather mcp server and client. This project is based on PyCharm + pipenv.

mcp server: weather_server.py

client: client.py


## 1, add your OPENAI_API_KEY in .env file

## 2, run: python client.py

### the sample output: 
session initialized

[12/01/25 10:17:27] INFO     Processing request of type ListToolsRequest                                                                                                                     server.py:534
Loaded MCP tools: ['get_weather']

Agent ready.

User: What is the weather in New York?

Agent is thinking...

[12/01/25 10:17:29] INFO     Processing request of type CallToolRequest                                                                                                                      server.py:534

[12/01/25 10:17:30] INFO     HTTP Request: GET https://geocoding-api.open-meteo.com/v1/search?name=New+York&count=1&language=en&format=json "HTTP/1.1 200 OK"                              _client.py:1740

[12/01/25 10:17:32] INFO     HTTP Request: GET https://api.open-meteo.com/v1/forecast?latitude=40.71427&longitude=-74.00597&current_weather=true "HTTP/1.1 200 OK"                         _client.py:1740

Final Answer: The current weather in New York is 4.8°C with a wind speed of 13.7 km/h.

