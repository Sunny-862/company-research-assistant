<h1 align="center">🔍 Research AI - AI-Powered Company Research Assistant</h1>

<p align="center">
 
</p>

<p align="center">

![Python](https://img.shields.io/badge/-Python-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/-Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![OpenRouter](https://img.shields.io/badge/-OpenRouter-000000?style=flat)
![Serper](https://img.shields.io/badge/-Serper%20API-4285F4?style=flat&logo=google&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/-BeautifulSoup-43B02A?style=flat)
![GitHub](https://img.shields.io/badge/-GitHub-181717?style=flat&logo=github&logoColor=white)

</p>

---

## 📌 Project Overview

**Research AI** is an AI-powered company intelligence application that automates the process of researching companies.

The user simply enters a **company name or website URL**, and the application automatically discovers the official website, crawls relevant pages, collects public web information, generates AI-powered company intelligence, identifies business pain points, discovers competitors, and creates a downloadable professional PDF report.

The project demonstrates an end-to-end workflow involving **web scraping, REST API integration, LLM usage, data processing, UI development, PDF generation, and cloud deployment**.

---

## 🖥️ Application Preview

<p align="center">
<img width="1920" height="897" alt="Screenshot (1125)" src="https://github.com/user-attachments/assets/60e8f4b9-e56c-48a3-9070-ac3e6f1cbb90" />
</p>

> 📌 Replace `YOUR_SCREENSHOT_URL_HERE` with the GitHub URL of your application screenshot.

---

## 🔄 Application Flow

```text
Company Name / URL
        │
        ▼
Official Website Discovery
        │
        ▼
Website Crawling
        │
        ▼
Live Web Research
        │
        ▼
AI-Powered Analysis
        │
        ▼
Business Pain Point Generation
        │
        ▼
Competitor Discovery
        │
        ▼
Professional PDF Report
```

---

## 🏗️ Architecture

```text
                     ┌──────────────────────┐
                     │        USER          │
                     │ Company Name / URL   │
                     └──────────┬───────────┘
                                │
                                ▼
                     ┌──────────────────────┐
                     │    Streamlit UI      │
                     │       app.py         │
                     └──────────┬───────────┘
                                │
               ┌────────────────┴────────────────┐
               │                                 │
               ▼                                 ▼
     ┌────────────────────┐           ┌────────────────────┐
     │     Serper API     │           │  Website Crawler   │
     │                    │           │                    │
     │ Official Website   │           │ BeautifulSoup      │
     │ Public Research    │           │ Page Extraction    │
     └──────────┬─────────┘           └──────────┬─────────┘
                │                                │
                └────────────────┬───────────────┘
                                 │
                                 ▼
                      ┌────────────────────┐
                      │    OpenRouter API  │
                      │                    │
                      │   LLM Processing   │
                      │   AI Intelligence  │
                      └──────────┬─────────┘
                                 │
                                 ▼
              ┌──────────────────────────────────┐
              │     Structured Company Data      │
              │                                  │
              │  • Company Information           │
              │  • Products & Services           │
              │  • Business Pain Points          │
              │  • Competitor Intelligence       │
              └────────────────┬─────────────────┘
                               │
                               ▼
                    ┌────────────────────┐
                    │  ReportLab PDF     │
                    │     Generator      │
                    └─────────┬──────────┘
                              │
                              ▼
                    📄 Downloadable Report
```

---

## ✨ Features

🔎 Search for companies using a company name or website URL

🌐 Automatically discover the official company website

🕷️ Crawl and extract information from relevant website pages

🔍 Collect additional public company information using live web search

🤖 Generate structured company intelligence using AI

📦 Identify company products and services

💡 Generate potential business pain points

🏢 Discover company competitors and their websites

🔗 Display collected research sources

📄 Generate downloadable professional PDF research reports

⚠️ Handle website, API, and AI processing failures

☁️ Deploy the complete application using Streamlit Community Cloud

---

## 🛠️ Tech Stack & Tools Used

| Category | Tools / Technologies |
| :--- | :--- |
| **Programming Language** | Python |
| **Frontend / Dashboard** | Streamlit |
| **AI / LLM Integration** | OpenRouter API |
| **Live Web Search** | Serper API |
| **Web Scraping** | BeautifulSoup |
| **HTTP Requests** | Requests |
| **PDF Generation** | ReportLab |
| **Environment Management** | python-dotenv |
| **Version Control** | Git & GitHub |
| **Deployment** | Streamlit Community Cloud |

---

## 📁 Project Structure

```bash
company-research-assistant/
│
├── services/
│   ├── __init__.py
│   ├── competitor_service.py
│   ├── crawler.py
│   ├── discord_service.py
│   ├── openrouter_service.py
│   ├── pdf_service.py
│   └── serper_service.py
│
├── utils/
│   ├── __init__.py
│   ├── helpers.py
│   └── prompts.py
│
├── app.py
├── python_test_pipeline.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🔄 Research Pipeline

### 1️⃣ Company Input

The user enters either:

- A company name
- A company website URL

The application processes the input and starts the automated research pipeline.

---

### 2️⃣ Official Website Discovery

🔍 The **Serper API** searches the live web for the company's official website.

🚫 Irrelevant sources and selected third-party domains are filtered.

✅ The most relevant official company website is selected.

---

### 3️⃣ Website Crawling

🕷️ The application crawls the official company website.

📄 Relevant website content is extracted using **BeautifulSoup**.

🧹 The collected content is cleaned and prepared for AI processing.

---

### 4️⃣ Public Web Research

🌐 Additional publicly available information is collected through live web searches.

The research process gathers information related to:

- Company background
- Products and services
- Industry information
- Business operations
- Public company information

---

### 5️⃣ AI-Powered Company Intelligence

🤖 Collected website and research data is sent to an LLM through the **OpenRouter API**.

The AI generates structured intelligence including:

- Company name
- Official website
- Industry
- Country
- Contact information
- Company address
- Company summary
- Products and services
- Potential business pain points

---

### 6️⃣ Competitor Discovery

🏢 The application analyzes company information and identifies relevant competitors.

For each competitor, the application provides:

- Company name
- Website URL

---

### 7️⃣ PDF Report Generation
<img width="1920" height="1080" alt="Screenshot (1129)" src="https://github.com/user-attachments/assets/9a2b42fc-ee47-4b2b-aa48-6e7d9bbe37d3" />


📄 A professional company research report is generated using **ReportLab**.

The report contains:

- Company information
- Company intelligence summary
- Products and services
- AI-generated business pain points
- Competitive landscape
- Research information

The generated PDF can be downloaded directly from the application.

---

## 📊 Research Results Preview

<p align="center">
  <img width="1920" height="881" alt="Screenshot (1126)" src="https://github.com/user-attachments/assets/8fc59e8c-bea5-4802-a790-633178ab08e5" />
</p>

> 📌 Replace `<img width="1196" height="911" alt="Screenshot (1127)" src="https://github.com/user-attachments/assets/0217be81-73cb-4b6e-9a82-a2729c6ab465" />
` with the GitHub URL of your research results screenshot.

---

## 📄 PDF Report Preview

<p align="center">
 <img width="1920" height="1080" alt="Screenshot (1129)" src="https://github.com/user-attachments/assets/9a2b42fc-ee47-4b2b-aa48-6e7d9bbe37d3" />
</p>

> 📌 Replace `
` with the GitHub URL of your PDF report screenshot.

---

## ⚙️ How to Run This Project

### 🔹 Step 1 — Clone the Repository

```bash
git clone https://github.com/Sunny-862/company-research-assistant.git
```

---

### 🔹 Step 2 — Navigate to the Project

```bash
cd company-research-assistant
```

---

### 🔹 Step 3 — Create a Virtual Environment

```bash
python -m venv venv
```

---

### 🔹 Step 4 — Activate the Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

---

### 🔹 Step 5 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 🔹 Step 6 — Configure Environment Variables

Create a `.env` file in the root directory.

Add:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
SERPER_API_KEY=your_serper_api_key
```

⚠️ Never commit the actual `.env` file or API keys to GitHub.

---

### 🔹 Step 7 — Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## ☁️ Deployment

The application is deployed using **Streamlit Community Cloud**.

Deployment process:

1. Push the complete project to GitHub.
2. Connect the GitHub repository to Streamlit Community Cloud.
3. Select `app.py` as the main application file.
4. Configure the required API keys using Streamlit Secrets.
5. Deploy the application.

Required Streamlit Secrets:

```toml
SERPER_API_KEY = "your_serper_api_key"
OPENROUTER_API_KEY = "your_openrouter_api_key"
```

---

## 🔐 Security & Best Practices

✅ API keys are stored using environment variables

✅ `.env` files are excluded using `.gitignore`

✅ Sensitive credentials are not committed to GitHub

✅ Modular service-based project architecture

✅ Separate services for web search, crawling, AI processing, competitor discovery, and PDF generation

✅ Error handling for API and website failures

✅ Environment configuration provided through `.env.example`

---

## ⚠️ Error Handling & Robustness

The application handles common real-world issues including:

- Invalid company names or URLs
- Official website discovery failures
- Websites blocking automated crawling
- API request failures
- Missing environment variables
- AI response parsing errors
- Incomplete research results

---

## 📚 Learnings From This Project

🎯 Building an end-to-end AI automation application

🎯 Integrating REST APIs with Python

🎯 Implementing live web search

🎯 Crawling and extracting website information

🎯 Integrating LLM APIs into real-world applications

🎯 Structuring and processing AI-generated responses

🎯 Implementing competitor intelligence

🎯 Generating professional PDF reports

🎯 Building interactive applications using Streamlit

🎯 Deploying Python applications to the cloud

🎯 Managing environment variables and API credentials securely

---

## 🚀 Future Improvements

🔹 Discord bot integration

🔹 Research history and caching

🔹 Asynchronous website crawling

🔹 Additional company intelligence data sources

🔹 Advanced competitor comparison

🔹 User authentication

🔹 Multiple report export formats

🔹 Database integration for storing previous research

---

## 📬 Connect With Me

- **Sunny Kadam**

- 📧 Email: sunnykadam872@gmail.com

- 💼 LinkedIn: www.linkedin.com/in/sunny-862

- 💻 GitHub: Sunny-862

---

## ⚠️ Disclaimer

This application collects and analyzes publicly available web information.

AI-generated insights and business pain points are inferences based on collected data and should be independently verified before being used for business decisions.

---

## 📜 License

This project was developed as part of an **AI & Automation Developer Hiring Challenge**.
