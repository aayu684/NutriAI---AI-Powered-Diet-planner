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



