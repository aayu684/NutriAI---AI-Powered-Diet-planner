import streamlit as st
import os
from datetime import datetime
from typing import List, Dict, Any
import json

from config import Config
from ai_dietitian import AIDietitian
from pdf_generator import DietPlanPDFGenerator
from models import UserProfile, WeeklyDietPlan, ActivityLevel, Goal, DietaryRestriction, DailyRoutine

# Page configuration
st.set_page_config(
    page_title="AI Diet Planner",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling and dark theme
st.markdown("""
<style>
    /* Main app background */
    .stApp {
        background-color: #1a1b2e;
        color: #ffffff;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #151625;
        border-right: 1px solid #2a2b3d;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #ffffff !important;
    }
    
    /* Custom headers for sections */
    .section-header {
        color: #00e5ff;
        font-size: 1.2rem;
        font-weight: 600;
        margin-top: 1rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Input fields styling */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #13141f !important;
        color: #ffffff !important;
        border: 1px solid #2a2b3d !important;
        border-radius: 8px !important;
    }
    
    /* Labels */
    .stMarkdown label, .stTextInput label, .stNumberInput label, .stSelectbox label {
        color: #a0a0b0 !important;
        font-size: 0.9rem !important;
    }
    
    /* Chat messages */
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        color: #ffffff;
    }
    .user-message {
        background-color: #2a2b3d;
        border-left: 4px solid #00e5ff;
    }
    .assistant-message {
        background-color: #1f2033;
        border-left: 4px solid #9c27b0;
    }
    
    /* Metrics */
    div[data-testid="stMetricValue"] {
        color: #00e5ff !important;
    }
    
    /* Buttons */
    .stButton button {
        background-color: #00e5ff !important;
        color: #000000 !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        opacity: 0.8;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = None
    
    if 'diet_plan' not in st.session_state:
        st.session_state.diet_plan = None
    
    if 'conversation_complete' not in st.session_state:
        st.session_state.conversation_complete = False

def display_chat_message(role: str, content: str):
    """Display a chat message with appropriate styling"""
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>You:</strong><br>{content}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>Your AI nutritionist:</strong><br>{content}
        </div>
        """, unsafe_allow_html=True)

def display_user_profile(profile: UserProfile):
    """Display the extracted user profile"""
    st.subheader("📋 Your Profile Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Name:** {profile.name}")
        st.write(f"**Age:** {profile.age} years")
        st.write(f"**Gender:** {profile.gender}")
        st.write(f"**Height:** {profile.height_cm} cm")
        st.write(f"**Current Weight:** {profile.weight_kg} kg")
    
    with col2:
        if profile.target_weight_kg:
            st.write(f"**Target Weight:** {profile.target_weight_kg} kg")
        # Safely get string values from Enums or strings
        goal_val = getattr(profile.goal, 'value', profile.goal)
        activity_val = getattr(profile.activity_level, 'value', profile.activity_level)
        st.write(f"**Goal:** {str(goal_val).replace('_', ' ').title()}")
        st.write(f"**Activity Level:** {str(activity_val).replace('_', ' ').title()}")
        st.write(f"**Cooking Skill:** {profile.cooking_skill}")
    
    # Convert enum lists to string lists where necessary
    def stringify_list(items):
        if not items:
            return []
        return [getattr(i, 'value', str(i)) for i in items]

    dietary = stringify_list(profile.dietary_restrictions)
    if dietary and dietary != ["none"]:
        st.write(f"**Dietary Restrictions:** {', '.join(dietary)}")

    allergies = stringify_list(profile.allergies)
    if allergies:
        st.write(f"**Allergies:** {', '.join(allergies)}")

    prefs = stringify_list(profile.preferences)
    if prefs:
        st.write(f"**Food Preferences:** {', '.join(prefs)}")

def display_diet_plan_summary(plan: WeeklyDietPlan):
    """Display a summary of the generated diet plan"""
    st.subheader("🍽️ Your Weekly Diet Plan")
    
    # Weekly overview
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Calories", f"{plan.weekly_summary.total_calories}")
    with col2:
        st.metric("Avg Protein", f"{plan.weekly_summary.avg_protein}g")
    with col3:
        st.metric("Avg Carbs", f"{plan.weekly_summary.avg_carbs}g")
    with col4:
        st.metric("Avg Fat", f"{plan.weekly_summary.avg_fat}g")
    
    # Daily plans
    st.subheader("📅 Daily Meal Plans")
    for daily_plan in plan.daily_plans:
        with st.expander(f"{daily_plan.day} - {daily_plan.total_calories} calories"):
            for meal in daily_plan.meals:
                st.write(f"**{meal.meal_time.title()}:** {meal.meal_name}")
                st.write(f"*{meal.description}*")
                st.write(f"Calories: {meal.nutrition_info.calories} | "
                        f"Protein: {meal.nutrition_info.protein}g | "
                        f"Carbs: {meal.nutrition_info.carbs}g | "
                        f"Fat: {meal.nutrition_info.fat}g")
                st.write("---")
    
    # Shopping list
    if plan.shopping_list:
        st.subheader("🛒 Shopping List")
        shopping_text = "• " + "\n• ".join(plan.shopping_list)
        st.text_area("Items to buy:", shopping_text, height=150, disabled=True)
    
    # Recommendations
    if plan.recommendations:
        st.subheader("💡 Personalized Recommendations")
        for i, rec in enumerate(plan.recommendations, 1):
            st.write(f"{i}. {rec}")

def main():
    """Main application function"""
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🥗 NutriAI - Diet planner</h1>', unsafe_allow_html=True)
    st.markdown("### Meet Your AI nutritionist")
    
    # Sidebar Form
    with st.sidebar:
        st.markdown('<div class="section-header">👤 User Profile</div>', unsafe_allow_html=True)
        
        # Name field (hidden in image but needed for profile)
        name = st.text_input("Name", value="User", key="profile_name")
        
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=1, max_value=120, value=25, step=1, key="profile_age")
        with col2:
            height = st.number_input("Height (cm)", min_value=50, max_value=300, value=170, step=1, key="profile_height")
            
        col3, col4 = st.columns(2)
        with col3:
            weight = st.number_input("Weight (kg)", min_value=20, max_value=500, value=70, step=1, key="profile_weight")
        with col4:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="profile_gender")

        st.markdown('<div class="section-header">🎯 Goals & Lifestyle</div>', unsafe_allow_html=True)
        
        activity_level = st.selectbox(
            "Activity Level",
            [e.value for e in ActivityLevel],
            format_func=lambda x: x.replace('_', ' ').title(),
            key="profile_activity"
        )
        
        primary_goal = st.selectbox(
            "Primary Goal",
            [e.value for e in Goal],
            format_func=lambda x: x.replace('_', ' ').title(),
            key="profile_goal"
        )

        st.markdown('<div class="section-header">🥗 Preferences</div>', unsafe_allow_html=True)
        
        diet_type = st.selectbox(
            "Diet Type",
            [e.value for e in DietaryRestriction],
            format_func=lambda x: x.replace('_', ' ').title(),
            key="profile_diet"
        )
        
        # Additional fields needed for UserProfile but not in image
        with st.expander("Advanced Details"):
            cooking_skill = st.selectbox("Cooking Skill", ["Beginner", "Intermediate", "Advanced"], index=1)
            allergies = st.multiselect("Allergies", ["Nuts", "Dairy", "Eggs", "Soy", "Shellfish", "Wheat"])
            
        # Create UserProfile object from inputs
        current_profile = UserProfile(
            name=name,
            age=age,
            gender=gender,
            height_cm=height,
            weight_kg=weight,
            target_weight_kg=None, # Let AI determine or ask based on goal
            activity_level=ActivityLevel(activity_level),
            goal=Goal(primary_goal),
            dietary_restrictions=[DietaryRestriction(diet_type)],
            allergies=allergies,
            preferences=[],
            dislikes=[],
            daily_routine=DailyRoutine(wake_time="7:00 AM", bed_time="11:00 PM", work_schedule="9-5"),
            cooking_skill=cooking_skill,
            budget_constraint="Medium",
            cultural_preferences=[]
        )
        
        # Update session state
        st.session_state.user_profile = current_profile
    
    # Main content area
    # Main content area
    st.subheader("📋 Your Diet Plan Dashboard")
    
    # Display current profile summary
    if st.session_state.user_profile:
        with st.expander("View Current Profile", expanded=False):
            display_user_profile(st.session_state.user_profile)

    # Generate Button
    if st.button("✨ Generate My Diet Plan", type="primary", use_container_width=True):
        try:
            ai_dietitian = AIDietitian()
            with st.spinner("Creating your personalized diet plan based on your profile..."):
                # Use the profile directly from session state (populated by sidebar)
                plan = ai_dietitian.create_diet_plan(st.session_state.user_profile)
                
                if plan:
                    st.session_state.diet_plan = plan
                    st.success("✅ Diet plan generated successfully!")
                else:
                    st.error("❌ Could not generate diet plan. Please try again.")
        except Exception as e:
            st.error(f"Error generating plan: {str(e)}")

    # Display Results
    if st.session_state.diet_plan:
        st.markdown("---")
        display_diet_plan_summary(st.session_state.diet_plan)
        
        # PDF download
        st.markdown("---")
        st.subheader("📄 Download Your Diet Plan")
        
        if st.button("🔄 Generate PDF"):
            try:
                pdf_generator = DietPlanPDFGenerator()
                with st.spinner("Generating PDF..."):
                    pdf_path = pdf_generator.generate_diet_plan_pdf(st.session_state.diet_plan)
                    
                    # Read the PDF file
                    with open(pdf_path, "rb") as pdf_file:
                        pdf_bytes = pdf_file.read()
                    
                    # Create download button
                    st.download_button(
                        label="📥 Download PDF",
                        data=pdf_bytes,
                        file_name=f"diet_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf"
                    )
                    
                    # Clean up the temporary file
                    os.remove(pdf_path)
                    
            except Exception as e:
                st.error(f"Error generating PDF: {str(e)}")

if __name__ == "__main__":
    try:
        Config.validate()
        main()
    except ValueError as e:
        st.error(f"Configuration Error: {str(e)}")
        st.markdown("""
        Please set up your environment variables:
        1. Create a `.env` file in the project root
        2. Add your OpenAI API key: `OPENAI_API_KEY=your_key_here`
        3. Restart the application
        """)
    except Exception as e:
        st.error(f"Application Error: {str(e)}")
        st.markdown("Please check your configuration and try again.")
