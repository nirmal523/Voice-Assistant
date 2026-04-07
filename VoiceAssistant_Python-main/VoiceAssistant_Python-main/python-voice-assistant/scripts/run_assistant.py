"""
Main runner script for the Voice Assistant with enhanced error handling
"""

import sys
import os
from voice_assistant import VoiceAssistant
from config import config

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = [
        'speech_recognition',
        'pyttsx3',
        'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Missing required packages:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nPlease install them using:")
        print("python setup_requirements.py")
        return False
    
    return True

def setup_environment():
    """Setup environment variables and configuration"""
    print("Voice Assistant Setup")
    print("=" * 30)
    
    # Check for API keys
    if not config.api.weather_api_key:
        print("⚠ Weather API key not found.")
        print("To enable weather features, get a free API key from:")
        print("https://openweathermap.org/api")
        print("Then set the environment variable: WEATHER_API_KEY")
        print()
    
    if not config.api.email_address or not config.api.email_password:
        print("⚠ Email configuration not found.")
        print("To enable email features, set these environment variables:")
        print("EMAIL_ADDRESS - your email address")
        print("EMAIL_PASSWORD - your email app password")
        print()
    
    # User preferences setup
    if config.user.name == "User":
        name = input("What's your name? (press Enter to skip): ").strip()
        if name:
            config.user.name = name
    
    location = input(f"What's your default location? (current: {config.user.default_location}): ").strip()
    if location:
        config.user.default_location = location
    
    # Save configuration
    config.save_user_config()
    
    print(f"\nHello {config.user.name}! Your assistant is ready.")
    print("=" * 30)

def main():
    """Main function to run the voice assistant"""
    print("Python Voice Assistant")
    print("=" * 30)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Setup environment
    try:
        setup_environment()
    except KeyboardInterrupt:
        print("\nSetup cancelled.")
        return
    
    # Start the assistant
    try:
        assistant = VoiceAssistant()
        
        # Apply user configuration
        assistant.user_name = config.user.name
        assistant.wake_word = config.voice.wake_word
        
        print("\nStarting voice assistant...")
        print("Say 'help' for available commands or 'exit' to quit.")
        print("Press Ctrl+C to stop at any time.")
        print()
        
        assistant.run()
        
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"Error starting assistant: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure your microphone is working")
        print("2. Check your internet connection")
        print("3. Ensure all packages are installed correctly")

if __name__ == "__main__":
    main()
