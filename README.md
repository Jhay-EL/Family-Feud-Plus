# Family Feud+ 🎮

A feature-rich, interactive desktop application built with Python and PyQt5 designed to host and play **Family Feud** games. Complete with authentic sound effects, video title screens, dual-screen host controls, Face-Off and Fast Money rounds, and built-in SQLite question database management.

---

## ✨ Features

- **Host Control Panel**: Full management interface for game flow, score tracking, team names, round transitions, and manual point adjustments.
- **Title Screen & Multimedia**: Animated video title screen with theme music and sound effects powered by OpenCV and PyQt5 Multimedia.
- **Face-Off Round Window**: Interactive Face-Off game board displaying question prompts, answer reveals, strikes (X, XX, XXX), and point multipliers (Single, Double, Triple).
- **Fast Money Round Window**: Fast Money board supporting dual contestants, timers, question navigation, answer entry, point tallying, and total score verification.
- **Question Database Management**: Pre-loaded SQLite databases (`db/Face-Off Questions.db` and `db/Fast-Money Questions.db`) with support for loading custom question sets directly through the UI.
- **Audio & Visual Effects**: Authentic sound effects (buzzers, strikes, bells, correct/incorrect dings, commercial stingers) and game-show visuals.

---

## 📋 Prerequisites

- **Python 3.9+** (tested on Python 3.9 – 3.13)
- Operating System: macOS, Windows, or Linux

---

## 🚀 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone git@github.com:Jhay-EL/Family-Feud-Plus.git
   cd Family-Feud-Plus
   ```

2. **Create and activate a virtual environment**:
   - On macOS/Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - On Windows:
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🕹️ Running the Game

With your virtual environment activated, run:

```bash
python Family-feud+.py
```

### Tips for Playing:
- **Dual Monitor Setup**: Run the host control panel on your primary monitor and move the Face-Off / Fast Money / Title Screen windows to a second display or projector for the audience and players.
- **Custom Questions**: Modify or create your own question databases using the built-in SQLite database editor or by swapping database files in the `db/` directory.

---

## 📁 Project Structure

```text
Family-Feud+/
├── Family-feud+.py          # Main application & Host Control Panel
├── Face_off_window.py        # Face-Off Round game board window
├── Fast_Money_window.py      # Fast Money Round game board window
├── TitleScreen_window.py     # Animated title screen window
├── gui_setup.py              # UI layout & component initialization
├── ui_adjustments.py         # Dynamic UI styling & adjustments
├── requirements.txt          # Python package dependencies
├── db/                       # SQLite question databases
│   ├── Face-Off Questions.db
│   └── Fast-Money Questions.db
├── res/                      # Multimedia assets
│   ├── bg/                   # Video backgrounds & images
│   ├── img/                  # UI graphics & board screenshots
│   ├── mipmap/               # Icons & logos
│   └── sound/                # Game audio & sound effects
├── etc/                      # Documentation, guides & design previews
├── LICENSE                   # MIT License
└── README.md                 # Project documentation
```

---

## 📦 Dependencies

- [`PyQt5`](https://pypi.org/project/PyQt5/) – GUI framework and multimedia handling
- [`opencv-python`](https://pypi.org/project/opencv-python/) – Video decoding for animated backgrounds
- [`psutil`](https://pypi.org/project/psutil/) – Process and system management

---

## 📄 License

This project is open-source software licensed under the [MIT License](LICENSE).
