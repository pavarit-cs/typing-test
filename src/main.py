from textbank import all_text
print("=== Typing Speed Meter (Batch) ===")
print("Hi! This program measures your typing speed and accuracy.")
while True:
  print("\n-- Menu --")
  print("1. Shuffle a prompt")
  print("2. Quit")

  choice = input("Please select an option (1-2): ")

  if choice == "1":
    print("\nPrompt selected:")
    print("Consistent practice improves both speed and accuracy.")
    print("\nPress Enter to START timing...")
    user_input = input("")
    print("\nType the prompt and press enter to SUBMIT:")
    user_input = input(">> ")

  elif choice == "2":
    print("\nExiting Program...")
    break

  else:
    print("\nPlease Input The Required Number")
