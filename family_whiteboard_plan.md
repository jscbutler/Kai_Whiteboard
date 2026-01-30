## 9) Normalized event data model (keeps views consistent)

### 9.1 Canonical Event object (what everything becomes)

All calendar sources should be transformed into a single internal shape:

- `event_id` (string) — stable ID (Google event id)
- `source` (enum) — `google`
- `calendar_id` (string)
- `title` (string)
- `description` (string, optional)
- `location` (string, optional)
- `start` (ISO timestamp, timezone aware)
- `end` (ISO timestamp, timezone aware)
- `all_day` (bool)
- `attendees` (list of strings/emails, optional)
- `people_tags` (list) — e.g. `["kelligh","mammy","daddy"]` (derived rules)
- `category` (enum/string) — e.g. `swim`, `school`, `work`, `travel` (derived from title/calendar)
- `color_key` (string) — UI mapping (per person/calendar)
- `visibility` (enum) — `public|private` (for UI redaction rules)
- `last_modified` (ISO timestamp) — for caching + reconciliation
- `fingerprint` (string) — hash of key fields to detect changes

### 9.2 Derived fields (so NL queries are easy)

At ingest time, compute:

- `day_key` = `YYYY-MM-DD` in household timezone
- `week_key` = ISO week (`YYYY-Www`)
- `sort_key` = start time numeric
- `summary_line` = short human form (“Swim (Kelligh) 18:00”)

### 9.3 View payloads (what the UI actually consumes)

Don’t make the UI reconstruct logic. Return views pre-shaped:

**Week view**

- `range_start`, `range_end`
- `days`: list of `{date, events:[...]}` sorted
- `next_up`: single event + countdown
- `people_legend`: `{person -> color_key}`

**Month view**

- calendar grid cells with event counts and top 1–2 events

**Day view**

- timeline list + “now marker” + grouped by person/category if desired

---

## 10) Redis caching: key strategy + invalidation map

### 10.1 Key naming (predictable + debuggable)

Use a single namespace + version so you can migrate without pain:

- `kai:v1:view:week:{tz}:{people_scope}:{start_date}`
- `kai:v1:view:day:{tz}:{people_scope}:{date}`
- `kai:v1:view:month:{tz}:{people_scope}:{yyyy-mm}`

Where:

- `tz` = `Europe/Dublin`
- `people_scope` = `all` or `kelligh` / `mammy` etc.
- `start_date` = Monday of that week in tz

Store JSON blobs as values.

### 10.2 Metadata keys (status + hashes)

- `kai:v1:meta:last_sync_google` (timestamp)
- `kai:v1:meta:view_hash:{view_key}` (hash string)
- `kai:v1:meta:generated_at:{view_key}` (timestamp)
- `kai:v1:meta:stale_after:{view_key}` (timestamp)

This makes `/status` cheap:

- Return `last_sync_google`
- Return hashes for the main views the tablet cares about (week + next 1–2 weeks)

### 10.3 TTLs (align with your 4-hour hard refresh)

- Views TTL: **4h 15m** (a little longer than the job interval to avoid gaps)
- Meta TTL: **8–24h** (safe, low cost)
- Optional “hot week” TTL: 12h, but still rebuild on write

### 10.4 Invalidation on write (refresh-on-add/move/cancel)

When an event changes, invalidate the minimal set of impacted views:

Given event start/end dates (in household tz):

- Always invalidate:
  - `day` for start day
  - `week` containing start day
  - `month` containing start day
- If move crosses day/week/month boundaries:
  - also invalidate old day/week/month

Simple algorithm:

1) Compute `old_day/week/month` and `new_day/week/month`
2) Build set of affected view keys
3) `DEL` those keys + their meta keys
4) Rebuild immediately and return updated view payloads to client

### 10.5 Rebuild strategy (avoid stampedes)

If multiple clients request the same missing key:

- Use a short Redis lock:
  - `kai:v1:lock:{view_key}` with TTL 10–30s
- First requester rebuilds; others wait briefly and then fetch

---

## 11) Wake-word integration path (early milestone, low-maintenance)

### 11.1 Design choice: local wake word, cloud NLU

Keep wake word and mic control on the tablet:

- Wake word = local detection
- After wake word: record audio (short window) → backend transcription + intent

