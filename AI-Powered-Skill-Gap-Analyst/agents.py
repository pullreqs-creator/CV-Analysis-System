import os
from typing import List
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

# Import from the new state.py file
from state import GraphState
from tools import search_market_trends

# --- Define the LLM for all agents ---
# The model will read the key from the .env file when the main script runs.
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", # Changed from gemini-2.5-flash for potentially higher accuracy
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    # Adding a timeout for the more complex generation tasks
    request_timeout=90 # Slightly reduced timeout for faster feedback, adjust as needed
)

# --- Pydantic Models for Structured Output ---

class StructuredCV(BaseModel):
    """Structured representation of a CV."""
    summary: str = Field(description="A brief summary of the candidate's profile.")
    experience: List[str] = Field(description="List of professional experiences.")
    skills: List[str] = Field(description="List of key skills mentioned.")
    education: List[str] = Field(description="List of educational qualifications.")
    projects: List[str] = Field(description="List of notable projects.")

class SkillGap(BaseModel):
    """Represents a single skill gap or alignment."""
    market_demand: str = Field(description="A specific skill or requirement from the job market analysis.")
    candidate_skill_alignment: str = Field(description="How the candidate's skills align with this demand. Note strengths, partial matches, or clear gaps.")

class GapAnalysisResult(BaseModel):
    """Structured output for the skill-gap analysis."""
    skill_gaps: List[SkillGap]
    key_strengths: List[str] = Field(description="A bulleted list of the candidate's key strengths.")
    upskilling_plan: List[str] = Field(description="A bulleted list of actionable upskilling recommendations.")

# --- Agent Definitions ---

def parse_cv(state: GraphState):
    """
    Parses the raw CV text into a structured format using an LLM.
    Role: The "Data Engineer" agent.
    """
    print("---AGENT: CV Parser---")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert CV parser. Your job is to extract information from a given CV text and structure it into the provided JSON format. Focus on key details like professional experience, skills, and education."),
        ("human", "Please parse the following CV content: \n\n{cv_content}")
    ])
    
    structured_llm = llm.with_structured_output(StructuredCV)
    chain = prompt | structured_llm
    
    structured_output = chain.invoke({"cv_content": state['cv_content']})
    
    return {"structured_cv": structured_output.dict()}

def analyze_skills(state: GraphState):
    """
    Analyzes the structured CV to infer explicit and implicit skills.
    Role: The "Subject Matter Expert" agent.
    """
    print("---AGENT: Skill Analyst---")
    prompt = ChatPromptTemplate.from_template(
        """Analyze the following structured CV for the target role of '{target_role}'. 
        Identify all explicit skills listed. More importantly, infer implicit skills. 
        For example, a project using 'LangChain' implies knowledge of 'LLMs' and 'Python'. 
        Provide a detailed analysis of the candidate's capabilities.
        
        Structured CV:
        {structured_cv}"""
    )
    chain = prompt | llm
    result = chain.invoke({
        "structured_cv": state['structured_cv'], 
        "target_role": state['target_role']
    })
    return {"skill_analysis": result.content}

def analyze_market(state: GraphState):
    """
    Gathers market intelligence for the target role using a search tool.
    Role: The "Market Researcher" agent.
    """
    print("---AGENT: Market Intelligence---")
    market_summary = search_market_trends.invoke({"role": state['target_role']})
    return {"market_analysis": market_summary}

def analyze_skill_gap(state: GraphState):
    """
    Compares the candidate's skills with market demands to identify gaps, strengths, and suggest an upskilling plan.
    Role: The "Analysis" agent.
    """
    print("---AGENT: Gap Analyzer---")
    prompt = ChatPromptTemplate.from_template(
        """You are an expert HR analyst. Your task is to perform a detailed skill-gap analysis by comparing a candidate's skills with the current market demands for a '{target_role}'.

        **Candidate's Skills Summary:**
        {skill_analysis}

        **Market Demand Summary:**
        {market_analysis}

        Based on the two summaries above, provide a detailed analysis. Your output MUST be a JSON object that follows the specified schema. For the 'skill_gaps' array, create an entry for each major market demand identified.
        
        **Instructions:**
        1.  **skill_gaps:** For each key market demand, create an object. In 'candidate_skill_alignment', clearly state how the candidate's skills (both explicit and implicit) align. Mention if it's a strong match, a developing skill, or a gap.
        2.  **key_strengths:** List the candidate's most prominent strengths that make them a good fit for this role.
        3.  **upskilling_plan:** Suggest a concise, actionable upskilling plan to address the identified gaps. Be specific with technologies or concepts.
        """
    )
    
    structured_llm = llm.with_structured_output(GapAnalysisResult)
    chain = prompt | structured_llm
    
    try:
        analysis_result = chain.invoke({
            "skill_analysis": state['skill_analysis'],
            "market_analysis": state['market_analysis'],
            "target_role": state['target_role']
        })
        return {"gap_analysis": analysis_result}
    except Exception as e:
        print(f"Error during gap analysis: {e}")
        return {"gap_analysis": None}

def format_report(state: GraphState):
    """
    Takes all the analyzed data and formats it into the final Markdown report.
    Role: The "Communicator" agent.
    """
    print("---AGENT: Report Formatter---")
    
    gap_analysis_data = state.get('gap_analysis')
    if not gap_analysis_data:
        return {"final_report": "Error: Gap analysis data is missing and the report could not be generated."}

    # Build the Markdown table from the structured gap analysis
    table = "| Market Demand | Candidate Skill Alignment |\n"
    table += "|---|---|\n"
    for item in gap_analysis_data.skill_gaps:
        market_demand = item.market_demand.replace("\n", " ")
        skill_alignment = item.candidate_skill_alignment.replace("\n", " ")
        table += f"| {market_demand} | {skill_alignment} |\n"

    # Build the strengths list
    strengths = "\n".join([f"* {s}" for s in gap_analysis_data.key_strengths])

    # Build the upskilling plan list
    upskilling_plan = "\n".join([f"* {p}" for p in gap_analysis_data.upskilling_plan])

    # Assemble the final report
    final_report = f"""
# {state['target_role']} Candidate Summary Report

## 1. Candidate Skill Analysis
{state['skill_analysis']}

## 2. Current Market Demands for {state['target_role']}
{state['market_analysis']}

## 3. Skill-Gap Analysis
The candidate's profile has been compared against current market demands. Here is the breakdown:

{table}

## 4. Key Strengths
{strengths}

## 5. Personalized Upskilling Plan
{upskilling_plan}
"""
    return {"final_report": final_report.strip()}

