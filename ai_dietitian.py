import json
from typing import List, Dict, Any, Optional

import google.generativeai as genai
from google.generativeai import types

from models import UserProfile, WeeklyDietPlan
from config import Config


class AIDietitian:
    """AI Dietitian service using Gemini 2.5 Flash"""

    def __init__(self):
        Config.validate()
        # Configure Gemini API with the API key
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model_name = Config.GEMINI_MODEL

        self.system_prompt = self._get_system_prompt()
        self.few_shot_examples = self._get_few_shot_examples()
        self.cot_prompts = self._get_cot_prompts()

    def _get_system_prompt(self) -> str:
        return (
            "You are a certified clinical nutritionist and registered dietitian.\n"
            "Design safe, practical, Indian-friendly diet plans when possible, and explain clearly.\n"
            "Keep answers structured and easy to follow."
        )

    def _get_few_shot_examples(self) -> List[Dict[str, str]]:
        return [
            {
                "user": "I want to lose fat but keep muscle.",
                "assistant": (
                    "Great goal! To customize a plan, please share your age, gender, "
                    "height, current weight, target weight, daily activity level, "
                    "any medical issues, and foods you like or want to avoid."
                ),
            }
        ]

    def _get_cot_prompts(self) -> Dict[str, str]:
        return {
            "profile_extraction": "Think step by step and extract all user profile fields cleanly.",
            "meal_planning": "Think step by step to build a realistic weekly Indian-friendly meal plan.",
        }

    # ------------ basic chat ------------

    def chat(self, message: str, conversation_history: List[Dict[str, str]]) -> str:
        """Chat with Gemini model."""
        model = genai.GenerativeModel(self.model_name, system_instruction=self.system_prompt)
        
        # Build message history with few-shot examples
        messages = []
        
        # Add few-shot examples
        for ex in self.few_shot_examples:
            messages.append({"role": "user", "parts": ex["user"]})
            messages.append({"role": "model", "parts": ex["assistant"]})
        
        # Add conversation history
        for turn in conversation_history:
            if "role" in turn and "content" in turn:
                # Handle Streamlit format: {"role": "user"/"assistant", "content": "..."}
                role = "model" if turn["role"] == "assistant" else turn["role"]
                messages.append({"role": role, "parts": turn["content"]})
            elif "user" in turn:
                messages.append({"role": "user", "parts": turn["user"]})
            if "assistant" in turn and "role" not in turn:
                messages.append({"role": "model", "parts": turn["assistant"]})
        
        # Add current message
        messages.append({"role": "user", "parts": message})
        
        # Generate response
        response = model.generate_content(messages)
        return response.text

    # ------------ user profile extraction ------------

    def extract_user_profile(
        self, conversation_history: List[Dict[str, str]]
    ) -> Optional[UserProfile]:
        """Extract user profile from conversation using structured output."""
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "gender": {"type": "string"},
                "height_cm": {"type": "number"},
                "weight_kg": {"type": "number"},
                "target_weight_kg": {"type": "number"},
                "activity_level": {"type": "string"},
                "goal": {"type": "string"},
                "dietary_restrictions": {"type": "array", "items": {"type": "string"}},
                "allergies": {"type": "array", "items": {"type": "string"}},
                "preferences": {"type": "array", "items": {"type": "string"}},
                "dislikes": {"type": "array", "items": {"type": "string"}},
                "daily_routine": {
                    "type": "object",
                    "properties": {
                        "wake_time": {"type": "string"},
                        "sleep_time": {"type": "string"}
                    }
                },
                "cooking_skill": {"type": "string"},
                "budget_constraint": {"type": "string"},
                "cultural_preferences": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["name", "age", "gender", "height_cm", "weight_kg"],
        }

        # Convert conversation history to readable format
        formatted_history = ""
        for turn in conversation_history:
            if "role" in turn and "content" in turn:
                role = turn["role"].upper()
                formatted_history += f"{role}: {turn['content']}\n"
            elif "user" in turn and "assistant" in turn:
                formatted_history += f"USER: {turn['user']}\n"
                formatted_history += f"ASSISTANT: {turn['assistant']}\n"

        prompt = (
            f"{self.cot_prompts['profile_extraction']}\n"
            "Conversation history:\n"
            f"{formatted_history}\n\n"
            "Extract user profile as JSON with the schema provided."
        )

        model = genai.GenerativeModel(self.model_name)
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=schema,
            ),
        )

        try:
            # Parse the JSON response
            data = json.loads(response.text)
            return UserProfile(**data)
        except Exception as e:
            print(f"Profile extraction error: {e}")
            return None

    # ------------ weekly diet plan creation ------------

    def create_diet_plan(self, user_profile: UserProfile) -> Optional[WeeklyDietPlan]:
        prompt = (
            f"{self.cot_prompts['meal_planning']}\n\n"
            "User profile:\n"
            f"{user_profile.model_dump_json(indent=2)}\n\n"
            "Create a realistic, budget-aware weekly diet plan with Indian options when possible. "
            "Use the JSON schema exactly."
        )

        model = genai.GenerativeModel(self.model_name)
        resp = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=WeeklyDietPlan,
            ),
        )

        try:
            data = json.loads(resp.text)
            return WeeklyDietPlan(**data)
        except Exception as e:
            print("Plan parse error:", e)
            return None
