# High-Level Solution Design: AI Storm Overflow Advisor

## 1. Executive Summary
The **AI Storm Overflow Advisor** is an agentic AI system designed to proactively manage pollution risks in the water network. Unlike traditional dashboards that simply display data, this system acts as an intelligent co-pilot, autonomously analyzing complex telemetry, predicting risks, and recommending specific operational interventions.

![Solution Architecture Diagram](/Users/ajaichaudhary/.gemini/antigravity/brain/b49615dc-d371-42e6-a2f5-1874e84f1084/solution_architecture_diagram_1764505532803.png)

## 2. Agentic Architecture Principles
This solution adopts a **Multi-Agent Architecture** orchestrated by **LangGraph**. It adheres to key Agentic AI best practices:

*   **Separation of Concerns**: specialized agents (Planner, Risk Engine, Advisor) handle distinct cognitive tasks.
*   **Deterministic vs. Probabilistic**: Critical safety logic (Risk Engine) is deterministic and rule-based, while interpretation and communication (Advisor) utilize LLMs.
*   **Human-in-the-Loop**: The system proposes actions (Job Tickets) but requires explicit operator approval to execute, ensuring safety in critical infrastructure.
*   **Shared State**: A unified `AgentState` schema ensures all agents operate on the same context.

## 3. System Components

### 3.1 The "Brain" (LangGraph Orchestrator)
The core logic is a state machine that manages the flow of information between agents.

*   **State Schema**:
    *   `messages`: Chat history for context.
    *   `catchment_id`: The geographic scope of analysis.
    *   `risk_analysis`: Structured data output from the Risk Engine.
    *   `recommendations`: Natural language advice from the Advisor.

### 3.2 Agent Roles

#### 🤖 Planner Agent (The "Ear")
*   **Role**: Intent Recognition & Context Extraction.
*   **Function**: Parses user natural language (e.g., "Check C-03") to determine the target catchment and time horizon.
*   **AI Pattern**: Zero-shot extraction using LLM.

#### ⚙️ Risk Engine (The "Calculator")
*   **Role**: Deterministic Risk Assessment.
*   **Function**: Aggregates rainfall forecasts and telemetry data. Applies hard-coded safety rules (e.g., "If Level > 1.5m AND Rain > 5mm") to flag **Spill** or **Blockage** risks.
*   **Best Practice**: **Hallucination Prevention**. By using code-based logic instead of an LLM for math/thresholds, we guarantee accuracy.

#### 🧠 Advisor Agent (The "Voice")
*   **Role**: Synthesis & Recommendation.
*   **Function**: Consumes the structured risk data and generates a plain-English explanation (Chain of Thought). Suggests operational actions based on the specific risk type.
*   **AI Pattern**: Context-aware generation.

### 3.3 User Interface (Streamlit)
*   **Control Room View**: Real-time chat interface.
*   **Dynamic Context**: Sidebar controls for catchment selection.
*   **Actionable UI**: "Create Job" buttons generated dynamically based on high-risk findings, closing the loop between insight and action.

## 4. Data Flow
1.  **Ingest**: User Query ("Show risk for C-01") → **Planner** extracts `C-01`.
2.  **Process**: **Risk Engine** fetches CSV stubs for C-01, runs logic, outputs `JSON` risk list.
3.  **Synthesize**: **Advisor** reads `JSON`, writes summary ("Critical risk at CSO-001 due to heavy rain").
4.  **Act**: UI renders summary + "Create Job" button. User clicks → Job Ticket JSON created.

## 5. Technology Stack
*   **Orchestration**: LangGraph / LangChain
*   **LLM**: OpenAI GPT-4o
*   **Frontend**: Streamlit
*   **Containerization**: Docker
*   **Deployment**: Google Cloud Run
