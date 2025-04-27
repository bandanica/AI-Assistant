from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from tools.weather_tools import WeatherTools

def create_what_to_wear_agent():
    llm = ChatOpenAI(openai_api_base="http://localhost:11434/v1", openai_api_key="ollama", model="llama3.2")

    tools = [WeatherTools.get_weather_info]

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )

    return agent
