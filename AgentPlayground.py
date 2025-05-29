import requests
from dotenv import load_dotenv
from langchain.tools import BaseTool
from typing import Union
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
load_dotenv()

desc = (
    "A weather tool optimized for comprehensive up to date weather information. Useful for when you need to answer questions about the weather, use this tool to answer questions about the weather for a specific location. To use the tool, you must provide at the following parameters" 
    "['latitude', 'longitude']."
)
@tool
class AgentPlayground():
   """Weather reporter"""
     description = desc

    def _run(
            self,
            latitude: Union[int, float],
            longitude: Union[int, float]) -> None:
        url = "https://api.open-meteo.com/v1/forecast"
        # Parameters for the API request
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": "true"  # Get current weather; adjust parameters as needed
        }

        # Make the GET request to Open-Meteo
        response = requests.get(url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract and print the current weather details
            current_weather = data.get("current_weather")
            temperature = current_weather.get("temperature")
            current_rain = current_weather.get("current_rain")
            result_string = f"Current Temperature: {temperature}°C, Rain: {current_rain}"
            return result_string
        else:
            print("Failed to retrieve weather data")
            return "no weather data"

    def _arun(self, query: str):
        raise NotImplementedError("This tool does not support async")


llm = ChatOpenAI(model_name="gpt-4", temperature=0.7, verbose=True)

tools = [AgentPlayground()]

prompt = prompt = hub.pull("hwchase17/structured-chat-agent")

agent = create_structured_chat_agent(llm,tools,prompt)

executor = AgentExecutor(agent=agent, tools=tools,handle_parsing_errors=True)

output = executor.invoke({"input":"whats the weather like in waddesdon"})

print(output)

output = executor.invoke({"input":"whats the latest information about the kings cancer diagnosis"})

print(output)



