import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from .env file FIRST
load_dotenv()

# Now, import the other modules
from langgraph.graph import StateGraph, END
from state import GraphState
from agents import parse_cv, analyze_skills, analyze_market, analyze_skill_gap, format_report

# Verify that the API keys are loaded and available
if not os.getenv("GOOGLE_API_KEY"):
    st.error("GOOGLE_API_KEY not found in .env file. Please check your configuration.")
    st.stop()
if not os.getenv("JSEARCH_API_KEY"):
    st.error("JSEARCH_API_KEY not found in .env file. Please check your configuration.")
    st.stop()

# Define the workflow (copied from main.py)
workflow = StateGraph(GraphState)

# Add the nodes (each node is an agent function)
workflow.add_node("cv_parser", parse_cv)
workflow.add_node("skill_analyst", analyze_skills)
workflow.add_node("market_analyst", analyze_market)
workflow.add_node("gap_analyzer", analyze_skill_gap)
workflow.add_node("report_generator", format_report)

# Set the entrypoint
workflow.set_entry_point("cv_parser")

# Add the edges to define the sequence of execution
workflow.add_edge("cv_parser", "skill_analyst")
workflow.add_edge("skill_analyst", "market_analyst")
workflow.add_edge("market_analyst", "gap_analyzer")
workflow.add_edge("gap_analyzer", "report_generator")
workflow.add_edge("report_generator", END)

# Compile the graph into a runnable application
app = workflow.compile()

st.set_page_config(page_title="AI-Powered Skill Gap Analyst", layout="wide")

st.title("AI-Powered Skill Gap Analyst")

st.markdown("""
This application analyzes a candidate's CV against market demands for a target role
to identify skill gaps, key strengths, and provide an upskilling plan.
""")

# Input fields
cv_content = st.text_area("Paste CV Content Here:", height=300, help="Enter the full text content of the candidate's CV.")
target_role = st.text_input("Target Job Role:", "Senior AI Engineer", help="Specify the job role for which to perform the skill gap analysis.")

if st.button("Run Analysis"):
    if not cv_content:
        st.warning("Please paste the CV content to run the analysis.")
    elif not target_role:
        st.warning("Please enter a target job role.")
    else:
        with st.spinner("Running skill gap analysis... This might take a few moments."):
            try:
                inputs = {
                    "cv_content": cv_content,
                    "target_role": target_role
                }
                result = app.invoke(inputs)

                st.success("Analysis Complete!")
                st.subheader("Final Report")
                st.markdown(result['final_report'])

                # Option to download the report
                st.download_button(
                    label="Download Report",
                    data=result['final_report'],
                    file_name="skill_gap_report.md",
                    mime="text/markdown"
                )

            except Exception as e:
                st.error(f"An error occurred during analysis: {e}")
                st.exception(e)

st.markdown("---")
st.info("Ensure your `GOOGLE_API_KEY` and `JSEARCH_API_KEY` are set in a `.env` file in the project root.")