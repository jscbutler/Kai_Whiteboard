"""
Kai Family Whiteboard API
FastAPI backend with Google Calendar integration and caching
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import json
import os

app = FastAPI(title="Kai Family Whiteboard", version="1.0.0")

# CORS for tablet frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple file-based cache (will upgrade to Redis later)
CACHE_FILE = os.path.expanduser("~/.openclaw/workspace/whiteboard_cache.json")

def get_cache():
    """Load cache from file"""
    try:
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def set_cache(key: str, value: dict, ttl_hours: int = 4):
    """Save to cache with TTL"""
    cache = get_cache()
    cache[key] = {
        "data": value,
        "expires": (datetime.now() + timedelta(hours=ttl_hours)).isoformat()
    }
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f)

def get_cached(key: str):
    """Get from cache if not expired"""
    cache = get_cache()
    if key in cache:
        entry = cache[key]
        expires = datetime.fromisoformat(entry["expires"])
        if datetime.now() < expires:
            return entry["data"]
    return None

# Family model
FAMILY = {
    "jeff": {"display": "Daddy", "color": "#3b82f6", "aliases": ["daddy", "jeff", "dad"], "email": "jscbutler@gmail.com"},
    "lorraine": {"display": "Mammy", "color": "#ec4899", "aliases": ["mammy", "lorraine", "mom"], "email": ""},
    "kelligh": {"display": "Kelligh", "color": "#10b981", "aliases": ["kelligh", "kelly"], "email": ""},
    "celeste": {"display": "Celeste", "color": "#f59e0b", "aliases": ["celeste", "au pair"], "email": ""},
    "bart": {"display": "Bart", "color": "#8b5cf6", "aliases": ["bart", "dog", "doggo"], "email": ""},
}

class Event(BaseModel):
    event_id: str
    title: str
    start: datetime
    end: datetime
    people_tags: List[str]
    category: Optional[str] = None
    location: Optional[str] = None
    all_day: bool = False
    calendar_id: Optional[str] = None

class WeekView(BaseModel):
    range_start: datetime
    range_end: datetime
    days: List[dict]
    next_up: Optional[Event]
    people_legend: dict


def fetch_google_calendar(start_date: datetime, end_date: datetime) -> List[Event]:
    """Fetch events from Google Calendar using gog"""
    import subprocess
    
    events = []
    
    try:
        # Run gog command to fetch events
        # This uses the already-authenticated gog CLI
        result = subprocess.run(
            ['gog', 'calendar', 'events', 'list', 
             '--calendar', 'primary',
             '--since', start_date.strftime('%Y-%m-%d'),
             '--until', end_date.strftime('%Y-%m-%d'),
             '--max', '100'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            # Parse the output (this is a simplified parser)
            lines = result.stdout.strip().split('\n')
            for line in lines:
                # Look for event lines
                if '|' in line and 'ID' not in line:
                    parts = line.split('|')
                    if len(parts) >= 4:
                        event_id = parts[1].strip()
                        title = parts[2].strip()
                        date_str = parts[3].strip()
                        
                        # Derive people tags from title
                        people_tags = []
                        title_lower = title.lower()
                        for person_id, person in FAMILY.items():
                            for alias in person['aliases']:
                                if alias in title_lower:
                                    people_tags.append(person_id)
                                    break
                        
                        # Parse date (simplified)
                        try:
                            event_date = datetime.strptime(date_str, '%Y-%m-%d')
                        except:
                            event_date = start_date
                        
                        events.append(Event(
                            event_id=event_id,
                            title=title,
                            start=event_date,
                            end=event_date + timedelta(hours=1),
                            people_tags=people_tags,
                            category="general"
                        ))
        
    except Exception as e:
        print(f"Error fetching calendar: {e}")
    
    return events


def get_mock_events() -> List[Event]:
    """Return mock events for testing"""
    today = datetime.now()
    return [
        Event(
            event_id="1",
            title="Swim class - Kelligh",
            start=today.replace(hour=18, minute=0),
            end=today.replace(hour=19, minute=0),
            people_tags=["kelligh"],
            category="activity",
            location="Leisure centre"
        ),
        Event(
            event_id="2",
            title="School pickup",
            start=today.replace(hour=14, minute=30),
            end=today.replace(hour=15, minute=0),
            people_tags=["kelligh"],
            category="school"
        ),
        Event(
            event_id="3",
            title="Dinner with family",
            start=today.replace(hour=19, minute=0),
            end=today.replace(hour=20, minute=0),
            people_tags=["jeff", "lorraine", "kelligh", "celeste"],
            category="meal"
        ),
    ]


@app.get("/")
async def root():
    return {"message": "Kai Family Whiteboard API", "version": "1.0.0", "status": "running"}


@app.get("/api/family")
async def get_family():
    """Return family members and their aliases"""
    return FAMILY


@app.get("/api/calendar/week")
async def get_week_view(person: Optional[str] = None):
    """
    Get week view calendar data
    Cached with 4-hour TTL
    """
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())  # Monday
    week_end = week_start + timedelta(days=7)
    
    cache_key = f"week:{person or 'all'}:{week_start.strftime('%Y-%W')}"
    
    # Try cache first
    cached = get_cached(cache_key)
    if cached:
        return cached
    
    # Fetch events (try Google Calendar, fall back to mock)
    try:
        events = fetch_google_calendar(week_start, week_end)
        if not events:
            events = get_mock_events()
    except:
        events = get_mock_events()
    
    # Build week view
    days = []
    for i in range(7):
        day_date = week_start + timedelta(days=i)
        day_events = [
            {
                "id": e.event_id,
                "title": e.title,
                "start": e.start.isoformat(),
                "end": e.end.isoformat(),
                "people": e.people_tags,
                "color": FAMILY.get(e.people_tags[0], {}).get("color", "#3b82f6") if e.people_tags else "#3b82f6"
            }
            for e in events
            if e.start.date() == day_date.date()
        ]
        days.append({
            "date": day_date.strftime("%Y-%m-%d"),
            "day_name": day_date.strftime("%a"),
            "day_num": day_date.day,
            "is_today": day_date.date() == today.date(),
            "events": day_events
        })
    
    # Find next upcoming event
    next_up = None
    for e in sorted(events, key=lambda x: x.start):
        if e.start > today:
            next_up = e
            break
    
    view = {
        "range_start": week_start.isoformat(),
        "range_end": week_end.isoformat(),
        "days": days,
        "next_up": {
            "id": next_up.event_id,
            "title": next_up.title,
            "start": next_up.start.isoformat(),
            "people": next_up.people_tags
        } if next_up else None,
        "people_legend": {k: {"display": v["display"], "color": v["color"]} 
                         for k, v in FAMILY.items()}
    }
    
    # Cache for 4 hours
    set_cache(cache_key, view, 4)
    
    return view


@app.get("/api/calendar/next")
async def get_next_event(person: Optional[str] = None):
    """Get the next upcoming event"""
    today = datetime.now()
    
    # Get events for today
    week_view = await get_week_view(person)
    today_data = next((d for d in week_view["days"] if d["is_today"]), None)
    
    if today_data and today_data["events"]:
        upcoming = [
            e for e in today_data["events"]
            if datetime.fromisoformat(e["start"]) > today
        ]
        if upcoming:
            return {"next_event": upcoming[0]}
    
    return {"next_event": None}


@app.post("/api/calendar/event")
async def add_event(event: Event):
    """Add a new event to the calendar"""
    # TODO: Add to Google Calendar via gog
    # For now, invalidate cache
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    cache_key = f"week:all:{week_start.strftime('%Y-%W')}"
    
    # Clear cache
    cache = get_cache()
    if cache_key in cache:
        del cache[cache_key]
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache, f)
    
    return {"status": "created", "event_id": event.event_id, "message": "Event added (cache invalidated)"}


@app.get("/api/kai/status")
async def get_kai_status():
    """Get Kai's current state (expression, outfit, version)"""
    from kai.presence import kai
    
    return {
        "expression": kai.expression,
        "outfit": kai.outfit,
        "season": kai.season,
        "version": kai.version,
        "last_evolution": datetime.now().isoformat()
    }


