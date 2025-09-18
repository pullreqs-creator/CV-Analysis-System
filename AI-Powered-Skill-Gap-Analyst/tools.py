import os
import requests
import json
from langchain_core.tools import tool

@tool
def search_market_trends(role: str) -> str:
    """
    Uses the JSearch API to find real, current job listings for a given role 
    and summarizes the key skills and requirements found in the top results.
    This provides real-world context for the skill gap analysis.
    """
    print(f"---SEARCHING FOR REAL-TIME JOB DATA FOR: {role}---")
    
    api_key = os.getenv("JSEARCH_API_KEY")
    if not api_key:
        return "Error: JSearch API key not found in environment variables."

    url = "https://jsearch.p.rapidapi.com/search"
    querystring = {"query": f"{role} in USA", "num_pages": "1"}
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=30)
        response.raise_for_status()
        
        results = response.json().get('data', [])
        if not results:
            return "No job listings found for this role."

        summary = "Based on the top job listings, here are the current market demands:\n\n"
        
        for job in results[:5]:
            title = job.get('job_title', 'N/A')
            employer = job.get('employer_name', 'N/A')
            description = job.get('job_description', 'No description available.')
            
            if len(description) > 400:
                description_snippet = description[:400].rsplit(' ', 1)[0] + "..."
            else:
                description_snippet = description

            summary += f"- **{title} at {employer}:** {description_snippet}\n"

        return summary

    except requests.exceptions.RequestException as e:
        return f"Error fetching job data: {e}"
    except json.JSONDecodeError:
        return "Error: Failed to parse the response from the job search API."

