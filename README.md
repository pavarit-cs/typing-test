# Typing Test CLI & Streamlit

Typing Test CLI & Streamlit is a small project for measuring typing speed and accuracy from the terminal or a web UI. It was built as part of the CP352301 Script Programming mini project and now includes persistent statistics, a 30-second challenge mode, and improved word-based scoring.

---

## Features
- Random prompt selection from `prompts.json`
- Shared word-by-word accuracy and character-level metrics
- Words Per Minute (WPM) calculation using the 5-char standard
- 30-second challenge mode that reuses the last prompt for record attempts
- Automatic result tracking in `stats.json` with summary and history views
- Streamlit interface that mirrors the CLI capabilities
- Graceful handling of `Ctrl+C` in the CLI to return to the menu

---

## Project Structure
```text
Typing-Test-CLI/
├─ App/
│  └─ main_app.py            # Streamlit app
├─ docs/
│  ├─ PLAN.md
│  └─ PROGRESS.md
├─ src/typing_test/
│  ├─ data/
│  │  ├─ prompts.json
│  │  └─ script_sort_jsonPrompts.py
│  ├─ __init__.py
│  ├─ main.py                # CLI entry point
│  ├─ metrics.py             # Shared typing metrics helper
│  ├─ prompt_source.py
│  ├─ stats_store.py         # Stats persistence helpers
│  ├─ textbank.py
│  └─ typing_calculate.py
├─ requirements.txt
├─ pyproject.toml
└─ README.md
```

---

## Installation
```bash
git clone https://github.com/pavarit548x/Typing-Test-CLI.git
cd Typing-Test-CLI

python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
# or install the package in editable mode
pip install -e .
```

---

## Running the CLI
```bash
python src/typing_test/main.py
```
Menu options:
- `1` – Normal mode (shuffle a new prompt)
- `2` – 30-second challenge mode using the last prompt
- `3` – View saved statistics
- `4` – Quit

The CLI measures your typing session, reports WPM and word-based accuracy, and stores the result in `stats.json` unless the 30-second timer expires in challenge mode.

---

## Running the Streamlit App
```bash
streamlit run App/main_app.py
```
Open http://localhost:8501 and you will find two tabs:
- **Typing** – Run either the normal or 30-second challenge mode. Results show matched words, accuracy, elapsed time, and WPM.
- **Statistics** – View aggregated metrics, best records, and the latest sessions.

The Streamlit experience uses the same metrics and persistence layer as the CLI, so all results are shared automatically.

---

## Typing Statistics
- Results are stored in `src/typing_test/data/stats.json` by default.
- Set the `TYPING_STATS_PATH` environment variable to choose a custom location.
- The statistics viewer summarises averages, best records, and recent sessions, including matched word counts.

---

## Prompt Configuration
By default prompts are loaded from `src/typing_test/data/prompts.json`. You can customise this behaviour with environment variables:
- `PROMPT_JSON_PATH` – Absolute or relative path to an alternate JSON file
- `PROMPT_TAG` – Filter prompts by tag when using the structured JSON schema

---

## Keyboard Shortcuts & Tips
- Press `Ctrl+C` in the CLI at any time to cancel the current action and return to the menu safely.
- In the Streamlit app, use `Enter` (or `Ctrl+Enter`) in the text area to submit the prompt immediately.
- Challenge mode only saves results that finish within 30 seconds, helping you focus on personal best runs.

Enjoy improving your typing speed!
