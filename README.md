# Family Feud+

A desktop application built with Python and PyQt5 designed to host and play Family Feud games. The software provides sound effects, video title screens, dual-screen host controls, Face-Off and Fast Money rounds, and built-in SQLite question database management.

---

## Features

- Host Control Panel: Interface for managing game flow, score tracking, team names, round transitions, and manual point adjustments.
- Title Screen and Multimedia: Animated video title screen with theme music and sound effects using OpenCV and PyQt5 Multimedia.
- Face-Off Round Window: Interactive Face-Off game board displaying question prompts, answer reveals, strikes (X, XX, XXX), and point multipliers (Single, Double, Triple).
- Fast Money Round Window: Fast Money board supporting dual contestants, timers, question navigation, answer entry, point tallying, and total score verification.
- Question Database Management: SQLite databases (db/Face-Off Questions.db and db/Fast-Money Questions.db) with support for loading custom question sets directly through the UI.
- Audio and Visual Effects: Game-show sound effects (buzzers, strikes, bells, correct/incorrect dings, commercial stingers) and visual assets.

---

## Prerequisites

- Python 3.9 or higher
- Operating System: macOS, Windows, or Linux

---

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone git@github.com:Jhay-EL/Family-Feud-Plus.git
   cd Family-Feud-Plus
   ```

2. Create and activate a virtual environment:
   - On macOS and Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - On Windows:
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Application

With your virtual environment activated, run:

```bash
python Family-feud+.py
```

### Operation Notes:
- Dual Monitor Setup: Run the host control panel on the primary monitor and move the Face-Off, Fast Money, or Title Screen windows to a second display or projector for audience and player viewing.
- Custom Questions: Modify or create question databases using the built-in SQLite database editor or by swapping database files in the db/ directory.

---

## Project Structure

```text
Family-Feud+/
|-- Family-feud+.py          # Main application and Host Control Panel
|-- Face_off_window.py        # Face-Off Round game board window
|-- Fast_Money_window.py      # Fast Money Round game board window
|-- TitleScreen_window.py     # Animated title screen window
|-- gui_setup.py              # UI layout and component initialization
|-- ui_adjustments.py         # Dynamic UI styling and adjustments
|-- requirements.txt          # Python package dependencies
|-- db/                       # SQLite question databases
|   |-- Face-Off Questions.db
|   `-- Fast-Money Questions.db
|-- res/                      # Multimedia assets
|   |-- bg/                   # Video backgrounds and images
|   |-- img/                  # UI graphics and board screenshots
|   |-- mipmap/               # Icons and logos
|   `-- sound/                # Game audio and sound effects
|-- etc/                      # Documentation, guides, and design previews
|-- LICENSE                   # MIT License
`-- README.md                 # Project documentation
```

---

## Dependencies

- PyQt5 - GUI framework and multimedia handling
- opencv-python - Video decoding for animated backgrounds
- psutil - Process and system management

---

## License

This project is open-source software licensed under the MIT License. See the LICENSE file for details.
