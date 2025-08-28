from textbank import all_text   # dataset of sentences
from typing_calculate import calc_accuracy_pct, calc_wpm_char5  # calculation functions
import random                   # for random prompt selection
import time                     # for timing

print("=== Typing Speed Meter (Batch) ===")
print("Hi! This program measures your typing speed and accuracy.")

while True:
  # --- Menu ---
  print("\n-- Menu --")
  print("1. Shuffle a prompt")
  print("2. Quit")
  
  try:
    choice = input("Please select an option (1-2): ")
  
    if choice == "1": 
      # === Step 1: Generate random prompt ===
      print("\nPrompt selected:")
      random_sentence = random.choice(all_text)
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
      typing_WPM = calc_wpm_char5(N, time_counter)
      
      # === Step 5: Show summary ===
      print("\n[Result]")
      print(f" Time: {time_counter:.2f} s")
      print(f" Accuracy: {typing_accuracy} %")
      print(f" Words Per Minute (WPM): {typing_WPM}")

    elif choice == "2":
      # Exit program
      print("\nExiting Program...")
      break

    else:
      # Invalid input
      print("\nUnknown command. Please choose 1 or 2.")
      
  except KeyboardInterrupt:
      # Handle Ctrl+C → return to menu safely
      print("\n(Cancelled) Returning to main menu...\n")
      continue
