import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    # Use Gemini 2.5 Flash
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    APP_TITLE = os.getenv("APP_TITLE", "Gemini AI Diet Planner")
    APP_DESCRIPTION = os.getenv("APP_DESCRIPTION", "Personalized diet planning with Gemini 2.5 Flash")

    PDF_FONT_SIZE = 12
    PDF_MARGIN = 50
    PDF_LINE_HEIGHT = 20

    @classmethod
    def validate(cls):
        if not cls.GEMINI_API_KEY:
            load_dotenv()
            cls.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        return True
