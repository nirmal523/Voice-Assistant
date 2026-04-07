import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import threading
import time

class VoiceAssistant:
    def __init__(self):
        # Initialize speech recognition and text-to-speech
        self.recognizer = sr.Recognizer()
        try:
            self.microphone = sr.Microphone()
        except OSError as e:
            print(f"Microphone not found or not accessible: {e}")
            self.microphone = None
        self.tts_engine = pyttsx3.init()
        
        # Configure TTS settings
        self.tts_engine.setProperty('rate', 150)
        self.tts_engine.setProperty('volume', 0.9)
        
        # User preferences
        self.user_name = "User"
        self.wake_word = "hello assistant"
        
        # API keys (you would set these as environment variables)
        self.weather_api_key = os.getenv('WEATHER_API_KEY')
        if not self.weather_api_key:
            print("Warning: WEATHER_API_KEY environment variable not set.")
            self.weather_api_key = None
        
        self.email_password = os.getenv('EMAIL_PASSWORD')
        if not self.email_password:
            print("Warning: EMAIL_PASSWORD environment variable not set.")
            self.email_password = None
        
        print("Voice Assistant initialized successfully!")
        self.speak("Hello! I'm your voice assistant. How can I help you today?")

    def speak(self, text):
        """Convert text to speech"""
        try:
            print(f"Assistant: {text}")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"Error in text-to-speech: {e}")

    def listen(self):
        """Listen for voice commands"""
        try:
            with self.microphone as source:
                print("Listening...")
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                # Listen for audio
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            # Recognize speech using Google's speech recognition
            command = self.recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
            
        except sr.WaitTimeoutError:
            print("Listening timeout")
            return ""
        except sr.UnknownValueError:
            print("Could not understand audio")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return ""

    def get_current_time(self):
        """Get current time"""
        now = datetime.datetime.now()
        time_string = now.strftime("%I:%M %p")
        return f"The current time is {time_string}"

    def get_current_date(self):
        """Get current date"""
        today = datetime.date.today()
        date_string = today.strftime("%B %d, %Y")
        return f"Today's date is {date_string}"

    def search_web(self, query):
        """Search the web using default browser"""
        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            return f"Searching the web for {query}"
        except Exception as e:
            return f"Error searching the web: {e}"

    def get_weather(self, city="New York"):
        """Get weather information (requires API key)"""
        try:
            if self.weather_api_key == 'your_weather_api_key':
                return "Weather API key not configured. Please set your OpenWeatherMap API key."
            
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_api_key}&units=metric"
            response = requests.get(url, timeout=5)
            data = response.json()
            
            if response.status_code == 200:
                temp = data['main']['temp']
                description = data['weather'][0]['description']
                return f"The weather in {city} is {description} with a temperature of {temp} degrees Celsius"
            else:
                return f"Could not get weather information for {city}"
                
        except Exception as e:
            return f"Error getting weather: {e}"

    def send_email(self, recipient, subject, body):
        """Send email (requires email configuration)"""
        import smtplib
        from smtplib import SMTPException, SMTPAuthenticationError, SMTPConnectError, SMTPRecipientsRefused
        try:
            if not self.email_password:
                return "Email configuration not set up. Please configure your email credentials."
            
            # Email configuration (Gmail example)
            sender_email = "your_email@gmail.com"
            
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = recipient
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))
            
            # Gmail SMTP configuration
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, self.email_password)
            server.send_message(message)
            server.quit()
            
            return f"Email sent successfully to {recipient}"
            
        except SMTPAuthenticationError:
            return "SMTP Authentication Error: Check your email and password."
        except SMTPConnectError:
            return "SMTP Connection Error: Unable to connect to the SMTP server."
        except SMTPRecipientsRefused:
            return "SMTP Recipients Refused: The recipient address was rejected."
        except SMTPException as e:
            return f"SMTP error occurred: {e}"
        except Exception as e:
            return f"Error sending email: {e}"

    def set_reminder(self, message, delay_minutes):
        """Set a reminder (simple implementation)"""
        def reminder_thread():
            time.sleep(delay_minutes * 60)
            self.speak(f"Reminder: {message}")
            print(f"REMINDER: {message}")
        
        thread = threading.Thread(target=reminder_thread)
        thread.daemon = True
        thread.start()
        
        return f"Reminder set for {delay_minutes} minutes: {message}"

    def parse_reminder_command(self, command):
        """Parse reminder command to extract message and delay in minutes"""
        import re
        try:
            # Example formats:
            # "remind me to call mom in 10 minutes"
            # "remind me in 5 minutes to check email"
            pattern1 = r"remind me to (.+) in (\d+) minute"
            pattern2 = r"remind me in (\d+) minute(?:s)? to (.+)"
            
            match = re.search(pattern1, command)
            if match:
                message = match.group(1).strip()
                delay = int(match.group(2))
                return message, delay
            
            match = re.search(pattern2, command)
            if match:
                delay = int(match.group(1))
                message = match.group(2).strip()
                return message, delay
            
            return None, None
        except Exception as e:
            print(f"Error parsing reminder command: {e}")
            return None, None

    def process_command(self, command):
        """Process voice commands using natural language understanding"""
        if not command:
            return
        
        # Basic greetings
        if any(word in command for word in ['hello', 'hi', 'hey']):
            responses = [
                f"Hello {self.user_name}! How can I help you?",
                "Hi there! What can I do for you?",
                "Hey! I'm here to assist you."
            ]
            import random
            self.speak(random.choice(responses))
        
        # Time queries
        elif any(word in command for word in ['time', 'clock']):
            response = self.get_current_time()
            self.speak(response)
        
        # Date queries
        elif any(word in command for word in ['date', 'today']):
            response = self.get_current_date()
            self.speak(response)
        
        # Web search
        elif 'search' in command or 'google' in command:
            # Extract search query
            if 'search for' in command:
                query = command.split('search for', 1)[1].strip()
            elif 'google' in command:
                query = command.split('google', 1)[1].strip()
            else:
                query = command.replace('search', '').strip()
            
            if query:
                response = self.search_web(query)
                self.speak(response)
            else:
                self.speak("What would you like me to search for?")
        
        # Weather queries
        elif 'weather' in command:
            city = "New York"  # Default city
            if 'in' in command:
                parts = command.split('in')
                if len(parts) > 1:
                    city = parts[1].strip()
            
            response = self.get_weather(city)
            self.speak(response)
        
        # Email functionality
        elif 'send email' in command or 'email' in command:
            self.speak("Email functionality requires configuration. Please set up your email credentials.")
        
        # Reminder functionality
        elif 'remind me' in command or 'reminder' in command:
            message, minutes = self.parse_reminder_command(command)
            if message and minutes:
                response = self.set_reminder(message, minutes)
                self.speak(response)
            else:
                self.speak("I couldn't understand the reminder format. Try saying 'remind me to do something in 5 minutes'")
        
        # Exit commands
        elif any(word in command for word in ['exit', 'quit', 'goodbye', 'bye']):
            self.speak("Goodbye! Have a great day!")
            return False
        
        # Help command
        elif 'help' in command:
            help_text = """
            I can help you with:
            - Telling time and date
            - Searching the web
            - Getting weather information
            - Setting reminders
            - Basic conversation
            
            Try saying things like:
            'What time is it?'
            'Search for Python tutorials'
            'What's the weather like?'
            'Remind me to call mom in 30 minutes'
            """
            self.speak("Here's what I can do for you:")
            print(help_text)
        
        # Unknown command
        else:
            responses = [
                "I'm not sure how to help with that. Try saying 'help' to see what I can do.",
                "I didn't understand that command. Can you try rephrasing?",
                "Sorry, I don't know how to do that yet. Say 'help' for available commands."
            ]
            import random
            self.speak(random.choice(responses))
        
        return True

    def run(self):
        """Main loop for the voice assistant"""
        print("Voice Assistant is running. Say 'help' for available commands or 'exit' to quit.")
        
        while True:
            try:
                command = self.listen()
                if command:
                    should_continue = self.process_command(command)
                    if should_continue is False:
                        break
                
            except KeyboardInterrupt:
                print("\nShutting down...")
                self.speak("Goodbye!")
                break
            except Exception as e:
                print(f"Error in main loop: {e}")
                self.speak("Sorry, I encountered an error. Please try again.")

def main():
    """Main function to start the voice assistant"""
    try:
        assistant = VoiceAssistant()
        assistant.run()
    except Exception as e:
        print(f"Failed to start voice assistant: {e}")
        print("Make sure you have the required packages installed:")
        print("pip install speechrecognition pyttsx3 requests")

    print("If you encounter issues with microphone or audio, please check your device settings and permissions.")

if __name__ == "__main__":
    main()
