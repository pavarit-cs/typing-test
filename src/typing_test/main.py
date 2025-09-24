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


print("=== Typing Speed Meter (Batch) ===")
print("Hi! This program measures your typing speed and accuracy.")

while True:
  # --- Menu ---
  print("\n-- Menu --")
  print("1. Shuffle a prompt")
  print("2. View statistics")
  print("3. Quit")
  
  try:
    choice = input("Please select an option (1-3): ")
  
    if choice == "1": 
      # === Step 1: Generate random prompt ===
      print("\nPrompt selected:")
      random_sentence = get_random_prompt()
      print("   " + random_sentence)

      # === Step 2: Start typing test ===
      print("\nPress Enter to START timing...")
      input("")
      t0 = time.perf_counter()  # start timer
       
      print("Type the prompt and press enter to SUBMIT:")
      user_input = input(">> ")
      time_counter = time.perf_counter() - t0  # stop timer
      
      # === Step 3: Compare characters ===
      correct_count = 0
      incorrect_count = 0
      length_prompt = len(random_sentence)
      length_user_input = len(user_input)
      N = max(length_prompt, length_user_input)
      
      for i in range(N):
        p_char = random_sentence[i] if i < length_prompt else ""
        u_char = user_input[i] if i < length_user_input else ""
        if p_char == u_char:
          correct_count += 1
        else:
          incorrect_count += 1
          
      # === Step 4: Calculate results ===
      typing_accuracy = calc_accuracy_pct(correct_count, N)
      typing_WPM = calc_wpm_char5(length_user_input, time_counter)
      
      # === Step 5: Show summary ===
      print("\n[Result]")
      print(f" Time: {time_counter:.2f} s")
      print(f" Accuracy: {typing_accuracy} %")
      print(f" Words Per Minute (WPM): {typing_WPM}")

      record = create_stat_record(
        duration_sec=time_counter,
        accuracy_pct=typing_accuracy,
        wpm=typing_WPM,
        prompt_length=length_prompt,
        input_length=length_user_input,
        correct_chars=correct_count,
        incorrect_chars=incorrect_count,
        prompt=random_sentence,
      )
      append_stat(record)
      total_sessions = len(load_stats())
      print(f" Saved! Total recorded sessions: {total_sessions}")

    elif choice == "2":
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
          prompt_text = (entry.get("prompt") or "").replace("\n", " ")
          if len(prompt_text) > 60:
            prompt_text = prompt_text[:57] + "..."
          print(
            f" {ts} | WPM {wpm_display} | Accuracy {accuracy_display}% | Time {duration_display:.2f}s"
          )
          if prompt_text:
            print(f"    Prompt: {prompt_text}")

    elif choice == "3":
      # Exit program
      print("\nExiting Program...")
      break

    else:
      # Invalid input
      print("\nUnknown command. Please choose 1, 2 or 3.")
      
  except KeyboardInterrupt:
      # Handle Ctrl+C -> return to menu safely
      print("\n(Cancelled) Returning to main menu...\n")
      continue
  
