from textbank import all_text

while True:
  print("\n-- Menu --")
  print("1. Typing Speed Test 15 Seconds")
  print("2. Typing Speed Test 30 Seconds")
  print("3. Typing Speed Test 1 Minute")
  print("4. Exit Program")

  choice = input("Please select an option (1-4): ")

  if choice == "1":
    print("\n[Typing Speed Test 15 Seconds Starting...]")

    print("[Typing Test Finished! Returning to Menu...]")

  elif choice == "2":
    print("\n[Typing Speed Test 30 Seconds Starting...]")

    print("[Typing Test Finished! Returning to Menu...]")

  elif choice == "3":
    
    print("[Typing Test Finished! Returning to Menu...]")

  elif choice == "4":
    print("\nExiting Program...")
    break

  else:
    print("\nPlease Input The Required Number")
