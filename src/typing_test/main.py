from __future__ import annotations

from datetime import datetime
import time
from prompt_source import get_random_prompt   # dataset of sentences
from stats_store import (
    append_stat,
    create_stat_record,
    load_stats,
    recent_stats,
    summarize_stats,
)
from typing_calculate import calc_accuracy_pct, calc_wpm_char5  # calculation functions
try:
    from metrics import compute_metrics
except ImportError:  # pragma: no cover
    from typing_test.metrics import compute_metrics  # type: ignore

CHALLENGE_TIME_LIMIT = 30.0  # seconds


def _format_timestamp(value: str | None) -> str:
  if not value:
    return "-"
  try:
    dt = datetime.fromisoformat(value)
    return dt.astimezone().strftime("%Y-%m-%d %H:%M")
  except ValueError:
    return value


def _safe_float(value, digits: int = 2) -> float:
  try:
    return round(float(value), digits)
  except (TypeError, ValueError):
    return 0.0





def _run_typing_session(prompt: str, *, mode: str, time_limit: float | None = None) -> bool:
  print("\nPress Enter to START timing...")
  if time_limit is not None:
    print(f"You have {time_limit:.0f} seconds to submit once the timer starts.")
  input("")
  t0 = time.perf_counter()

  print("Type the prompt and press enter to SUBMIT:")
  user_input = input(">> ")
  time_counter = time.perf_counter() - t0

  metrics = compute_metrics(prompt, user_input)

  typing_accuracy = calc_accuracy_pct(metrics["word_correct"], metrics["word_total"])
  typing_WPM = calc_wpm_char5(len(user_input), time_counter)

  print("\n[Result]")
  print(f" Time: {time_counter:.2f} s")
  print(f" Accuracy (word-based): {typing_accuracy} %")
  print(f" Words Per Minute (WPM): {typing_WPM}")
  if metrics["word_total"] > 0:
    print(
      f" Matched words: {metrics['word_correct']} / {metrics['word_total']}"
    )

  if time_limit is not None and time_counter > time_limit:
    print(f" Exceeded the {time_limit:.0f}-second limit. Result not saved.")
    return False

  record = create_stat_record(
    duration_sec=time_counter,
    accuracy_pct=typing_accuracy,
    wpm=typing_WPM,
    prompt_length=len(prompt),
    input_length=len(user_input),
    correct_chars=metrics["char_correct"],
    char_total=metrics["char_total"],
    incorrect_chars=metrics["char_incorrect"],
    prompt=prompt,
    mode=mode,
    correct_words=metrics["word_correct"],
    incorrect_words=metrics["word_incorrect"],
    word_total=metrics["word_total"],
    prompt_word_count=metrics["prompt_word_count"],
    input_word_count=metrics["input_word_count"],
  )
  append_stat(record)
  total_sessions = len(load_stats())
  print(f" Saved! Total recorded sessions: {total_sessions}")
  return True


print("=== Typing Speed Meter (Batch) ===")
print("Hi! This program measures your typing speed and accuracy.")

last_prompt: str | None = None

while True:
  # --- Menu ---
  print("\n-- Menu --")
  print("1. Shuffle a prompt (normal mode)")
  print("2. Break the record (30s challenge)")
  print("3. View statistics")
  print("4. Quit")
  
  try:
    choice = input("Please select an option (1-4): ")
  
    if choice == "1": 
      # === Step 1: Generate random prompt ===
      print("\nPrompt selected:")
      random_sentence = get_random_prompt()
      last_prompt = random_sentence
      print("   " + random_sentence)

      _run_typing_session(random_sentence, mode="standard")

    elif choice == "2":
      if not last_prompt:
        print("\nNo previous prompt available. Run option 1 once to set a challenge sentence.")
        continue

      print("\n[Challenge Mode]")
      print("Using your last prompt. No shuffling allowed!")
      print("   " + last_prompt)
      _run_typing_session(last_prompt, mode="challenge", time_limit=CHALLENGE_TIME_LIMIT)

    elif choice == "3":
      stats = load_stats()
      if not stats:
        print("\nNo typing sessions recorded yet. Run option 1 to create your first result.")
        continue

      summary = summarize_stats(stats)

      print("\n[Statistics]")
      print(f" Sessions recorded: {summary['total_sessions']}")
      print(f" Average WPM: {summary['avg_wpm']}")
      print(f" Average accuracy: {summary['avg_accuracy']} %")
      if summary['best_wpm'] is not None:
        print(
          f" Best WPM: {summary['best_wpm']} (on {_format_timestamp(summary['best_wpm_timestamp'])})"
        )
      if summary['best_accuracy'] is not None:
        print(
          f" Best accuracy: {summary['best_accuracy']} % (on {_format_timestamp(summary['best_accuracy_timestamp'])})"
        )

      recent = recent_stats(stats, limit=5)
      if recent:
        print("\nRecent sessions (newest first):")
        for entry in reversed(recent):
          ts = _format_timestamp(entry.get("timestamp"))
          wpm_display = _safe_float(entry.get("wpm"))
          accuracy_display = _safe_float(entry.get("accuracy_pct"))
          duration_display = _safe_float(entry.get("duration_sec"))
          mode_display = (entry.get("mode") or "standard").lower()
          prompt_text = (entry.get("prompt") or "").replace("\n", " ")
          if len(prompt_text) > 60:
            prompt_text = prompt_text[:57] + "..."
          detail_parts = [
            f"Mode {mode_display}",
            f"WPM {wpm_display}",
            f"Accuracy {accuracy_display}%",
            f"Time {duration_display:.2f}s",
          ]
          total_words = entry.get('word_total')
          if total_words is None:
            total_words = (entry.get('correct_words') or 0) + (entry.get('incorrect_words') or 0)
          correct_words = entry.get('correct_words')
          if total_words and correct_words is not None:
            detail_parts.append(
              f"Words {int(correct_words)}/{int(total_words)}"
            )
          print(f" {ts} | " + " | ".join(detail_parts))
          if prompt_text:
            print(f"    Prompt: {prompt_text}")

    elif choice == "4":
      # Exit program
      print("\nExiting Program...")
      break

    else:
      # Invalid input
      print("\nUnknown command. Please choose 1, 2, 3 or 4.")
      
  except KeyboardInterrupt:
      # Handle Ctrl+C -> return to menu safely
      print("\n(Cancelled) Returning to main menu...\n")
      continue
  


