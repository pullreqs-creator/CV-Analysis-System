from typing import TypedDict, List, Dict, Any

class GraphState(TypedDict):
    """
    Represents the state of our graph. It's a dictionary that will be passed
    between nodes, with each node adding or modifying its fields.

    Attributes:
        cv_content: The raw text content of the CV.
        target_role: The job role we are analyzing the CV for.
        structured_cv: The CV parsed into a structured format (JSON/dict).
        skill_analysis: A detailed text analysis of the candidate's explicit and implicit skills.
        market_analysis: A summary of current market demands for the role based on real job listings.
        gap_analysis: A structured object containing the skill gap analysis, strengths, and upskilling plan.
        final_report: The final, well-structured report in Markdown format.
    """
    cv_content: str
    target_role: str
    structured_cv: Dict
    skill_analysis: str
    market_analysis: str
    gap_analysis: Any # Using 'Any' to hold the Pydantic model instance
    final_report: str
