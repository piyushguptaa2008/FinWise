
import json
from agents import run_agent
from approval import ApprovalManager

manager = ApprovalManager()

print("=" * 45)
print("FinWise - AI Personal Finance Agent")
print("=" * 45)
print("Type 'exit' to quit.")
print("Type 'history' to view reviewed plans.")

while True:
    question = input("\nAsk FinWise: ").strip()

    if question.lower() == "exit":
        print("Thank you for using FinWise!")
        break

    if question.lower() == "history":
        print(json.dumps(manager.get_history(), indent=4))
        continue

    if not question:
        continue

    try:
        result = run_agent(question, return_trace=True)

        print("\nFinWise:", result["answer"])

        if "create_budget_plan" in result["tools_used"]:

            proposal = manager.create_proposal(
                "Save budget plan",
                {
                    "request": question,
                    "recommendation": result["answer"]
                }
            )

            print("\n--- Human Approval Required ---")
            print("Action: Save proposed budget plan")

            choice = input(
                "Approve this plan? (yes/no): "
            ).strip().lower()

            if choice == "yes":
                decision = manager.approve(proposal["id"])
            else:
                decision = manager.reject(proposal["id"])

            print("Status:", decision.get("status", decision.get("error")))

    except Exception as error:
        print("Error:", error)
