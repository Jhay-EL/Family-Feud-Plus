---
name: flutter-python-bridge
description: >-
  Specifications, schema contracts, WebSocket protocols, and process management for connecting the Flutter desktop frontend to the Python core engine in Family Feud+. Use when writing IPC communication, network protocols, process spawning, or backend state integration.
---

# Flutter <-> Python Bridge Specification

This skill outlines the architectural bridge connecting the Flutter desktop frontend to the headless Python core backend service in Family Feud+.

---

## 1. Architectural Model

```
+-------------------------------------------------------------+
|                     FLUTTER FRONTEND                        |
|  - Operator Console UI                                      |
|  - Audience Presentation Displays (Dual Monitor)            |
|  - WebSocket Client (Riverpod / ValueNotifier State Stream)  |
+------------------------------+------------------------------+
                               |
                   Localhost WebSocket (Port 8765)
                   JSON-RPC / Event-Driven Protocol
                               |
+------------------------------v------------------------------+
|                     PYTHON CORE BACKEND                     |
|  - Async WebSocket Server (aiohttp / FastAPI / websockets)   |
|  - Headless Game Engine & State Machine                     |
|  - SQLite Data Repository (Face-Off & Fast-Money)           |
|  - Host Hardware Audio Service (QMediaPlayer / pygame / etc)|
+-------------------------------------------------------------+
```

---

## 2. Process Lifecycle Management

The Flutter application is responsible for the Python core lifecycle:

1. **Startup**:
   - Flutter checks if a Python core instance is already listening on `ws://127.0.0.1:8765/ws`.
   - If not, Flutter spawns the Python backend as a child process via `Process.start()`:
     ```dart
     final process = await Process.start('python3', ['backend/server.py'],
         mode: ProcessStartMode.detached);
     ```
   - Flutter polls `http://127.0.0.1:8765/health` with exponential backoff until ready (timeout: 5 seconds).

2. **Shutdown**:
   - On application window close (`WindowListener.onWindowClose`), Flutter sends an explicit `SHUTDOWN` action to the Python server and terminates the spawned child process.

---

## 3. Protocol Schema: Actions vs. Events

Communication consists of two JSON message types:
- **`Action`** (Flutter $\rightarrow$ Python): Host operator triggers a game action or database query.
- **`Event`** (Python $\rightarrow$ Flutter): Python state machine broadcasts the updated state to all connected Flutter windows.

### A. Action Envelope
```json
{
  "type": "ACTION_NAME",
  "payload": { ... }
}
```

Standard Actions:
| Action Type | Payload Parameters | Description |
| :--- | :--- | :--- |
| `LOAD_QUESTION` | `{"round_type": "face_off", "id": 1}` | Loads a question and its answers into active memory. |
| `REVEAL_ANSWER` | `{"index": 2}` | Reveals answer #2, awards points to round bank, plays chime. |
| `ADD_STRIKE` | `{"team": "A"}` | Increments strike count for Team A, triggers strike X and buzzer. |
| `REWARD_POINTS` | `{"team": "A"}` | Transfers banked points to Team A's total. |
| `SET_MULTIPLIER`| `{"multiplier": 2}` | Toggles $2\times$ or $3\times$ point multiplier. |
| `START_TIMER` | `{"seconds": 3}` | Starts countdown timer. |
| `LOG_ROUND` | `{}` | Archives current round into R1–R4 match log and resets board. |
| `FAST_MONEY_INPUT` | `{"player": 1, "index": 0, "ans": "Tenga", "pts": 32}` | Sets Fast Money answers. |
| `SAVE_QUESTION` | `{"question": "...", "answers": [...]}` | Creates or updates question in SQLite. |
| `DELETE_QUESTION` | `{"id": 1}` | Deletes question from database. |

### B. Event Envelope (Broadcast)
```json
{
  "event": "EVENT_NAME",
  "data": { ... }
}
```

Key Events:
| Event Name | Data Fields | Description |
| :--- | :--- | :--- |
| `STATE_SYNC` | Full `GameState` object | Pushed on initial connect and after any state change. |
| `AUDIO_CUE` | `{"cue": "strike" | "good_answer" | "win"}` | Notifies client of audio playback. |
| `TIMER_TICK` | `{"remaining": 18}` | Pushed every second during active countdowns. |
| `DB_UPDATED` | `{"questions": [...]}` | Pushed when questions list changes. |

---

## 4. Full GameState JSON Schema Contract
```json
{
  "round": 1,
  "multiplier": 1,
  "bank_points": 75,
  "team_a": {
    "name": "Team A",
    "total_points": 120,
    "strikes": 1
  },
  "team_b": {
    "name": "Team B",
    "total_points": 0,
    "strikes": 0
  },
  "active_question": {
    "id": 1,
    "text": "Salitang pwede i describe sa saging",
    "total_survey_answers": 5,
    "answers": [
      {"index": 1, "text": "Mahaba", "points": 25, "is_revealed": true},
      {"index": 2, "text": "Mataba", "points": 20, "is_revealed": false},
      {"index": 3, "text": "Yellow", "points": 15, "is_revealed": true},
      {"index": 4, "text": "Malambot", "points": 10, "is_revealed": false},
      {"index": 5, "text": "Matamis/Masarap", "points": 5, "is_revealed": false}
    ]
  },
  "match_log": [
    {"round": 1, "team_a_points": 50, "team_b_points": 0, "team_a_strikes": 1, "team_b_strikes": 3}
  ],
  "fast_money": {
    "p1_answers": [...],
    "p2_answers": [...],
    "total_points": 145,
    "timer": 0
  }
}
```
