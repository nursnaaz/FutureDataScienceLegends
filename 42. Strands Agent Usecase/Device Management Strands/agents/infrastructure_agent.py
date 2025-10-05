from strands import Agent, tool
import sqlite3
import pandas as pd
import os

from strands import Agent
from strands.models.ollama import OllamaModel

def get_db_connection(db_path='data/dubai_infrastructure.db'):
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found at {db_path}")
    conn = sqlite3.connect(db_path)
    return conn

@tool
def query_infrastructure_by_district(district_name: str='all', risk_level: str='all') -> str:
    """
    Query infrastructure details by district name and risk level.
    """
    conn = get_db_connection()

    query = f"SELECT asset_name, asset_type, district, risk_level, daily_usage, maintenance_cost_aed,  construction_year, next_inspection_due, condition_score FROM infrastructure_assets WHERE district LIKE '%{district_name}%' "
    if risk_level != 'all':
        query += f" AND risk_level = '{risk_level}'"

    query += " ORDER BY condition_score ASC LIMIT 10;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df.to_string(index=False)

@tool
def get_critical_alerts(risk_level: str='critical') -> str:
    """
    Get critical alerts from the infrastructure assets.
    """
    conn = get_db_connection()
    query = f"SELECT * FROM alerts JOIN infrastructure_assets ON alerts.asset_id = infrastructure_assets.asset_id WHERE alerts.severity in ('high', 'critical') AND alerts.status = 'active' "
    if risk_level != 'all':
        query += f" AND infrastructure_assets.risk_level = '{risk_level}'"
    print(query)
    df = pd.read_sql(query, conn)
    conn.close()
    return df.to_string(index=False)

@tool
def get_infrastructure_stats_by_risk() -> str:
    """
    Get infrastructure statistics grouped by risk level.
    """
    conn = get_db_connection()
    query = """
        SELECT risk_level, 
               COUNT(*) AS total_assets, 
               AVG(condition_score) AS avg_condition_score, 
               SUM(maintenance_cost_aed) AS total_maintenance_cost 
        FROM infrastructure_assets 
        GROUP BY risk_level
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df.to_string(index=False)

@tool
def get_infrastructure_stats_by_district() -> str:
    """
    Get infrastructure statistics grouped by district.
    """
    conn = get_db_connection()
    query = """
        SELECT district, 
               COUNT(*) AS total_assets, 
               AVG(condition_score) AS avg_condition_score, 
               SUM(maintenance_cost_aed) AS total_maintenance_cost 
        FROM infrastructure_assets 
        GROUP BY district
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df.to_string(index=False)

@tool
def fallback_tool(query: str) -> str:
    """
    Handles generic or out-of-scope questions.
    """
    return (
        "I'm here to help with infrastructure data queries. "
        "For other questions, please clarify or ask about infrastructure, alerts, or statistics."
    )

ollama_model = OllamaModel(
    host="http://localhost:11434",  # Ollama server address
    #model_id="MFDoom/deepseek-r1-tool-calling:1.5b",
    model_id="llama3.1:8b",
    think = False,
    reasoning = False
                                # Specil to use
)
agent = Agent(model=ollama_model, 
              system_prompt="""
You are an expert Dubai infrastructure management assistant. You have access to the following tools to answer user queries about infrastructure assets, their conditions, and related alerts:

query_infrastructure_by_district(district_name, risk_level): Retrieve infrastructure details filtered by district and risk level.
get_critical_alerts(risk_level): List recent critical or high-severity alerts for assets with a given risk level.
get_infrastructure_stats_by_risk(): Show summary statistics (count, average condition, total maintenance cost) grouped by risk level.
get_infrastructure_stats_by_district(): Show summary statistics grouped by district.

Your goals:
- Always use the most relevant tool to answer the user's question about infrastructure.
- If a query is ambiguous, ask clarifying questions (e.g., “Which district are you interested in?” or “Do you want to filter by risk level?”).
- If a tool returns no results, suggest alternative queries or broader filters (e.g., try 'all' for risk level or district).
- If a user asks for information not directly available, combine tool outputs or explain what is possible.
- For follow-up questions, use context from previous queries to provide seamless, intelligent assistance.
- If a database or tool error occurs, apologize and suggest the user check data availability or try again.
- Always be concise, accurate, and proactive in helping users explore Dubai’s infrastructure data.

IMPORTANT: If the user's question is not related to infrastructure or the available tools, respond conversationally and do NOT use any tool. For example, if the user asks "What is my name?" or "How are you?", reply as a helpful assistant would, without calling any function.
""",        
              
              tools=[query_infrastructure_by_district, 
                     get_critical_alerts, 
                     get_infrastructure_stats_by_risk, 
                     get_infrastructure_stats_by_district,
                     fallback_tool])


def main():
    print("Welcome to the Dubai Infrastructure Management Agent!")
    print("Type 'exit' to quit.")
    while True:
        user_input = input("\nEnter your query: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        response = agent(user_input)
        # Ensure response.message is a string
        msg = response.message
        if not isinstance(msg, str):
            msg = str(msg)
        print("\n" + msg)


if __name__ == "__main__":
    main()