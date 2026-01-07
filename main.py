from brain import ask_ai

print("🤖 Shakshi: Hello Vijay! Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("🤖 Shakshi: Bye! See you soon 🚀")
        break

    reply = ask_ai(user_input)
    print("🤖 Shakshi:", reply)
