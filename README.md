
# CV-Analysis-System: AI-Powered Skill Gap Analyst

## 1. Objective & Architecture

CV-Analysis-System is an AI-powered multi-agent system designed to assist technical recruiters. It analyzes a candidate's CV, compares it against current market demands for specific roles, and generates an actionable skill-gap report. The system leverages Python and the LangGraph framework to coordinate five independent agents in a streamlined workflow.

### Architectural Overview

The workflow consists of the following agents:

- **CV Parsing & Normalization Agent**: Parses raw CV text and converts it to structured JSON, extracting experience, skills, education, and more.
- **Specialized Skill Analyst Agent**: Identifies explicit and implicit skills from the CV (e.g., inferring LLM knowledge).
- **Market Intelligence Agent**: Queries real-time job listings via the JSearch API to aggregate in-demand skills and technologies.
- **Gap Analysis Agent**: Compares candidate skills to market needs and generates a structured gap analysis.
- **Report Formatting Agent**: Outputs the final, human-readable skill gap report in Markdown.

Workflow:
```
[Start] → [CV Parser] → [Skill Analyst] → [Market Analyst] → [Gap Analyzer] → [Report Formatter] → [End]
```

---

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
