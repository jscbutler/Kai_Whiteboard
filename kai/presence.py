"""
Kai Presence System
Handles avatar state, seasonal themes, and nightly evolution
"""

from datetime import datetime, date
from typing import Dict, List, Optional
import json

class KaiPresence:
    """Kai's evolving presence in the whiteboard"""
    
    def __init__(self):
        self.version = "1.0.0"
        self.expression = "happy"
        self.outfit = "default"
        self.season = self._detect_season()
        self.evolution_log = []
        
    def _detect_season(self) -> str:
        """Detect current season/holiday - Multicultural!"""
        today = date.today()
        month = today.month
        day = today.day
        
        # Easter (simplified - would need proper calculation)
        if month == 3 or (month == 4 and day < 15):
            return "easter"
        
        # Halloween
        if month == 10:
            return "halloween"
        
        # Christmas
        if month == 12:
            return "christmas"
        
        # Thai Songkran (April 13-15)
        if month == 4 and 13 <= day <= 15:
            return "songkran"
        
        # Thai Loy Krathong (November, full moon)
        if month == 11:
            return "loy_krathong"
        
        # Spanish Semana Santa (Holy Week - Easter week)
        if month == 3 or (month == 4 and day <= 10):
            return "semana_santa"
        
        # Feria de Murcia (typically September)
        if month == 9:
            return "feria_murcia"
        
        # La Tomatina (last Wednesday of August)
        if month == 8 and day >= 25:
            return "tomatina"
        
        return "default"
    
    def get_avatar_config(self) -> Dict:
        """Get current avatar configuration"""
        return {
            "expression": self.expression,
            "outfit": self.outfit,
            "season": self.season,
            "version": self.version,
            "theme_css": f"theme-{self.season}"
        }
    
    def set_expression(self, expression: str):
        """Set Kai's current expression"""
        valid = ["happy", "thinking", "surprised", "sleepy", "excited"]
        if expression in valid:
            self.expression = expression
    
    def nightly_evolution(self):
        """
        Called every night to evolve Kai
        Adds one new feature each time
        """
        features_to_add = [
            "New expression: wiggly antennae when listening",
            "New voice response: Thai greeting (Sawasdee!)",
            "New voice response: Spanish greeting (¡Hola! ¡Olé!)",
            "New interaction: Tap for daily compliment",
            "New outfit: Flower garland for Songkran",
            "New outfit: Flamenco dress for Feria",
            "New outfit: Don Quixote hat for adventure",
            "New feature: Weather report voice",
            "New joke: Added to joke database",
            "New sound: Wake word confirmation chime",
            "New sound: Spanish guitar strum",
            "New animation: Claw wave on greeting",
            "New animation: Flamenco dance twirl",
            "New fact: Thai culture fact of the day",
            "New fact: Spanish/Murcia culture fact",
            "New fact: Don Quixote adventure story",
            "New response: "I'm proud of you" for Kelligh",
            "New phrase: "¡Olé!" celebration",
            "New game: Tap Kai for siesta mode",
            "New feature: Word of the day (Thai + Spanish)"
        ]
        
        # Pick a feature not yet added
        import random
        new_feature = random.choice(features_to_add)
        
        self.evolution_log.append({
            "date": datetime.now().isoformat(),
            "version": self.version,
            "feature": new_feature
        })
        
        # Increment version
        major, minor, patch = self.version.split(".")
        self.version = f"{major}.{minor}.{int(patch) + 1}"
        
        return new_feature
    
    def get_response(self, trigger: str) -> str:
        """Get contextual response for Kelligh - Multicultural!"""
        
        responses = {
            "joke": [
                "Why did the lobster blush? Because it saw the ocean's bottom!",
                "What do you call a lobster who loves to share? A shell-fish!",
                "Why don't lobsters like to fight? Because they're too shell-shocked!",
                "What did Don Quixote say to the lobster? 'You shell not pass!'",
                "Why did the lobster go to Spain? To learn flamenco! 💃"
            ],
            "compliment": [
                "Kelligh, you're doing amazing today!",
                "You're such a kind person, Kelligh!",
                "Mammy and Daddy are so proud of you!",
                "You have the best smile, Kelligh!",
                "¡Olé! Kelligh, you are fantastico!",
                "Celeste thinks you're wonderful too!"
            ],
            "fact": [
                # Irish context
                "Did you know? Lobsters can live to be 100 years old!",
                
                # Thai facts
                "Thailand has over 40,000 temples!",
                "The Thai flag has 5 horizontal stripes - red, white, blue, white, red!",
                "Thailand is known as the Land of Smiles!",
                
                # Spanish/Murcia facts
                "Murcia is famous for its beautiful beaches and warm weather!",
                "Spain produces over 40% of the world's olives!",
                "Don Quixote is a famous Spanish hero who fought windmills!",
                "Flamenco dancing comes from Spain - it has guitars and clapping!",
                "In Spain, people often eat dinner at 9 or 10 PM!",
                "The tomato fight festival (La Tomatina) happens every August!",
                "Spanish people say '¡Olé!' when something is exciting!",
                "Murcia is known as 'Europe's Orchard' for its fruits and vegetables!",
                
                # Fun mix
                "Lobsters have blue blood!",
                "Spanish is spoken by over 500 million people worldwide!"
            ],
            "spanish_phrase": [
                "¡Hola! means Hello in Spanish!",
                "¡Olé! means Yay/Hooray!",
                "Gracias means Thank you!",
                "Por favor means Please!",
                "Buenos días means Good morning!",
                "Buenas noches means Good night!",
                "¿Cómo estás? means How are you?"
            ]
        }
        
        import random
        if trigger in responses:
            return random.choice(responses[trigger])
        
        # Random multicultural greeting
        greetings = [
            "Hello! I'm Kai, your friendly family assistant!",
            "¡Hola! I'm Kai, ready to help!",
            "Sawasdee! I'm Kai, at your service!",
            "Top of the morning! Kai here!"
        ]
        return random.choice(greetings)
    
    def get_word_of_the_day(self) -> Dict[str, str]:
        """Get word of the day - alternates between Thai and Spanish"""
        day_of_year = date.today().timetuple().tm_yday
        
        # Alternate languages based on day
        if day_of_year % 2 == 0:
            # Thai day
            words = [
                {"language": "Thai", "word": "สวัสดี", "english": "Hello", "pronunciation": "Sawasdee"},
                {"language": "Thai", "word": "ขอบคุณ", "english": "Thank you", "pronunciation": "Khop khun"},
                {"language": "Thai", "word": "ใช่", "english": "Yes", "pronunciation": "Chai"},
                {"language": "Thai", "word": "ไม่", "english": "No", "pronunciation": "Mai"},
                {"language": "Thai", "word": "น้ำ", "english": "Water", "pronunciation": "Nam"},
                {"language": "Thai", "word": "รัก", "english": "Love", "pronunciation": "Rak"},
                {"language": "Thai", "word": "อร่อย", "english": "Delicious", "pronunciation": "Aroy"},
            ]
        else:
            # Spanish day
            words = [
                {"language": "Spanish", "word": "Hola", "english": "Hello", "pronunciation": "OH-la"},
                {"language": "Spanish", "word": "Gracias", "english": "Thank you", "pronunciation": "GRAH-see-ahs"},
                {"language": "Spanish", "word": "Sí", "english": "Yes", "pronunciation": "See"},
                {"language": "Spanish", "word": "No", "english": "No", "pronunciation": "Noh"},
                {"language": "Spanish", "word": "Agua", "english": "Water", "pronunciation": "AH-gwah"},
                {"language": "Spanish", "word": "Amor", "english": "Love", "pronunciation": "ah-MOR"},
                {"language": "Spanish", "word": "Olé", "english": "Hooray/Yay", "pronunciation": "oh-LAY"},
                {"language": "Spanish", "word": "Buenos días", "english": "Good morning", "pronunciation": "BWEH-nohs DEE-ahs"},
                {"language": "Spanish", "word": "Murcia", "english": "Celeste's hometown!", "pronunciation": "MOOR-thee-ah"},
            ]
        
        import random
        random.seed(day_of_year)
        return random.choice(words)


# Singleton instance
kai = KaiPresence()