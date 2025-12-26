from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class ActivityLevel(str, Enum):
    """User activity level enumeration"""
    SEDENTARY = "sedentary"
    LIGHTLY_ACTIVE = "lightly_active"
    MODERATELY_ACTIVE = "moderately_active"
    VERY_ACTIVE = "very_active"
    EXTREMELY_ACTIVE = "extremely_active"

class Goal(str, Enum):
    """User health goals enumeration"""
    WEIGHT_LOSS = "weight_loss"
    WEIGHT_GAIN = "weight_gain"
    MAINTENANCE = "maintenance"
    MUSCLE_GAIN = "muscle_gain"
    GENERAL_HEALTH = "general_health"

class DietaryRestriction(str, Enum):
    """Dietary restrictions enumeration"""
    NONE = "none"
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    GLUTEN_FREE = "gluten_free"
    DAIRY_FREE = "dairy_free"
    NUT_FREE = "nut_free"
    LOW_CARB = "low_carb"
    KETO = "keto"
    PALEO = "paleo"

class MealTime(str, Enum):
    """Meal times enumeration"""
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACKS = "snacks"

class NutritionInfo(BaseModel):
    """Nutritional information for a meal"""
    calories: int
    protein: float
    carbs: float
    fat: float

class WeeklySummary(BaseModel):
    """Summary of the weekly diet plan"""
    total_calories: int
    avg_protein: float
    avg_carbs: float
    avg_fat: float

class DailyRoutine(BaseModel):
    """User's daily routine"""
    wake_time: str = Field(description="Time user wakes up, e.g. '7:00 AM'")
    bed_time: str = Field(description="Time user goes to bed, e.g. '11:00 PM'")
    work_schedule: str = Field(description="Work hours, e.g. '9-5'")

class UserProfile(BaseModel):
    """User profile information extracted from conversation"""
    name: str = Field(description="User's name")
    age: int = Field(description="User's age in years")
    gender: str = Field(description="User's gender")
    height_cm: float = Field(description="User's height in centimeters")
    weight_kg: float = Field(description="User's current weight in kilograms")
    target_weight_kg: Optional[float] = Field(description="User's target weight in kilograms")
    activity_level: ActivityLevel = Field(description="User's activity level")
    goal: Goal = Field(description="User's primary health goal")
    dietary_restrictions: List[DietaryRestriction] = Field(description="List of dietary restrictions")
    allergies: List[str] = Field(description="List of food allergies")
    preferences: List[str] = Field(description="List of food preferences and likes")
    dislikes: List[str] = Field(description="List of foods user dislikes")
    daily_routine: DailyRoutine = Field(description="User's daily routine and schedule")
    cooking_skill: str = Field(description="User's cooking skill level")
    budget_constraint: Optional[str] = Field(description="Budget constraints for food")
    cultural_preferences: List[str] = Field(description="Cultural food preferences")

class MealPlan(BaseModel):
    """Individual meal plan structure"""
    meal_time: MealTime
    meal_name: str
    description: str
    ingredients: List[str]
    instructions: List[str]
    nutrition_info: NutritionInfo
    prep_time: str
    cooking_time: str
    difficulty: str

class DailyPlan(BaseModel):
    """Daily meal plan structure"""
    day: str
    meals: List[MealPlan]
    total_calories: int
    total_protein: float
    total_carbs: float
    total_fat: float
    notes: Optional[str]

class WeeklyDietPlan(BaseModel):
    """Complete weekly diet plan"""
    user_profile: UserProfile
    daily_plans: List[DailyPlan]
    weekly_summary: WeeklySummary
    recommendations: List[str]
    shopping_list: List[str]
    created_date: str
