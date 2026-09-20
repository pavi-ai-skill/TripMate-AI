import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
    OPENWEATHER_BASE_URL = os.getenv("OPENWEATHER_BASE_URL")
    AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
    AVIATIONSTACK_BASE_URL = os.getenv("AVIATIONSTACK_BASE_URL")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    @classmethod
    def validate(cls):
        required_keys = {
            "TAVILY_API_KEY": cls.TAVILY_API_KEY,
            "OPENWEATHER_API_KEY": cls.OPENWEATHER_API_KEY,
            "OPENWEATHER_BASE_URL": cls.OPENWEATHER_BASE_URL,
            "AVIATIONSTACK_API_KEY": cls.AVIATIONSTACK_API_KEY,
            "AVIATIONSTACK_BASE_URL": cls.AVIATIONSTACK_BASE_URL,
            "GROQ_API_KEY": cls.GROQ_API_KEY
        }
        for name, value in required_keys.items():
            if not value:
                raise ValueError(f"{name} environment variable is missing or empty in your .env file.")