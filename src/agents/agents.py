from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.tools.tools import web_search, scrape_url
from dotenv import load_dotenv

load_dotenv()

# Model inizialization
llm = ChatOpenAI(model = "gpt-4o-mini", temperature=0, max_tokens=2000)

# 1st agent : Search Agent
def build_search_agent():
    """
    Build a search agent that can perform web searches and scrape URLs.
    """
    return create_agent(
        model = llm,
        tools = [web_search],
    )

# 2nd agent : Reader Agent
def build_reader_agent():
    """
    Build a reader agent that can read and summarize content from URLs.
    """
    return create_agent(
        model = llm,
        tools = [scrape_url],
    )

#writer chain
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "you are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """ Write a detailed research repot on the topic below.

    Topic: {topic}
    Research gathered: {research}
    Structrure the report as:
    - Introduction
    - Key Findings (minimum 3 well explained points)
    - Conclusion
    - sources (list all the URLs found in the research)

    Be detailed, factual and professional."""),])

writer_chain = writer_prompt | llm | StrOutputParser()

#Critic_chain

critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "you are a sharp and constructive research critic. Be honest and specific in your feedback."),
    ("human", """ Review the research report and evaluate it strictly.

    Report: {report}

    Respond in this exact format:

    Score: X/10

    Strengths:
    - ...
    - ...

    Areas for Improvement:
    - ... 
    - ...

    One line veredict: ..."""),])

critic_chain = critic_prompt | llm | StrOutputParser()