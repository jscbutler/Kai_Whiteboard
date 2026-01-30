# Quick Start Guide

## 1. Start Redis (for caching)

```bash
# Install Redis if not present
sudo apt install redis-server

# Start Redis
sudo systemctl start redis-server

# Verify
redis-cli ping
# Should return: PONG
```

## 2. Start API Backend

```bash
cd ~/projects/whiteboard/api

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start server
python main.py
# Or: uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Test
open http://localhost:8000/docs
```

## 3. Start Frontend

```bash
cd ~/projects/whiteboard/frontend

# Serve with Python (simple)
python3 -m http.server 3000

# Or with Node/Vite (if installed)
npm install
npm run dev

# Open on tablet
open http://localhost:3000
```

## 4. Setup Tailscale (for tablet access)

```bash
# On VPS (where OpenClaw runs)
sudo tailscale up

# Get auth key from Tailscale admin panel
# Or use: sudo tailscale up --authkey tskey-...

# Note the Tailscale IP
ip addr show tailscale0

# On tablet
# Install Tailscale app
# Login with same account
# Access whiteboard at: http://<tailscale-ip>:3000
```

## 5. Google Calendar Integration

```bash
# Ensure gog is authenticated
gog auth list

# Test calendar access
gog calendar events list --calendar family --max 10

# API will use existing gog credentials
```

## Project Structure

```
whiteboard/
├── api/                    # FastAPI backend
│   ├── main.py            # Main API server
│   └── requirements.txt   # Python deps
├── frontend/              # Tablet UI
│   ├── index.html         # Single-file Vue app
│   └── package.json       # Node deps (optional)
├── kai/                   # Kai presence system
│   ├── presence.py        # Avatar state & evolution
│   └── README.md          # Kai design docs
├── docs/                  # Documentation
├── family_whiteboard_plan.md  # Original spec
└── README.md              # This file
```

## Next Steps

1. **Test locally** - Get API + frontend talking
2. **Add Google Calendar sync** - Pull real family events
3. **Setup Tailscale** - Tablet can reach VPS
4. **Voice integration** - Add wake-word detection
5. **Kai evolution** - Implement nightly updates

## API Endpoints

- `GET /` - Health check
- `GET /api/family` - Family members
- `GET /api/calendar/week` - Week view (cached)
- `POST /api/calendar/event` - Add event
- `POST /api/voice/command` - Voice commands
- `GET /api/kai/status` - Kai's current state

## Family Members

- **Daddy** (Jeff) - c1
- **Mammy** (Lorraine) - c2  
- **Kelligh** - c3 (5yo, from Thailand)
- **Celeste** - c4 (au pair)
- **Bart** - c5 (doggo)

## Seasonal Themes

- Easter (March/April) - Bunny ears
- Songkran (April 13-15) - Thai water festival
- Halloween (October) - Spooky cape
- Loy Krathong (November) - Lanterns
- Christmas (December) - Santa hat

## Voice Commands

**Queries:**
- "When is the next swim for Kelligh?"
- "When is Mammy home?"
- "Show Daddy's week"

**Add Events:**
- "Add vet appointment for Bart tomorrow at 10"
- "Kelligh has swimming Tuesday at 6"

**Kai Fun:**
- "Hey Kai, tell me a joke"
- "Hey Kai, surprise me!"

## Development

**Add new feature:**
1. Edit `api/main.py` for backend
2. Edit `frontend/index.html` for UI
3. Edit `kai/presence.py` for Kai behavior
4. Test locally
5. Deploy to VPS

**Nightly evolution:**
- Run: `python kai/presence.py`
- Automatically increments version
- Adds new feature to evolution log
- Kelligh discovers changes each morning!

## Troubleshooting

**Redis not connecting:**
```bash
sudo systemctl status redis-server
sudo systemctl start redis-server
```

**API won't start:**
```bash
# Check port 8000 not in use
lsof -i :8000
# Kill if needed: kill -9 <PID>
```

**Frontend not loading:**
```bash
# Check CORS settings in api/main.py
# Ensure port 3000 is allowed
```