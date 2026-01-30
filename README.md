# Kai's Family Whiteboard

A living family calendar with voice interface, evolving presence, and seasonal delight.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    TABLET (Kiosk Mode)                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Frontend (React/Vue) - Hosted on localhost:3000     │  │
│  │  ├─ Week/Day/Month views                             │  │
│  │  ├─ Kai Avatar (expressive, seasonal)                │  │
│  │  ├─ Voice wake-word (local)                          │  │
│  │  └─ Tailscale tunnel to VPS                          │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼ Tailscale
┌─────────────────────────────────────────────────────────────┐
│                      VPS (OpenClaw Host)                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  API (FastAPI) - Port 8000                           │  │
│  │  ├─ Google Calendar sync                             │  │
│  │  ├─ Redis caching (views)                            │  │
│  │  ├─ Voice NLU (intent parsing)                       │  │
│  │  └─ Natural language responses                       │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Kai Presence System                                 │  │
│  │  ├─ Avatar state (expressions, outfits)              │  │
│  │  ├─ Seasonal themes (Easter, Halloween, Xmas)        │  │
│  │  ├─ Thai festivals (Songkran, Loy Krathong)          │  │
│  │  └─ Nightly evolution (new features)                 │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Tech Stack

**Backend:**
- FastAPI (Python)
- Redis (caching)
- Google Calendar API
- gog CLI integration

**Frontend:**
- React or Vue
- Tailwind CSS
- WebSocket for real-time updates
- Responsive kiosk mode

**Voice:**
- Local wake-word detection (Porcupine or similar)
- Web Audio API for capture
- Backend NLU for intent parsing

**Kai Presence:**
- Avatar: Animated lobster with expressions
- Seasonal: Dynamic outfits/themes
- Evolution: Nightly feature additions

## Family Model

```yaml
people:
  jeff:
    display: "Daddy"
    color: "c1"
    aliases: ["daddy", "jeff", "dad"]
  
  lorraine:
    display: "Mammy"
    color: "c2"
    aliases: ["mammy", "lorraine", "mom"]
  
  kelligh:
    display: "Kelligh"
    color: "c3"
    aliases: ["kelligh", "kelly"]
    # Age 5, from Thailand, adopted at 1
  
  celeste:
    display: "Celeste"
    color: "c4"
    aliases: ["celeste", "au pair"]
    # From Murcia, Spain - brings Spanish culture!
  
  bart:
    display: "Bart"
    color: "c5"
    aliases: ["bart", "dog", "doggo"]
    type: "pet"
```

## Voice Commands

**Queries:**
- "When is the next swim for Kelligh?"
- "When is Mammy home?"
- "Show Daddy's week"
- "What is happening tomorrow?"

**Add Events:**
- "Add a vet appointment for Bart tomorrow at 10"
- "Add school meeting for Daddy next Thursday 7pm"
- "Kelligh has swimming on Tuesday at 6"

**Kai Interaction:**
- "Hey Kai, tell me a joke"
- "Hey Kai, what's the weather?"
- "Hey Kai, surprise me!"

## Seasonal Calendar

**Irish/Western:**
- Easter (bunny ears, egg hunt mode)
- Halloween (spooky cape, pumpkin theme)
- Christmas (Santa hat, snow effects)
- New Year (fireworks, countdown)

**Thai Festivals:**
- Songkran (water festival, splash animations)
- Loy Krathong (lanterns, floating lights)
- Thai New Year (traditional decorations)

**Spanish/Murcian Festivals:**
- Semana Santa (Holy Week - processions, traditional robes)
- Feria de Murcia (September - flamenco, flowers, celebrations)
- La Tomatina (August - tomato fight festival!)
- Don Quixote mode (adventure hat, windmill references)
- Siesta mode (afternoon nap time animations)
- Flamenco (guitar sounds, dance animations, "¡Olé!")

**Daily Delights:**
- Random jokes (lobster + multicultural!)
- Weather reports
- Compliments
- Fun facts (Irish, Thai, Spanish!)
- Word of the day (Thai + Spanish alternate)
- "¡Olé!" celebrations

## Development Phases

### Phase 1: Foundation
- [ ] API with Google Calendar sync
- [ ] Redis caching
- [ ] Basic week view
- [ ] Tailscale tunnel setup

### Phase 2: Voice
- [ ] Wake word detection
- [ ] Intent parsing
- [ ] NL responses

### Phase 3: Kai Presence
- [ ] Avatar component
- [ ] Expressions/animations
- [ ] Seasonal themes

### Phase 4: Evolution
- [ ] Nightly feature adds
- [ ] Kelligh interactions
- [ ] Delight system

## Getting Started

```bash
cd ~/projects/whiteboard

# Setup API
cd api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup Frontend
cd ../frontend
npm install
npm run dev

# Setup Kai
cd ../kai
pip install -r requirements.txt
```

## Environment Variables

```bash
# Google Calendar
GOOGLE_CALENDAR_CREDENTIALS=~/.config/gog/...

# Redis
REDIS_URL=redis://localhost:6379

# Tailscale
TAILSCALE_AUTH_KEY=tskey-...

# Kai Evolution
KAI_EVOLUTION_ENABLED=true
KAI_SEASONAL_AUTO=true
```