from agents import run_agent


def main():
    print("=" * 40)
    print("FinWise - Personal Finance Agent")
    print("=" * 40)

    while True:
        question = input("\nAsk FinWise: ")

        if question.lower().strip() == "exit":
            print("Thank you for using FinWise!")
            break

        if not question.strip():
            continue

        try:
            response = run_agent(question)
            print("\nFinWise:", response)

        except Exception as error:
            print("\nError:", error)


if __name__ == "__main__":
    main()
