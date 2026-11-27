
import json

from agents import run_agent
from approval import ApprovalManager


manager = ApprovalManager(persistent=True)

print("=" * 45)
print("FinWise - AI Personal Finance Agent")
print("=" * 45)

print("Type 'exit' to quit.")
print("Type 'history' to view reviewed plans.")


while True:

    question = input("\nAsk FinWise: ").strip()

    if question.lower() == "exit":

        manager.close()

        print("Thank you for using FinWise!")

        break

    if question.lower() == "history":

        history = manager.get_history()

        if not history:

            print("No reviewed plans yet.")

        else:

            print(json.dumps(history, indent=4))

        continue

    if not question:
        continue

    try:

        result = run_agent(
            question,
            return_trace=True
        )

        print("\nFinWise:", result["answer"])

        if (
            result["validated"]
            and "create_budget_plan" in result["tools_used"]
        ):

            proposal = manager.create_proposal(
                "Save budget plan",
                {
                    "request": question,
                    "recommendation": result["answer"]
                }
            )

            print("\n--- Human Approval Required ---")
            print("Action: Save proposed budget plan")

            while True:

                choice = input(
                    "Approve this plan? (yes/no): "
                ).strip().lower()

                if choice == "yes":

                    decision = manager.approve(
                        proposal["id"]
                    )

                    break

                elif choice == "no":

                    decision = manager.reject(
                        proposal["id"]
                    )

                    break

                else:

                    print("Please enter yes or no.")

            print(
                "Status:",
                decision.get(
                    "status",
                    decision.get("error")
                )
            )

            if "export_warning" in decision:

                print(
                    "Export warning:",
                    decision["export_warning"]
                )

    except Exception as error:

        print("Error:", error)