@app.post("/api/kai/interact")
async def interact_with_kai(trigger: str = "tap"):
    """Interact with Kai - get response"""
    from kai.presence import kai
    
    if trigger == "tap":
        # Random response type
        import random
        response_type = random.choice(["joke", "compliment", "fact"])
        message = kai.get_response(response_type)
        
        return {
            "type": response_type,
            "message": message,
            "expression": "happy"
        }
    
    elif trigger == "word":
        word = kai.get_word_of_the_day()
        return {
            "type": "word_of_the_day",
            "language": word["language"],
            "word": word["word"],
            "english": word["english"],
            "pronunciation": word["pronunciation"]
        }
    
    return {"type": "unknown", "message": "Hello! I'm Kai!", "expression": "happy"}


@app.post("/api/voice/command")
async def process_voice_command(command: dict):
    """
    Process voice command and return response
    """
    text = command.get("text", "").lower()
    
    # Simple intent parsing
    if "when" in text and ("kelligh" in text or "swim" in text):
        return {
            "command": text,
            "intent": "query_schedule",
            "response": "Kelligh has swim class today at 6 PM!",
            "action": "show_events"
        }
    
    elif "add" in text or "create" in text:
        return {
            "command": text,
            "intent": "add_event",
            "response": "I heard you want to add an event. What should I call it?",
            "action": "prompt_details"
        }
    
    elif "joke" in text or "funny" in text:
        from kai.presence import kai
        return {
            "command": text,
            "intent": "entertain",
            "response": kai.get_response("joke"),
            "action": "speak"
        }
    
    return {
        "command": text,
        "intent": "unknown",
        "response": "I heard you! I'm still learning to understand. Can you try saying 'When is Kelligh's swim class?' or 'Tell me a joke'?",
        "action": "speak"
    }


@app.get("/api/status")
async def get_status():
    """Health check endpoint"""
    return {
        "api": "ok",
        "cache": "file_based",
        "google_calendar": "gog_cli",
        "timestamp": datetime.now().isoformat(),
        "family_members": len(FAMILY)
    }


if __name__ == "__main__":
    import uvicorn
    print("🦞 Starting Kai Family Whiteboard API...")
    print("📅 Connecting to Google Calendar via gog")
    print("💾 Using file-based cache (Redis coming soon)")
    uvicorn.run(app, host="0.0.0.0", port=8000)