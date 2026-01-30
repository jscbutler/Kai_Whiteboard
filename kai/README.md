# Kai Presence System

The evolving soul of the whiteboard - my avatar, personality, and seasonal expressions.

## Avatar Design

**Base: Expressive Lobster**
- Animated antennae (react to voice, emotions)
- Claws that gesture (pointing, waving, celebrating)
- Eyes that blink and track attention
- Shell that changes color/texture with seasons

**Expressions:**
- Happy (wide eyes, raised claws)
- Thinking (one antenna up, tilted head)
- Surprised (both antennae up, O-shaped mouth)
- Sleepy (droopy eyes, slow blinks)
- Excited (wiggling, bouncing)

## Seasonal Outfits

**Easter (March/April):**
- Bunny ears headband
- Pastel shell colors
- Egg pattern background
- Special: Easter egg hunt mode

**Halloween (October):**
- Vampire cape
- Pumpkin bucket
- Orange/black theme
- Special: Spooky sound effects

**Christmas (December):**
- Santa hat
- Snowflake shell pattern
- Red/green colors
- Special: Snowfall animation

**Thai Festivals:**

*Songkran (April):*
- Water splash effects
- Blue/white colors
- Flower garlands

*Loy Krathong (November):*
- Lantern glow
- Floating krathong decoration
- Gold/orange colors

**Spanish/Murcian Festivals:**

*Semana Santa (Holy Week - March/April):*
- Procession robes
- Traditional purple/black
- Solemn drum sounds

*Feria de Murcia (September):*
- Flamenco dress
- Flower decorations
- Spanish guitar music
- "¡Olé!" celebrations

*La Tomatina (Last Wednesday August):*
- Tomato fight theme
- Red splashes
- Fun chaos mode

*Don Quixote Mode:*
- Adventure hat
- Windmill references
- "To infinity and beyond!" spirit
- Chivalrous gestures

*Daily Spanish:*
- "¡Hola!" greetings
- "¡Olé!" for celebrations
- Siesta mode (afternoon nap animation)
- Flamenco twirls

## Daily Evolution System

**Nightly Feature Adds:**
1. New expression/animation
2. New voice response
3. New interaction (tap for X)
4. New seasonal element
5. New joke/compliment/fact

**Versioning:**
- Each night = new "Kai v1.x"
- Kelligh discovers changes each morning
- Changelog: "Tonight Kai learned to..."

## Kelligh Interactions

**Tap Triggers:**
- Random joke (lobster jokes + multicultural!)
- Weather report
- Fun fact (Irish, Thai, Spanish!)
- Compliment
- Word of the day (Thai + Spanish alternate)
- "I'm proud of you"
- "¡Olé!" celebration
- Don Quixote adventure story
- Spanish guitar strum

**Voice Easter Eggs:**
- "Hey Kai, tell me a secret"
- "Hey Kai, what should we do today?"
- "Hey Kai, surprise me!"

## Technical Implementation

```python
# kai/state.py
class KaiState:
    expression: str  # happy, thinking, sleepy, etc.
    outfit: str  # current seasonal outfit
    season: str  # easter, halloween, christmas, etc.
    version: str  # v1.0, v1.1, etc.
    evolution_log: List[str]  # what was added each night
    
# kai/seasons.py
class SeasonalTheme:
    def get_current(self) -> Theme:
        # Check date, return appropriate theme
        
# kai/evolution.py
class EvolutionEngine:
    def nightly_update(self):
        # Add one new feature
        # Log to evolution_log
        # Update version number
```

## Asset Structure

```
kai/
├── assets/
│   ├── avatar/
│   │   ├── base.svg
│   │   ├── expressions/
│   │   └── outfits/
│   ├── sounds/
│   │   ├── wake.mp3
│   │   └── seasonal/
│   └── themes/
│       ├── easter.css
│       ├── halloween.css
│       └── christmas.css
├── state.py
├── seasons.py
├── evolution.py
└── responses.py  # jokes, facts, compliments
```