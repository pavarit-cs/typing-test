from textbank import all_text   # import sentence dataset
import random                   # import random for shuffle
import time

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
      # --- Generate random prompt ---
      print("\nPrompt selected:")
      random_sentence = random.choice(all_text)
      print("   " + random_sentence)

      # --- Start typing test ---
      print("\nPress Enter to START timing...")
      input("")
      t0 = time.perf_counter()
       
      print("Type the prompt and press enter to SUBMIT:")
      user_input = input(">> ")
      time_counter = time.perf_counter() - t0
      
      
      # --- Compare characters one by one ---
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
          
      # --- Show result ---
      print("\nCorrect:", correct_count, "Incorrect:", incorrect_count, "Time:", time_counter)

    elif choice == "2":
      print("\nExiting Program...")
      break

    else:
      print("\nUnknown command. Please choose 1 or 2.")
      
  except KeyboardInterrupt:
      # return to menu if user presses Ctrl+C
      print("\n(Cancelled) Returning to main menu...\n")
      continue
