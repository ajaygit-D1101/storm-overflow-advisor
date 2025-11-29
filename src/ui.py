

import streamlit as st
import sys
import os
import pandas as pd
from langchain_core.messages import HumanMessage

# Add root to path to ensure imports work
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.graph import create_graph

try:
    import config
    if hasattr(config, 'OPENAI_API_KEY'):
        os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY
except ImportError:
    pass # Config might not exist or be needed if env var is set otherwise

st.set_page_config(page_title="AI Storm Overflow Advisor", layout="wide")

st.title("AI Storm Overflow & Sewer Blockage Risk Advisor")
st.markdown("### Control Room View")

# Initialize Graph
if "graph" not in st.session_state:
    st.session_state.graph = create_graph()


# Sidebar for Context
with st.sidebar:
    st.header("System Status")
    st.success("Agent System: Online")
    
    # Dynamic Catchment Selection
    selected_catchment = st.selectbox(
        "Active Catchment",
        ["C-01", "C-02", "C-03", "C-04", "C-05"],
        index=0
    )
    st.info(f"Monitoring: {selected_catchment}")
    
    with st.expander("System Diagram"):
        st.image("src/assets/cso_diagram.png", caption="Combined Sewer System Overview", use_container_width=True)
    
    st.markdown("---")
    st.markdown("**Available Commands:**")
    st.markdown(f"- *Show risk for {selected_catchment}*")
    st.markdown(f"- *What is the blockage risk in {selected_catchment}?*")
    st.markdown(f"- *Are there any spill risks in {selected_catchment}?*")
    st.markdown(f"- *Recommend actions for {selected_catchment}*")
    st.markdown("- *Check status of CSO-001*")
    st.markdown("- *Analyze storm overflow risk*")


# Helper to run analysis
def run_analysis(user_prompt):
    # Display user message if it's not a system auto-run
    if user_prompt:
        st.chat_message("user").markdown(user_prompt)
        st.session_state.messages.append({"role": "user", "content": user_prompt})
    
    # Run Agent Graph
    with st.spinner("Analyzing Network Conditions..."):
        try:
            # Inject Context into the prompt for the Agent
            actual_prompt = user_prompt if user_prompt else f"Show risk for {selected_catchment}"
            context_prompt = f"{actual_prompt} [Context: User is viewing Catchment {selected_catchment}]"
            
            initial_state = {"messages": [HumanMessage(content=context_prompt)]}
            result = st.session_state.graph.invoke(initial_state)
            
            # Extract outputs
            risk_analysis = result.get("risk_analysis", [])
            recommendations = result.get("recommendations", "No recommendations generated.")
            
            # Store latest analysis for persistent actions
            st.session_state.latest_risk_analysis = risk_analysis
            
            # Display Advisor Response
            with st.chat_message("assistant"):
                st.markdown(recommendations)
                
                # Display Risk Table if available
                if risk_analysis:
                    st.markdown("### Detailed Risk Analysis")
                    df = pd.DataFrame(risk_analysis)
                    st.dataframe(df, use_container_width=True)
            
            st.session_state.messages.append({"role": "assistant", "content": recommendations})
                                
        except Exception as e:
            st.error(f"Error running agent: {e}")

# Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Track previous catchment to detect changes
if "last_catchment" not in st.session_state:
    st.session_state.last_catchment = selected_catchment

# Auto-run if catchment changed or if it's the first load
if selected_catchment != st.session_state.last_catchment or not st.session_state.messages:
    st.session_state.last_catchment = selected_catchment
    st.session_state.messages = [] 
    st.session_state.latest_risk_analysis = [] # Clear previous analysis
    run_analysis(None) # Auto-run with default prompt

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Persistent Action Area
if "latest_risk_analysis" in st.session_state and st.session_state.latest_risk_analysis:
    risk_analysis = st.session_state.latest_risk_analysis
    # Filter for high risks
    high_risks = [r for r in risk_analysis if r['risk_score'] in ['High', 'Critical']]
    
    if high_risks:
        st.markdown("---")
        st.subheader("⚠️ Recommended Actions (Active)")
        cols = st.columns(len(high_risks))
        for idx, risk in enumerate(high_risks):
            asset_id = risk['asset_id']
            with cols[idx]:
                if st.button(f"Create Job for {asset_id}", key=f"btn_persist_{asset_id}"):
                    from src.tools.job_tools import create_job_stub
                    action_type = "Inspection" if "blockage" in risk['reasons'].lower() else "Maintenance"
                    job_stub = create_job_stub(asset_id, action_type, risk['reasons'])
                    st.success(f"Job Ticket Created: {asset_id}")
                    st.json(job_stub)

# User Input
if prompt := st.chat_input("Ask the Risk Advisor..."):
    run_analysis(prompt)


