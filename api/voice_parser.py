"""
Voice Command Parser for Kai Whiteboard
Uses LLM to parse natural language into structured event data
"""

import os
import json
import re
from datetime import datetime, timedelta
from typing import Optional, List
import requests

# Family mapping for reference
FAMILY = {
    "jeff": {"display": "Daddy", "aliases": ["daddy", "jeff", "dad", "papa"]},
    "lorraine": {"display": "Mammy", "aliases": ["mammy", "lorraine", "mom", "mum"]},
    "kelligh": {"display": "Kelligh", "aliases": ["kelligh", "kelly", "kel"]},
    "celeste": {"display": "Celeste", "aliases": ["celeste", "au pair"]},
    "bart": {"display": "Bart", "aliases": ["bart", "dog", "doggo", "puppy"]},
}


def get_person_from_text(text: str) -> List[str]:
    """Extract person/people from text using aliases"""
    text_lower = text.lower()
    people = []
    
    for person_id, person in FAMILY.items():
        for alias in person['aliases']:
            if alias in text_lower:
                people.append(person_id)
                break
    
    return people


def parse_relative_date(text: str, base_date: datetime = None) -> Optional[datetime]:
    """Parse relative dates like 'tomorrow', 'next Thursday', 'this weekend'"""
    if base_date is None:
        base_date = datetime.now()
    
    text_lower = text.lower()
    
    # Handle "tomorrow"
    if "tomorrow" in text_lower:
        return base_date + timedelta(days=1)
    
    # Handle "today"
    if "today" in text_lower:
        return base_date
    
    # Handle "next week"
    if "next week" in text_lower:
        return base_date + timedelta(days=7)
    
    # Handle days of week
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    for i, day in enumerate(days):
        if day in text_lower:
            # Find the next occurrence of this day
            current_day = base_date.weekday()
            target_day = i
            days_ahead = target_day - current_day
            if days_ahead <= 0:  # Target day already happened this week
                days_ahead += 7
            return base_date + timedelta(days=days_ahead)
    
    return None


def parse_time(text: str) -> Optional[str]:
    """Extract time from text (e.g., '4pm', '14:30', '2 o'clock')"""
    text_lower = text.lower()
    
    # Pattern: 4pm, 4:30pm, 14:30
    time_pattern = r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)?'
    matches = re.findall(time_pattern, text_lower)
    
    if matches:
        hour, minute, period = matches[0]
        hour = int(hour)
        minute = int(minute) if minute else 0
        
        if period == 'pm' and hour != 12:
            hour += 12
        elif period == 'am' and hour == 12:
            hour = 0
        
        return f"{hour:02d}:{minute:02d}"
    
    # Common time phrases
    if "morning" in text_lower:
        return "09:00"
    if "afternoon" in text_lower:
        return "14:00"
    if "evening" in text_lower:
        return "18:00"
    if "night" in text_lower:
        return "20:00"
    
    return None


def parse_event_with_llm(text: str) -> dict:
    """
    Use LLM to parse natural language into structured event data
    Returns: {title, date, time, people, location, duration_minutes, confidence}
    """
    
    api_key = os.getenv('OPENROUTER_API_KEY')
    
    system_prompt = """You are a helpful assistant that extracts calendar event details from natural language.
    Parse the user's input and return a JSON object with these fields:
    - title: A concise event title (e.g., "Swim Class", "Doctor Appointment")
    - date_description: How the date was described (e.g., "tomorrow", "next Thursday")
    - time_description: How the time was described (e.g., "4pm", "morning")
    - people: Array of people mentioned (e.g., ["Kelligh", "Daddy"])
    - location: Location if mentioned, otherwise null
    - duration_minutes: Estimated duration (default 60 for most events, 120 for movies/parties, 30 for pickups)
    - event_type: Category like "activity", "school", "medical", "meal", "appointment"
    
    Return ONLY the JSON object, no other text."""
    
    user_prompt = f"Parse this calendar event: \"{text}\""
    
    try:
        response = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
            },
            json={
                'model': 'sourceful/riverflow-v2-pro',
                'messages': [
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt}
                ],
                'max_tokens': 300,
                'temperature': 0.3
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Extract JSON from response
            try:
                # Find JSON in the response (in case there's extra text)
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    parsed = json.loads(json_match.group())
                    return parsed
            except json.JSONDecodeError:
                pass
        
    except Exception as e:
        print(f"LLM parsing error: {e}")
    
    # Fallback: return basic structure
    return {
        "title": text,
        "date_description": "today",
        "time_description": None,
        "people": [],
        "location": None,
        "duration_minutes": 60,
        "event_type": "general"
    }


def process_voice_command(text: str) -> dict:
    """
    Main entry point: process voice command and return structured event data
    """
    text = text.strip()
    
    # Use LLM to parse
    parsed = parse_event_with_llm(text)
    
    # Resolve relative dates
    base_date = datetime.now()
    date = parse_relative_date(parsed.get('date_description', 'today'), base_date) or base_date
    
    # Parse time
    time_str = parse_time(text) or parsed.get('time_description')
    if time_str:
        hour, minute = map(int, time_str.split(':'))
        date = date.replace(hour=hour, minute=minute)
    else:
        # Default to current time or next hour
        date = date.replace(hour=base_date.hour + 1, minute=0)
    
    # Get people
    people = parsed.get('people', [])
    if not people:
        people = get_person_from_text(text)
    
    # Map people names to IDs
    people_ids = []
    for person in people:
        person_lower = person.lower()
        for person_id, person_data in FAMILY.items():
            if person_lower == person_data['display'].lower() or person_lower in [a.lower() for a in person_data['aliases']]:
                people_ids.append(person_id)
                break
    
    # Build final event
    event = {
        "title": parsed.get('title', text),
        "start": date.isoformat(),
        "end": (date + timedelta(minutes=parsed.get('duration_minutes', 60))).isoformat(),
        "people_tags": people_ids or ["family"],  # Default to generic if no one identified
        "category": parsed.get('event_type', 'general'),
        "location": parsed.get('location'),
        "all_day": False,
        "confidence": "high" if people_ids and time_str else "medium"
    }
    
    # Generate confirmation message
    people_display = ", ".join([FAMILY.get(p, {}).get('display', p) for p in people_ids]) if people_ids else "the family"
    confirmation = f"Added: {event['title']} for {people_display} on {date.strftime('%A at %I:%M %p')}"
    
    return {
        "command": text,
        "intent": "add_event",
        "parsed_event": event,
        "confirmation_message": confirmation,
        "requires_confirmation": True
    }


if __name__ == "__main__":
    # Test examples
    test_commands = [
        "Kelligh has swimming tomorrow at 4pm",
        "Daddy has a meeting on Thursday morning",
        "Add family dinner for Saturday at 7",
        "Doctor appointment for Mammy next Tuesday at 2pm",
        "Movie night this weekend"
    ]
    
    for cmd in test_commands:
        print(f"\n🎤 Command: {cmd}")
        result = process_voice_command(cmd)
        print(f"✅ Parsed: {json.dumps(result['parsed_event'], indent=2)}")
        print(f"💬 {result['confirmation_message']}")
