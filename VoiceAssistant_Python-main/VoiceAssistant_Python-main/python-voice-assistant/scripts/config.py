"""
Configuration file for the Voice Assistant
"""

import os
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class VoiceConfig:
    """Voice recognition and TTS configuration"""
    recognition_timeout: int = 5
    phrase_time_limit: int = 10
    tts_rate: int = 150
    tts_volume: float = 0.9
    wake_word: str = "hello assistant"

@dataclass
class APIConfig:
    """API keys and endpoints configuration"""
    weather_api_key: str = os.getenv('WEATHER_API_KEY', '')
    weather_api_url: str = "http://api.openweathermap.org/data/2.5/weather"
    
    # Email configuration
    email_smtp_server: str = "smtp.gmail.com"
    email_smtp_port: int = 587
    email_address: str = os.getenv('EMAIL_ADDRESS', '')
    email_password: str = os.getenv('EMAIL_PASSWORD', '')

@dataclass
class UserPreferences:
    """User-specific preferences"""
    name: str = "User"
    default_location: str = "New York"
    preferred_units: str = "metric"  # metric or imperial
    time_format: str = "12"  # 12 or 24 hour
    language: str = "en-US"

class AssistantConfig:
    """Main configuration class"""
    
    def __init__(self):
        self.voice = VoiceConfig()
        self.api = APIConfig()
        self.user = UserPreferences()
        
        # Load custom settings if available
        self.load_user_config()
    
    def load_user_config(self):
        """Load user configuration from file"""
        try:
            import json
            config_file = "user_config.json"
            
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config_data = json.load(f)
                
                # Update user preferences
                if 'user' in config_data:
                    for key, value in config_data['user'].items():
                        if hasattr(self.user, key):
                            setattr(self.user, key, value)
                
                # Update voice settings
                if 'voice' in config_data:
                    for key, value in config_data['voice'].items():
                        if hasattr(self.voice, key):
                            setattr(self.voice, key, value)
                            
        except Exception as e:
            print(f"Could not load user config: {e}")
    
    def save_user_config(self):
        """Save current configuration to file"""
        try:
            import json
            
            config_data = {
                'user': {
                    'name': self.user.name,
                    'default_location': self.user.default_location,
                    'preferred_units': self.user.preferred_units,
                    'time_format': self.user.time_format,
                    'language': self.user.language
                },
                'voice': {
                    'recognition_timeout': self.voice.recognition_timeout,
                    'phrase_time_limit': self.voice.phrase_time_limit,
                    'tts_rate': self.voice.tts_rate,
                    'tts_volume': self.voice.tts_volume,
                    'wake_word': self.voice.wake_word
                }
            }
            
            with open("user_config.json", 'w') as f:
                json.dump(config_data, f, indent=2)
                
            print("Configuration saved successfully!")
            
        except Exception as e:
            print(f"Could not save config: {e}")

# Default configuration instance
config = AssistantConfig()
