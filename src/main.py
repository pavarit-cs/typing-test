from textbank import all_text
import random
print("=== Typing Speed Meter (Batch) ===")
print("Hi! This program measures your typing speed and accuracy.")
while True:
  print("\n-- Menu --")
  print("1. Shuffle a prompt")
  print("2. Quit")

  choice = input("Please select an option (1-2): ")

  if choice == "1": 
    print("\nPrompt selected:")
    # *** Random sentence ***
    random_sentence = random.choice(all_text) # Normal random it can be same sentence.
    # random_sentence = random.shuffle(all_text) -> It can't be same sentence.
    print(random_sentence)
    print("\nPress Enter to START timing...")
    user_input = input("")
    print("\nType the prompt and press enter to SUBMIT:")
    user_input = input(">> ")
    correct_count = 0
    incorrect_count = 0
    # *** it check only correct and incorrect. If error out of range because: you input more or less than random text ***
    for char in range(len(random_sentence) - 1):
      if user_input[char] == random_sentence[char]:
        correct_count += 1
      else:
        incorrect_count += 1
    print("Correct :",correct_count,"Incorrect :",incorrect_count)



  elif choice == "2":
    print("\nExiting Program...")
    break

  else:
    print("\nPlease Input The Required Number")
