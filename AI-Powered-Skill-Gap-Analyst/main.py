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
    raise EnvironmentError("GOOGLE_API_KEY not found in .env file. Please check your configuration.")
if not os.getenv("JSEARCH_API_KEY"):
    raise EnvironmentError("JSEARCH_API_KEY not found in .env file. Please check your configuration.")


# Define the workflow
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


# --- Main execution block ---
if __name__ == "__main__":
    try:
        with open("sample_cv.txt", "r") as f:
            cv_text = f.read()

        # Define the initial state for the graph
        inputs = {
            "cv_content": cv_text,
            "target_role": "Senior AI Engineer"
        }

        # Run the graph
        print("Starting AI Skill Gap Analysis...")
        result = app.invoke(inputs)

        # Print the final report
        print("\n" + "="*50)
        print("          FINAL REPORT")
        print("="*50 + "\n")
        print(result['final_report'])

        # Save the report to a file
        with open("final_report.md", "w") as f:
            f.write(result['final_report'])
        print("\n--- Report saved to final_report.md ---")

    except FileNotFoundError:
        print("Error: 'sample_cv.txt' not found. Please create this file with a sample CV.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

