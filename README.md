﻿# Typing Test CLI & Streamlit

à¹‚à¸›à¸£à¹à¸à¸£à¸¡ **Typing Test CLI & Web App** à¸ªà¸³à¸«à¸£à¸±à¸šà¸§à¸±à¸”à¸„à¸§à¸²à¸¡à¹€à¸£à¹‡à¸§ (WPM) à¹à¸¥à¸°à¸„à¸§à¸²à¸¡à¹à¸¡à¹ˆà¸™à¸¢à¸³à¹ƒà¸™à¸à¸²à¸£à¸žà¸´à¸¡à¸žà¹Œ  
- **CLI version**: à¸£à¸±à¸™à¸šà¸™ Command Line  
- **Streamlit version**: à¸£à¸±à¸™à¹€à¸›à¹‡à¸™à¹€à¸§à¹‡à¸šà¹à¸­à¸›à¹ƒà¸Šà¹‰à¸‡à¸²à¸™à¸‡à¹ˆà¸²à¸¢  

à¹‚à¸›à¸£à¹€à¸ˆà¸à¸•à¹Œà¸™à¸µà¹‰à¹€à¸›à¹‡à¸™à¸‡à¸²à¸™ **Mini Project** à¸‚à¸­à¸‡à¸£à¸²à¸¢à¸§à¸´à¸Šà¸² **CP352301 Script Programming** à¸ à¸²à¸„à¹€à¸£à¸µà¸¢à¸™à¸—à¸µà¹ˆ 1 à¸›à¸µà¸à¸²à¸£à¸¨à¸¶à¸à¸©à¸² 2568  

---

## ðŸ“Œ à¸Ÿà¸µà¹€à¸ˆà¸­à¸£à¹Œ (Features)
- à¸ªà¸¸à¹ˆà¸¡à¸›à¸£à¸°à¹‚à¸¢à¸„à¸ˆà¸²à¸ `textbank.py` à¸«à¸£à¸·à¸­ `prompts.json`
- à¸ˆà¸±à¸šà¹€à¸§à¸¥à¸²à¸•à¸±à¹‰à¸‡à¹à¸•à¹ˆà¹€à¸£à¸´à¹ˆà¸¡à¸žà¸´à¸¡à¸žà¹Œà¸ˆà¸™à¸ˆà¸š
- à¸„à¸³à¸™à¸§à¸“ **Words Per Minute (WPM)**
- à¸„à¸³à¸™à¸§à¸“ **Accuracy (%)**
  - Uses word-by-word comparison for more accurate scoring.
  - Records each CLI session to `stats.json` and lets you review progress via the CLI.
  - 30-second challenge mode for breaking personal records using the last prompt.
- à¸•à¸£à¸§à¸ˆà¸ªà¸­à¸šà¸„à¸§à¸²à¸¡à¸–à¸¹à¸à¸•à¹‰à¸­à¸‡à¹à¸šà¸šà¸•à¸±à¸§à¸­à¸±à¸à¸©à¸£à¸•à¹ˆà¸­à¸­à¸±à¸à¸©à¸£
- à¸£à¸­à¸‡à¸£à¸±à¸š `Ctrl + C` à¹ƒà¸™ CLI à¹€à¸žà¸·à¹ˆà¸­à¸à¸¥à¸±à¸šà¹€à¸¡à¸™à¸¹à¸«à¸¥à¸±à¸
- (Streamlit) à¸£à¸­à¸‡à¸£à¸±à¸šà¸à¸” **Enter** à¹€à¸žà¸·à¹ˆà¸­à¸ªà¹ˆà¸‡à¸‚à¹‰à¸­à¸„à¸§à¸²à¸¡à¸—à¸±à¸™à¸—à¸µ  

---

## ðŸ“‚ à¹‚à¸„à¸£à¸‡à¸ªà¸£à¹‰à¸²à¸‡à¹‚à¸›à¸£à¹€à¸ˆà¸à¸•à¹Œ (Project Structure)

```bash
Typing-Test-CLI/
â”œâ”€â”€ .git/                   # git repo à¸‚à¸­à¸‡à¸„à¸¸à¸“
â”œâ”€â”€ .gitignore              # à¸à¸³à¸«à¸™à¸”à¹„à¸Ÿà¸¥à¹Œà¸—à¸µà¹ˆà¹„à¸¡à¹ˆà¸•à¹‰à¸­à¸‡à¸à¸²à¸£ track
â”œâ”€â”€ App/
â”‚   â””â”€â”€ main_app.py         # Streamlit app
â”‚
â”œâ”€â”€ docs/                   # à¹€à¸­à¸à¸ªà¸²à¸£à¸›à¸£à¸°à¸à¸­à¸š
â”‚   â”œâ”€â”€ PLAN.md
â”‚   â””â”€â”€ PROGRESS.md
â”‚
â”œâ”€â”€ src/typing_test/        # source code (package)
â”‚   â”œâ”€â”€ __init__.py         # à¸—à¸³à¹ƒà¸«à¹‰à¹€à¸›à¹‡à¸™ package
â”‚   â”œâ”€â”€ data/
â”‚   â”‚   â”œâ”€â”€ prompts.json
â”‚   â”‚   â””â”€â”€ script_sort_jsonPrompts.py
â”‚   â”œâ”€â”€ main.py             # CLI entry point
â”‚   â”œâ”€â”€ prompt_source.py
â”‚   â”œâ”€â”€ textbank.py
â”‚   â””â”€â”€ typing_calculate.py
â”‚
â”œâ”€â”€ requirements.txt        # dependencies (à¹€à¸Šà¹ˆà¸™ streamlit)
â”œâ”€â”€ pyproject.toml          # project config (pip install -e .)
â”œâ”€â”€ Dockerfile              # build docker image
â””â”€â”€ README.md               # à¸„à¸¹à¹ˆà¸¡à¸·à¸­à¹‚à¸›à¸£à¹€à¸ˆà¸à¸•à¹Œ

```

