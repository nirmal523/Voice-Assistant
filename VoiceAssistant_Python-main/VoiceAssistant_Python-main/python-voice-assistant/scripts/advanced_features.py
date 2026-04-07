import json
import re
from datetime import datetime, timedelta
import requests

class AdvancedVoiceAssistant:
    def __init__(self):
        self.user_preferences = {
            "name": "User",
            "location": "New York",
            "email": "",
            "smart_home_devices": []
        }
        self.conversation_history = []
        self.custom_commands = {}
    
    def natural_language_processing(self, text):
        """Basic NLP for intent recognition"""
        # Intent patterns
        intents = {
            "time_query": [r"what.*time", r"current time", r"time.*now"],
            "date_query": [r"what.*date", r"today.*date", r"current date"],
            "weather_query": [r"weather.*like", r"temperature.*today", r"forecast"],
            "search_query": [r"search.*for", r"look.*up", r"find.*information"],
            "email_intent": [r"send.*email", r"compose.*email", r"email.*to"],
            "reminder_intent": [r"remind.*me", r"set.*reminder", r"don't.*forget"],
            "smart_home": [r"turn.*on", r"turn.*off", r"dim.*lights", r"set.*temperature"]
        }
        
        # Extract entities
        entities = {
            "time_expressions": re.findall(r'\b(?:in\s+)?(\d+)\s+(minute|hour|day)s?\b', text),
            "email_addresses": re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text),
            "numbers": re.findall(r'\b\d+\b', text),
            "locations": self.extract_locations(text)
        }
        
        # Determine intent
        detected_intent = "unknown"
        for intent, patterns in intents.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    detected_intent = intent
                    break
            if detected_intent != "unknown":
                break
        
        return {
            "intent": detected_intent,
            "entities": entities,
            "original_text": text
        }
    
    def extract_locations(self, text):
        """Extract location names from text"""
        # Simple location extraction (in a real app, you'd use a proper NER model)
        common_cities = [
            "new york", "london", "paris", "tokyo", "sydney", "toronto",
            "los angeles", "chicago", "miami", "boston", "seattle"
        ]
        
        found_locations = []
        text_lower = text.lower()
        
        for city in common_cities:
            if city in text_lower:
                found_locations.append(city.title())
        
        return found_locations
    
    def smart_home_control(self, command):
        """Simulate smart home device control"""
        # This would integrate with actual smart home APIs like Philips Hue, Nest, etc.
        
        devices = {
            "lights": ["living room light", "bedroom light", "kitchen light"],
            "thermostat": ["temperature", "heating", "cooling"],
            "security": ["alarm", "camera", "door lock"]
        }
        
        command_lower = command.lower()
        
        if "turn on" in command_lower:
            if "light" in command_lower:
                return "Turning on the lights"
            elif "alarm" in command_lower:
                return "Activating security alarm"
        
        elif "turn off" in command_lower:
            if "light" in command_lower:
                return "Turning off the lights"
            elif "alarm" in command_lower:
                return "Deactivating security alarm"
        
        elif "set temperature" in command_lower:
            # Extract temperature value
            temp_match = re.search(r'(\d+)', command_lower)
            if temp_match:
                temp = temp_match.group(1)
                return f"Setting temperature to {temp} degrees"
        
        return "Smart home command not recognized"
    
    def personalized_responses(self, intent, entities):
        """Generate personalized responses based on user preferences and history"""
        user_name = self.user_preferences.get("name", "User")
        
        # Time-based greetings
        current_hour = datetime.now().hour
        if current_hour < 12:
            greeting = "Good morning"
        elif current_hour < 17:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"
        
        # Personalized responses based on intent
        if intent == "time_query":
            return f"{greeting} {user_name}! " + self.get_current_time()
        
        elif intent == "weather_query":
            location = entities.get("locations", [self.user_preferences["location"]])[0]
            return f"Let me check the weather in {location} for you, {user_name}."
        
        return f"How can I help you today, {user_name}?"
    
    def add_custom_command(self, trigger_phrase, response):
        """Allow users to add custom commands"""
        self.custom_commands[trigger_phrase.lower()] = response
        return f"Custom command added: '{trigger_phrase}' will now respond with '{response}'"
    
    def handle_custom_commands(self, command):
        """Check for and handle custom commands"""
        command_lower = command.lower()
        
        for trigger, response in self.custom_commands.items():
            if trigger in command_lower:
                return response
        
        return None
    
    def conversation_context(self, current_input):
        """Maintain conversation context for better responses"""
        # Add current input to history
        self.conversation_history.append({
            "timestamp": datetime.now(),
            "input": current_input,
            "type": "user"
        })
        
        # Keep only last 10 interactions for context
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
        
        # Analyze context for follow-up questions
        if len(self.conversation_history) >= 2:
            last_interaction = self.conversation_history[-2]
            
            # Handle follow-up questions
            if "weather" in last_interaction.get("input", "").lower():
                if any(word in current_input.lower() for word in ["tomorrow", "next", "later"]):
                    return "weather_followup"
        
        return None
    
    def privacy_filter(self, text):
        """Filter sensitive information from logs and responses"""
        # Remove potential sensitive information
        filtered_text = text
        
        # Remove email addresses from logs
        filtered_text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 
                              '[EMAIL_REDACTED]', filtered_text)
        
        # Remove phone numbers
        filtered_text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', 
                              '[PHONE_REDACTED]', filtered_text)
        
        # Remove potential credit card numbers
        filtered_text = re.sub(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b', 
                              '[CARD_REDACTED]', filtered_text)
        
        return filtered_text
    
    def get_current_time(self):
        """Get current time with enhanced formatting"""
        now = datetime.now()
        time_string = now.strftime("%I:%M %p")
        date_string = now.strftime("%A, %B %d")
        return f"It's {time_string} on {date_string}"

def main():
    """Demonstrate advanced features"""
    assistant = AdvancedVoiceAssistant()
    
    print("Advanced Voice Assistant Features Demo")
    print("=" * 40)
    
    # Test NLP
    test_commands = [
        "What's the weather like in Paris?",
        "Remind me to call mom in 30 minutes",
        "Turn on the living room lights",
        "Send an email to john@example.com"
    ]
    
    for command in test_commands:
        print(f"\nInput: {command}")
        nlp_result = assistant.natural_language_processing(command)
        print(f"Intent: {nlp_result['intent']}")
        print(f"Entities: {nlp_result['entities']}")
    
    # Test custom commands
    assistant.add_custom_command("tell me a joke", "Why don't scientists trust atoms? Because they make up everything!")
    print(f"\nCustom command test: {assistant.handle_custom_commands('tell me a joke')}")
    
    # Test smart home
    print(f"\nSmart home test: {assistant.smart_home_control('turn on the lights')}")

if __name__ == "__main__":
    main()
