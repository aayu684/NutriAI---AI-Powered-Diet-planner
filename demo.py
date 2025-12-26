#!/usr/bin/env python3
"""
Demo script for testing AI Dietitian and PDF generation components.
Run this to test core functionality without Streamlit.
"""

import os
from dotenv import load_dotenv
from models import UserProfile, ActivityLevel, Goal, DietaryRestriction
from ai_dietitian import AIDietitian
from pdf_generator import DietPlanPDFGenerator

# Load environment variables
load_dotenv()

# Use your API key here
API_KEY = os.getenv("your_api_key")
API_URL = "https://api.gemini.ai/v1/generate"

def generate_diet_plan(user_data):
    prompt = (
        f"Create a personalized diet plan for a {user_data['age']} year old "
        f"{user_data['gender']} weighing {user_data['weight']} kg and "
        f"height {user_data['height']} cm."
    )
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gemini-pro-2.5",
        "prompt": prompt,
        "max_tokens": 500
    }
    import requests
    response = requests.post(API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["text"]
    else:
        print("API error:", response.text)
        return None

def test_ai_dietitian():
    print("🧪 Testing AI Dietitian Service...")
    try:
        ai_dietitian = AIDietitian()
        profile = UserProfile(
            name="Sarah", age=28, gender="female", height_cm=165,
            weight_kg=72, target_weight_kg=65,
            activity_level=ActivityLevel.MODERATELY_ACTIVE,
            goal=Goal.WEIGHT_LOSS,
            dietary_restrictions=[DietaryRestriction.NONE],
            allergies=[],
            preferences=["Mediterranean", "vegetables"],
            dislikes=["spicy food"],
            daily_routine={"wake_up": "7:00 AM", "bedtime": "10:00 PM"},
            cooking_skill="beginner",
            budget_constraint=None,
            cultural_preferences=["Mediterranean"]
        )
        print("✅ Profile created")
        plan_text = generate_diet_plan({
            "weight": profile.weight_kg,
            "height": profile.height_cm,
            "age": profile.age,
            "gender": profile.gender
        })
        print("Generated Plan:\n", plan_text)
        # Wrap plan_text into a Plan object if needed
        return profile, plan_text
    except Exception as e:
        print("Error:", e)
        return None, None

def test_pdf_generation(plan_text):
    print("🧪 Testing PDF Generation Service...")
    try:
        pdf_gen = DietPlanPDFGenerator()
        filename = pdf_gen.generate_diet_plan_pdf(plan_text)
        if os.path.exists(filename):
            print("✅ PDF generated:", filename)
            os.remove(filename)  # Clean up
            return True
        else:
            print("PDF not found")
            return False
    except Exception as e:
        print("Error:", e)
        return False

def main():
    profile, plan_text = test_ai_dietitian()
    if profile and plan_text:
        test_pdf_generation(plan_text)

if __name__ == "__main__":
    main()