---

## âš™ï¸ à¸§à¸´à¸˜à¸µà¸à¸²à¸£à¸•à¸´à¸”à¸•à¸±à¹‰à¸‡à¹à¸¥à¸°à¹ƒà¸Šà¹‰à¸‡à¸²à¸™ (Installation & Usage)
1. Clone project
```bash
git clone https://github.com/pavarit548x/Typing-Test-CLI.git
cd Typing-Test-CLI
```
2. (à¹à¸™à¸°à¸™à¸³) à¸ªà¸£à¹‰à¸²à¸‡ virtual environment
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
```
3. à¸•à¸´à¸”à¸•à¸±à¹‰à¸‡ dependencies
```bash
pip install -r requirements.txt
```
à¸–à¹‰à¸²à¸­à¸¢à¸²à¸à¹ƒà¸«à¹‰à¹‚à¸„à¹‰à¸” import à¹„à¸”à¹‰à¸—à¸¸à¸à¸—à¸µà¹ˆ à¹ƒà¸Šà¹‰ editable mode:
```bash
pip install -e .
```

---

## â–¶ï¸ Run CLI version
```bash
python src/typing_test/main.py
```
à¹€à¸¡à¸™à¸¹:

* à¸à¸” 1 â†’ à¹‚à¸«à¸¡à¸”à¸›à¸à¸•à¸´ (à¸ªà¸¸à¹ˆà¸¡à¸›à¸£à¸°à¹‚à¸¢à¸„à¹ƒà¸«à¸¡à¹ˆ)
* à¸à¸” 2 â†’ à¹‚à¸«à¸¡à¸”à¸—à¸³à¸¥à¸²à¸¢à¸ªà¸–à¸´à¸•à¸´ 30 à¸§à¸´ (à¹ƒà¸Šà¹‰à¸›à¸£à¸°à¹‚à¸¢à¸„à¹€à¸”à¸´à¸¡à¸¥à¹ˆà¸²à¸ªà¸¸à¸”)
* à¸à¸” 3 â†’ à¸”à¸¹à¸ªà¸–à¸´à¸•à¸´à¸—à¸µà¹ˆà¸šà¸±à¸™à¸—à¸¶à¸à¹„à¸§à¹‰
* à¸à¸” 4 â†’ à¸­à¸­à¸à¸ˆà¸²à¸à¹‚à¸›à¸£à¹à¸à¸£à¸¡


---

## ðŸŒ Run Streamlit version
```bash
streamlit run App/main_app.py
```
à¹€à¸›à¸´à¸”à¹€à¸šà¸£à¸²à¸§à¹Œà¹€à¸‹à¸­à¸£à¹Œà¸—à¸µà¹ˆ http://localhost:8501

---

## ðŸ³ Run with Docker
1. Build image
```bash
docker build -t typing-test .
```
2. Run container
```bash
docker run -p 8501:8501 typing-test
```
à¹€à¸›à¸´à¸”à¹€à¸šà¸£à¸²à¸§à¹Œà¹€à¸‹à¸­à¸£à¹Œ: http://localhost:8501

```
Typing-Test-CLI
â”œâ”€ App
â”‚  â””â”€ main_app.py
â”œâ”€ docs
â”‚  â”œâ”€ PLAN.md
â”‚  â””â”€ PROGRESS.md
â”œâ”€ pyproject.toml
â”œâ”€ README.md
â””â”€ src
   â”œâ”€ typing_test
   â”‚  â”œâ”€ data
   â”‚  â”‚  â”œâ”€ prompts.json
   â”‚  â”‚  â””â”€ script_sort_jsonPrompts.py
   â”‚  â”œâ”€ main.py
   â”‚  â”œâ”€ prompt_source.py
   â”‚  â”œâ”€ textbank.py
   â”‚  â””â”€ typing_calculate.py
   â””â”€ typing_test.egg-info
      â”œâ”€ dependency_links.txt
      â”œâ”€ entry_points.txt
      â”œâ”€ PKG-INFO
      â”œâ”€ SOURCES.txt
      â””â”€ top_level.txt

```


