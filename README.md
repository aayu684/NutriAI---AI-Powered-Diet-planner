# 🥗 NutriAI — AI-Powered Personalized Diet Planner

NutriAI is an **agentic AI-driven diet planning system** that generates **highly personalized, nutritionally balanced, and culturally aware 7-day diet plans** using Large Language Models (LLMs).  
It bridges the gap between **expensive human dietitians** and **generic calorie-tracking apps** by offering **intelligent, constraint-aware nutrition planning**.

---

## 🚀 Key Features

-  Agentic AI reasoning for diet planning  
-  Structured and validated AI output using Pydantic  
-  Indian food–friendly and culturally adaptive plans  
-  Automated professional PDF diet report generation  
-  Low-latency AI responses  
-  Privacy-first, stateless architecture  

---

## 📌 Problem Statement

Modern lifestyle diseases such as **obesity, diabetes, and cardiovascular disorders** are increasing rapidly due to sedentary habits and poor dietary choices.

Existing diet applications suffer from:
- Static and generic meal plans  
- Inability to handle allergies, preferences, budget, and lifestyle together  
- Western-centric food suggestions  
- Lack of real reasoning and adaptability  

NutriAI addresses these issues using **LLM-based constrained reasoning**, producing diet plans that align with **real-world human needs**.

---

## 🧠 How NutriAI Works

1. User enters personal, lifestyle, and dietary information  
2. Data is validated and structured using Pydantic schemas  
3. A carefully engineered prompt is sent to Google Gemini AI  
4. The AI generates a structured 7-day diet plan in JSON format  
5. Output is validated again for reliability  
6. Results are displayed on a dashboard and exported as a PDF  

---

## 🏗️ System Architecture

```text
User (Streamlit UI)
↓
UserProfile (Pydantic Schema)
↓
Prompt Engineering + Constraints
↓
Google Gemini AI
↓
Structured JSON Output
↓
Pydantic Validation
↓
Dashboard Display + PDF Report
```

---

## 📂 Project Structure

```text
NutriAI/
│
├── app.py # Streamlit frontend
├── ai_dietitian.py # AI interaction logic
├── models.py # Pydantic data models
├── pdf_generator.py # PDF report generation
├── config.py # Environment configuration
├── requirements.txt
├── .env # API keys (not committed)
└── README.md
```

---

## 🧪 Data Validation & Reliability

NutriAI uses a **schema-first design** to ensure reliability and correctness.

### Core Data Models
- UserProfile  
- WeeklyDietPlan  
- DailyPlan  
- MealPlan  
- NutritionInfo  

All AI-generated outputs are **strictly validated** before being used or displayed, preventing hallucinated or malformed data.

---

## 🖥️ User Interface

### Sidebar (Input Panel)
- Age, Height, Weight  
- Activity Level  
- Health Goal  
- Dietary Restrictions  
- Allergies, Preferences & Budget  

### Dashboard (Output Panel)
- Weekly calorie & macro summary  
- Expandable daily meal plans  
- Meal-wise nutrition breakdown  
- One-click PDF download  

---

## 📄 PDF Report

The system generates a **professional, print-ready PDF** containing:
- User profile summary  
- Complete 7-day diet plan  
- Nutritional breakdown  
- Consolidated grocery shopping list  

---

## ⚙️ Tech Stack

### Programming Language
- Python 3.10+

### Frontend
- Streamlit

### AI & Intelligence
- Google Gemini API (gemini-2.5-flash)

### Data Validation
- Pydantic

### Reporting
- ReportLab

### Security
- python-dotenv

---

## ▶️ Installation & Execution

### Step 1: Clone Repository
```bash
git clone https://github.com/your-username/NutriAI.git
cd NutriAI
```
### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```
### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```
### Step 4: Configure Environment Variables
Create a .env file:
```bash
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```
### Step 5: Run the Application
```bash
streamlit run app.py
```

## 🎯 Future Enhancements 

- 📷 Food recognition via images (Vision AI)

- ⌚ Wearable integration (Fitbit / Google Fit)

- 🛒 Grocery app integrations

- 🔁 Long-term preference memory

- 📈 Reinforcement learning from user feedback

## 📌 Conclusion

NutriAI demonstrates how agentic AI + structured validation can build trustworthy, real-world health applications.
It shifts diet planning from static templates to dynamic reasoning, marking a significant step toward AI-assisted preventive healthcare.

## 👨‍💻 Made by
- **Aayushi soni** – [GitHub](https://github.com/aayu684) | [LinkedIn](https://www.linkedin.com/in/aayushisoni6295/)
- **Ishitaba Umat** – [GitHub](https://github.com/IshitaUmat) | [LinkedIn](https://www.linkedin.com/in/ishita-umat-4a8791282/)





