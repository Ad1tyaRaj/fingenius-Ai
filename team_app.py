from phi.agent import Agent
# from phi.model.openai import OpenAIChat
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

web_agent = Agent(
    name="Web Agent",
    model=Groq(id="deepseek-r1-distill-llama-70b"),
    # model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    show_tool_calls=True,
    markdown=True
)

finance_agent = Agent(
    name="Finance Agent",
    role="Get financial data",
    model=Groq(id="deepseek-r1-distill-llama-70b"),
    # model=OpenAIChat(id="gpt-4o"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True)],
    instructions=["Use tables to display data"],
    show_tool_calls=True,
    markdown=True,
)

agent_team = Agent(
    model=Groq(id="deepseek-r1-distill-llama-70b"),
    team=[web_agent, finance_agent],
    instructions=["Always include sources",
        "Use tables to display data",
        "give suggestions for the best investment",
        "Focus on the most recent and relevant information",
        "Limit your search to 3-4 key topics",
        "Format your response in a table with:",
        "1. Topic",
        "2. Latest Update",
        "3. Source",
        "Use markdown table syntax with | for columns",
        "Include a brief summary at the top"  ],
    show_tool_calls=True,
    markdown=True,
)