Why this matters:

- Privacy: no constant streaming audio to VPS
- Latency: immediate “listening” feedback
- Maintenance: you only maintain one simple device-side component

### 11.2 MVP wake word options (pick the easiest stable path)

**Option A (fastest, least fragile): “Tap-to-talk” + early wake word later**

- You want wake word early, but this is the most reliable baseline.
- Implement both: tap-to-talk first, then add wake word without changing backend.

**Option B (recommended for early wake word): Local wake word engine**
On Android, run an on-device keyword spotter.
Key requirements:

- Runs offline
- Exposes simple callbacks: `onWake()` → start capture
- Has sensitivity tuning + false-positive mitigation

### 11.3 False positives: how to prevent “Kai… Kai… Kai…”

- Require wake word + 200–400ms of silence before starting capture
- Add a short “cooldown” (e.g., 10–20s) after a trigger
- Display “Listening…” with a cancel gesture/button
- If confidence low: ask “Did you mean to call me?” and require a quick “yes”

### 11.4 Audio capture window + UX loop

- Wake triggers:
  - Start recording for 6–10 seconds
  - Stop early if silence detected for >1s
- Immediately show:
  - Transcript snippet
  - “Thinking…” indicator
- Speak response + update UI highlight

### 11.5 Security + household trust

- Wake word does **read-only** by default until you explicitly enable writes
- Destructive actions require:
  - confirmation + optional PIN OR
  - “admin voice” mode (later) + confirmation

### 11.6 Operational guardrails

- Add a “mic watchdog”:
  - if audio capture crashes, restart the local component
- Add “always visible mic state”:
  - muted/unmuted/listening indicator on screen at all times

## 12) Family model (people, aliases, and tagging rules)

### 12.1 Household members

These are the canonical “people ids” used everywhere (UI colors, filters, voice resolution):

- `jeff` — Display name: **Daddy** (Legal/name: Jeff)
- `lorraine` — Display name: **Mammy** (Legal/name: Lorraine)
- `kelligh` — Display name: **Kelligh**
- `celeste` — Display name: **Celeste** (Au Pair)
- `bart` — Display name: **Bart** (Doggo)

### 12.2 Aliases / ways people refer to each other

Store as a lookup table. These aliases are used in NL parsing, event tagging, and query resolution.

**Alias → person_id**

- `daddy` → `jeff`
- `jeff` → `jeff`

- `mammy` → `lorraine`
- `mommy` → `lorraine` (optional, if it ever comes up)
- `mum` → `lorraine` (optional)
- `lorraine` → `lorraine`

- `kelligh` → `kelligh`

- `celeste` → `celeste`
- `aupair` / `au pair` → `celeste` (optional)

- `bart` → `bart`
- `dog` / `doggo` → `bart` (optional)

### 12.3 Child-context rules (Kelligh referring to parents)

When the speaker is **Kelligh** (or when the utterance contains child-like phrasing), interpret:

- “Mammy” as `lorraine`
- “Daddy” as `jeff`

This avoids a common failure mode where “Mammy” gets treated as a generic role instead of a person.

### 12.4 Event tagging rules (people_tags)

When ingesting or creating an event, derive `people_tags` using:

1) **Explicit mention wins**

- If the utterance/event title contains any alias, tag that person.

1) **Calendar ownership contributes**

- If the event is on a person’s calendar, tag that person.

1) **Attendees contribute**

- If an attendee email maps to a person, tag them.

1) **Fallback**

- If no person is detected:
  - For queries: assume `all`
  - For adds: default to `family` calendar unless user specifies

### 12.5 UI legend & colors (implementation note)

Assign each `person_id` a stable `color_key` (don’t tie to Google’s color ids).
Example:

- `jeff` → `c1`
- `lorraine` → `c2`
- `kelligh` → `c3`
- `celeste` → `c4`
- `bart` → `c5`

### 12.6 Common utterances to support (tests)

- “When is the next swim for Kelligh?”
- “When is Mammy home?”
- “Add a vet appointment for Bart tomorrow at 10”
- “Add school meeting for Daddy next Thursday 7pm”
- “Show Mammy’s week”
- (If speaker = Kelligh) “When is Daddy home?”
