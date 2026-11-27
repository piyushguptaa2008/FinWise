
import json
from pathlib import Path
from datetime import datetime, timezone
from uuid import uuid4


class ApprovalManager:

    def __init__(self):
        self.proposals = {}
        self.history = []

    def create_proposal(self, action, details):
        proposal_id = str(uuid4())

        proposal = {
            "id": proposal_id,
            "action": action,
            "details": details,
            "status": "pending",
            "created_at": datetime.now(timezone.utc).isoformat()
        }

        self.proposals[proposal_id] = proposal

        return proposal.copy()

    def approve(self, proposal_id):
        proposal = self.proposals.get(proposal_id)

        if proposal is None:
            return {"error": "Proposal not found."}

        if proposal["status"] != "pending":
            return {"error": "Proposal already reviewed."}

        approved = {
            **proposal,
            "status": "approved",
            "reviewed_at": datetime.now(timezone.utc).isoformat()
        }

        folder = Path("approved_plans")
        folder.mkdir(exist_ok=True)

        file_path = folder / f"{proposal_id}.json"

        with file_path.open("x", encoding="utf-8") as file:
            json.dump(approved, file, indent=4)

        self.proposals[proposal_id] = approved
        self.history.append(approved.copy())

        return approved.copy()

    def reject(self, proposal_id):
        proposal = self.proposals.get(proposal_id)

        if proposal is None:
            return {"error": "Proposal not found."}

        if proposal["status"] != "pending":
            return {"error": "Proposal already reviewed."}

        proposal["status"] = "rejected"
        proposal["reviewed_at"] = (
            datetime.now(timezone.utc).isoformat()
        )

        self.history.append(proposal.copy())

        return proposal.copy()

    def get_pending(self):
        return [
            proposal.copy()
            for proposal in self.proposals.values()
            if proposal["status"] == "pending"
        ]

    def get_history(self):
        return [item.copy() for item in self.history]


if __name__ == "__main__":
    manager = ApprovalManager()

    proposal = manager.create_proposal(
        "Save budget plan",
        {
            "monthly_income": 10000,
            "planned_expenses": 6750,
            "remaining_balance": 3250
        }
    )

    print("Proposal created:")
    print(json.dumps(proposal, indent=4))

    choice = input("\nApprove this plan? (yes/no): ")

    if choice.strip().lower() == "yes":
        result = manager.approve(proposal["id"])
    else:
        result = manager.reject(proposal["id"])

    print("\nFinal result:")
    print(json.dumps(result, indent=4))
