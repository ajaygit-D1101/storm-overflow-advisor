
import sys
import os
from langchain_core.messages import HumanMessage

# Add root to path
sys.path.append(os.path.dirname(__file__))

try:
    import config
    if hasattr(config, 'OPENAI_API_KEY'):
        os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY
except ImportError:
    print("Warning: config.py not found or could not be imported.")

from src.graph import create_graph

def test_graph():
    print("Initializing Graph...")
    graph = create_graph()
    
    print("Invoking Graph with test query...")
    initial_state = {
        "messages": [HumanMessage(content="Show me the risk for Catchment C-01")]
    }
    
    try:
        result = graph.invoke(initial_state)
        print("\n--- Execution Successful ---")
        print(f"Catchment: {result.get('catchment_id')}")
        print(f"Risk Analysis Items: {len(result.get('risk_analysis', []))}")
        print("\nRecommendations:")
        print(result.get('recommendations'))
        print("\n----------------------------")
    except Exception as e:
        print(f"\n!!! Execution Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_graph()
