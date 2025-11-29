

from src.state import AgentState
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import json

def advisor_node(state: AgentState):
    """
    Advisor Agent (LLM).
    Interprets the risk analysis and generates a natural language summary and recommendations.
    """
    risk_analysis = state['risk_analysis']
    catchment_id = state.get('catchment_id', 'C-01')
    
    # Filter for High/Critical risks
    high_risks = [r for r in risk_analysis if r['risk_score'] in ['High', 'Critical']]
    
    if not high_risks:
        return {"recommendations": f"No significant risks detected for Catchment {catchment_id} in the next 48 hours."}
    
    # Prepare context for LLM
    context_str = json.dumps(high_risks, indent=2)
    
    system_prompt = """You are an AI Storm Overflow Advisor.
    Analyze the provided risk data for the catchment.
    
    For each high-risk asset:
    1. Explain WHY it is at risk in plain English.
    2. Recommend a specific operational action (e.g., "Inspect for blockage", "Pre-emptive jetting", "Optimize upstream storage").
    
    Format the output as a clear, prioritized list.
    """
    

    llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "Risk Data: {risk_data}")
    ])
    
    chain = prompt | llm
    response = chain.invoke({"risk_data": context_str})

    
    return {"recommendations": response.content}

