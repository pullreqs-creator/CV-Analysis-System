
# CV-Analysis-System: AI-Powered Skill Gap Analyst

## 1. Objective & Architecture

CV-Analysis-System is an AI-powered multi-agent system designed to assist technical recruiters. It analyzes a candidate's CV, compares it against current market demands for specific roles, and generates an actionable skill-gap report. The system leverages Python and the LangGraph framework to coordinate five independent agents in a streamlined workflow.

### Architectural Overview

The CV-Analysis-System operates as a multi-agent pipeline, where each agent performs a distinct step in the skill gap analysis process. The overall workflow looks like this:

```
Start
  │
  ▼
[CV Parser]
  │
  ▼
[Skill Analyst]
  │
  ▼
[Market Analyst]
  │
  ▼
[Gap Analyzer]
  │
  ▼
[Report Formatter]
  │
  ▼
End
```

#### Agent Responsibilities

1. **CV Parser:**  
   - Ingests the raw CV text.
   - Extracts and normalizes information such as work experience, skills, education, and projects.
   - Outputs a structured JSON for downstream analysis.

2. **Skill Analyst:**  
   - Analyzes the structured CV data.
   - Identifies both explicit (listed) and implicit (inferred) skills.
   - Infers advanced technical skills from context (e.g., use of AI frameworks).

3. **Market Analyst:**  
   - Queries real-time job data using the JSearch API.
   - Aggregates current market demand for skills and technologies for the specified role.
   - Summarizes in-demand skills and requirements from job listings.

4. **Gap Analyzer:**  
   - Compares the candidate’s skills profile against the market demands.
   - Identifies missing or underrepresented skills.
   - Produces a structured gap analysis highlighting areas for improvement.

5. **Report Formatter:**  
   - Assembles results from all previous agents.
   - Formats the skill gap analysis into a clear, actionable Markdown report for recruiters or candidates.

This modular, agent-driven workflow ensures each component is focused, maintainable, and extensible for future upgrades.


## 2. Environment Setup

Follow these steps to set up and run the project locally.

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd CV-Analysis-System
```

### Step 2: Create and Activate a Virtual Environment

```bash
# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up API Keys

You will need two API keys for this project. Create a file named `.env` in the root directory and add your keys:

```bash
# Get this from Google AI Studio or Google Cloud Console
GOOGLE_API_KEY="your-google-api-key-here"

# Get this from RapidAPI by subscribing to the JSearch API
JSEARCH_API_KEY="your-jsearch-api-key-here"
```

- [Google AI Studio](https://aistudio.google.com/app/apikey)
- [JSearch on RapidAPI](https://rapidapi.com/jsearch/api/jsearch)

**Note:** If you use the Vertex AI library, you do not need the GOOGLE_API_KEY in `.env`. Instead, authenticate via:
```bash
gcloud auth application-default login
```

---

## 3. How to Run the Application

### A. Run from the Command Line

Ensure you have a `sample_cv.txt` file in the root directory. Then run:

```bash
python main.py
```

The application will execute the agent workflow, print the report to your console, and save it as `final_report.md`.

### B. Run with Streamlit

For an interactive web interface, you can run the application using Streamlit. This allows you to upload CVs and view results in your browser.

```bash
streamlit run streamlit_app.py
```

- Open the provided local URL in your browser.
- Upload a CV or use the sample data.
- The app will display the skill gap analysis and allow you to download the markdown report.

---

## 4. Sample Output

A sample generated report can be found in `final_report.md`. It demonstrates how the system synthesizes CV and job market data into an actionable skill gap summary.

---

## 5. Contributing

Pull requests and suggestions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 6. License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
