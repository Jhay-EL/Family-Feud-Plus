---
name: family-feud-dual-display
description: >-
  Architectural patterns, window manager configurations, monitor enumeration, and state synchronization for multi-screen projection (Operator Console + Audience Display) in Family Feud+. Use when working on dual-monitor workflows, fullscreen presentation boards, or multi-window Flutter setups.
---

# Family Feud+ Dual-Display & Presentation Architecture

Family Feud+ relies on a **dual-screen architecture**:
1. **Operator Console Window** (Display 1 - Host Monitor): Complete operator controls, question bank, score overrides, soundboard, match logs.
2. **Audience Presentation Window** (Display 2 - Projector/TV): Fullscreen cinematic board for contestants and audience (Title Video, Face-Off board, Fast Money board).

---

## 1. Multi-Window Strategy in Flutter Desktop

### Architecture Choice: Multi-Instance or `desktop_multi_window`
For Flutter Desktop, there are two primary approaches for dual-monitor setups:

- **Approach A: Separate Window Process with Mode Flag (Recommended & Most Robust)**
  - Launching the app normally starts the **Operator Console**.
  - When the operator clicks "Deploy Face-Off" or "Deploy Title Screen", the app spawns a secondary lightweight process:
    ```bash
    flutter_frontend --mode=presentation --display=1 --view=face_off
    ```
  - Both windows connect to the **same local Python WebSocket server** (`ws://127.0.0.1:8765/ws`).
  - **Advantage**: Fully decoupled, native OS window management on macOS and Windows, zero native C++ crash risks, independent GPU render contexts.

- **Approach B: In-Process Multi-Window (`desktop_multi_window`)**
  - Uses the `desktop_multi_window` plugin to create a secondary child window in the same Flutter runtime.
  - Shares memory directly, but requires specific C++ runner build setup.

---

## 2. Monitor Discovery & Positioning

Using `screen_retriever` and `window_manager`:

```dart
import 'package:screen_retriever/screen_retriever.dart';
import 'package:window_manager/window_manager.dart';

Future<List<Display>> getAvailableDisplays() async {
  return await screenRetriever.getAllDisplays();
}

Future<void> openPresentationOnDisplay(Display targetDisplay) async {
  await windowManager.ensureInitialized();
  
  // Set bounds to target display rectangle
  await windowManager.setBounds(targetDisplay.visiblePosition & targetDisplay.size);
  await windowManager.setFullScreen(true);
}
```

---

## 3. Presentation Board Visual Specifications

The presentation window must adhere to strict broadcast standards:
1. **Letterboxing & Aspect Ratio**:
   - Wrap the game board in `AspectRatio(aspectRatio: 16 / 9, child: ...)` with `BoxFit.contain` so that 1080p, 4K, or 16:10 projectors never distort fonts or board geometry.
2. **Cursor Management**:
   - Hide the mouse cursor after 3 seconds of inactivity (`MouseRegion` + timer with `SystemMouseCursors.none`).
3. **Hardware-Accelerated Backgrounds**:
   - Use `media_kit` to loop `res/bg/FaceOff Round.mp4` or `res/bg/Title Screen.mp4` seamlessly behind the widget tree.
   - Set canvas blending so that text and score badges stay razor sharp over moving video.

---

## 4. Lockstep State Synchronization

When an operator performs an action on the Console:
```
Operator Console: User clicks "Reveal Answer 3"
       │
       ▼
Python Core: Engine validates, adds points to pot, broadcasts STATE_SYNC
       │
       ▼ (Simultaneous WebSocket Push)
Presentation Board: AnswerFlipCard(index: 3) receives isRevealed=true
       │
       ▼
Triggers 3D Flip Animation (450ms) + Audio Chime
```
Neither window polls. All updates are reactive and instant.
