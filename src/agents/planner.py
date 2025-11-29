

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from src.state import AgentState
import json

def planner_node(state: AgentState):
    """
    Planner agent that interprets the user's request to extract the Target Catchment and Time Horizon.
    """
    messages = state['messages']
    
    # Simple extraction via LLM
    # In a real scenario, we would use function calling or structured output.
    # For this PoC, we'll ask for a JSON response.
    

    system_prompt = """You are a Planner Agent for a Storm Overflow Risk system.
    Your job is to extract the 'catchment_id' and 'time_horizon' from the user's request.
    
    Available Catchments: C-01, C-02, C-03, C-04, C-05
    Default Time Horizon: 48 hours
    
    Rules:
    1. If the user specifies a catchment (e.g., "Check C-03"), use that.
    2. If the user does NOT specify a catchment, use the one provided in the [Context].
    3. If neither is present, default to C-01.
    
    Output strictly valid JSON:
    {{
        "catchment_id": "C-01",
        "time_horizon": "48 hours"
    }}
    """

    
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{input}")
    ])
    
    chain = prompt | llm
    
    last_message = messages[-1].content
    response = chain.invoke({"input": last_message})
    
    try:
        content = response.content.strip()
        # Handle potential markdown code blocks
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
            
        data = json.loads(content)
        return {
            "catchment_id": data.get("catchment_id", "C-01"),
            "time_horizon": data.get("time_horizon", "48 hours")
        }
    except Exception as e:
        # Fallback
        print(f"Planner extraction failed: {e}")
        return {"catchment_id": "C-01", "time_horizon": "48 hours"}

