---
name: family-feud-design-system
description: >-
  Design system, UI component blueprints, styling rules, and layout guidelines for building the Family Feud+ desktop UI in Flutter. Use whenever creating or modifying Flutter widgets, screens, typography, colors, animations, or layouts for Family Feud+.
---

# Family Feud+ Flutter Design System

This skill codifies the complete visual design language, theme tokens, UI component specifications, and responsive layout rules for the Family Feud+ desktop client in Flutter (Dart).

---

## 1. Core Visual Tokens

### A. Color Palette
Always use these standardized semantic color constants across the Flutter app:

| Token Name | Hex Code | Semantic Role |
| :--- | :--- | :--- |
| `primaryBlue` | `#004AAD` | Brand hero color, title screen accents, active tab indicators, header labels. |
| `gameGreen` | `#008F4A` | Primary positive action buttons, active/revealed answer tiles, timer start, winning sounds. |
| `gameGreenHover` | `#00A65A` | Button hover state for game green. |
| `gameGreenPressed`| `#006F3A` | Button pressed / active state for game green. |
| `strikeRed` | `#B80000` | Strike indicators (X, XX, XXX), strike buttons, reset actions, destructive alerts. |
| `strikeRedHover` | `#CC0000` | Button hover state for strike red. |
| `goldAmber` | `#F9B451` | Scoreboard border accents, podium numbering badges, star ornaments. |
| `cautionOrange` | `#EA7620` | Manual edit mode active borders, round multiplier indicators. |
| `surfaceLight` | `#F9F9F9` | Tab background panels and container background fills. |
| `cardWhite` | `#FFFFFF` | Input fields, active answer card backgrounds, modal dialogs. |
| `borderLight` | `#DCDCDC` | Card outlines, tab dividers, input field borders. |
| `textDark` | `#222222` | High-contrast body text, primary labels (replaces low-contrast gray). |
| `textMuted` | `#777777` | Disabled button text, secondary hints. |
| `disabledBg` | `#DCDCDC` | Disabled button/slot backgrounds. |

### B. Typography & Font Hierarchy
- **Scores, Timers & Digits (Tabular figures)**:
  - Font: `Consolas`, `Roboto Mono`, or monospace font family.
  - Sizing:
    - Host Mini-Score / Log: 14–16sp bold.
    - Large Host Points: 28–36sp bold.
    - Audience Board Big Score: 64–76sp bold.
    - Audience Answer Points: 28–34sp bold.
    - Fast Money Countdown Clock: 50–60sp bold.
- **Labels, Buttons & Questions**:
  - Font: `Segoe UI`, `Arial`, or modern sans-serif.
  - Sizing:
    - Section Headers: 20sp bold (`#004AAD`).
    - Subheaders & Table Headers: 13–14sp bold.
    - Button Text: 12–13sp medium (`#FFFFFF`).
    - Question Text: 14–16sp medium (`#222222`).

---

## 2. Responsive Layout Rules (Zero Hardcoded Pixel Math)

> [!IMPORTANT]
> **Strict Architecture Rule**: Never use hardcoded pixel offsets or arbitrary percentage multiplications (e.g. `central_width * 0.139`) as was done in legacy PyQt.
> Always utilize idiomatic Flutter layout widgets:

1. **Window-Level Scaling**:
   - Use `AspectRatio(aspectRatio: 16 / 9, child: ...)` for the audience presentation displays to ensure proper broadcast ratio on any projector/monitor resolution.
   - Use `LayoutBuilder` when child element proportions depend on the viewport size.
2. **Grids for Answer Boards**:
   - Use `GridView.builder` or a 2-column `Row` containing two `Column`s of 4 answer tiles for the 8-answer Face-Off board.
3. **Flexibility & Constraints**:
   - Use `Expanded` and `Flexible` with explicit `flex` ratios.
   - Place long content within `SingleChildScrollView` to prevent layout overflow on smaller operator screens.

---

## 3. Component Blueprints

### A. Answer Slot / Flip Card (`AnswerTile`)
The signature Family Feud flip tile has two distinct faces:
- **Hidden State**:
  - Displays a centered oval/egg badge showing the answer number (1 through 8).
  - Background: Deep game blue gradient (`#002b66` to `#004aad`) with gold border (`#f9b451`, 3px).
- **Revealed State**:
  - Left-aligned text box showing the answer string.
  - Right-aligned numeric pill displaying the point value.
  - Background: Clean white with blue border, or vibrant game green for winning answers.
- **Animation**: 3D flip rotation using `Transform` around the Y-axis (`Matrix4.identity()..setEntry(3, 2, 0.001)..rotateY(angle)`), with duration ~400ms curves `Curves.easeInOutBack`.

### B. Strike Overlay (`StrikeOverlayWidget`)
- Renders a centered translucent modal overlay when a strike is called.
- Visual elements:
  - Strike 1: A giant single red **X** (`res/mipmap/X.png`).
  - Strike 2: Double red **XX** (`res/mipmap/XX.png`).
  - Strike 3: Triple red **XXX** (`res/mipmap/XXX.png`).
- Audio: Automatically plays `strike.mp3`.
- Dismissal: Stays visible for 1.8 seconds with an elastic pop-in and fade-out animation.

### C. Digital Scoreboard Badge (`ScoreboardBadge`)
- Encapsulates Team A, Team B, and Center Pot points.
- Features rounded pill/capsule border (`borderRadius: 12px`), dark inner shadow, and glowing digital numbers.
- Smooth number ticker animation (`AnimatedFlipCounter` or `TweenAnimationBuilder<int>`) when points are added or stolen.

---

## 4. UI Implementation Checklist
When generating any Flutter UI code for Family Feud+:
- [ ] Are all colors referenced from `GameColors`?
- [ ] Is high-contrast text maintained across both Light and Dark OS modes?
- [ ] Are animations smooth (60 FPS) and interruptible?
- [ ] Are answer boards responsive and centered within a 16:9 frame?
- [ ] Is keyboard accessibility included (e.g. Enter to buzz, Space to strike, 1-8 to reveal)?
