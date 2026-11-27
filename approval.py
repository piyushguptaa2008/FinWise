
import json
import sqlite3

from pathlib import Path
from datetime import datetime, timezone
from uuid import uuid4


class ApprovalManager:

    def __init__(self, persistent=False):

        self.persistent = persistent

        database = (
            "approval_history.db"
            if persistent else ":memory:"
        )

        self.connection = sqlite3.connect(
            database,
            check_same_thread=False
        )

        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS proposals (
                id TEXT PRIMARY KEY,
                action TEXT NOT NULL,
                details TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                reviewed_at TEXT
            )
        """)

        self.connection.commit()


    def create_proposal(self, action, details):

        proposal = {
            "id": str(uuid4()),
            "action": action,
            "details": details,
            "status": "pending",
            "created_at": datetime.now(
                timezone.utc
            ).isoformat()
        }

        with self.connection:

            self.connection.execute("""
                INSERT INTO proposals (
                    id, action, details,
                    status, created_at
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                proposal["id"],
                proposal["action"],
                json.dumps(proposal["details"]),
                proposal["status"],
                proposal["created_at"]
            ))

        return proposal


    def get_proposal(self, proposal_id):

        row = self.connection.execute("""
            SELECT id, action, details,
                   status, created_at, reviewed_at
            FROM proposals
            WHERE id = ?
        """, (proposal_id,)).fetchone()

        if row is None:
            return None

        return self.format_row(row)


    def format_row(self, row):

        proposal = {
            "id": row[0],
            "action": row[1],
            "details": json.loads(row[2]),
            "status": row[3],
            "created_at": row[4]
        }

        if row[5] is not None:
            proposal["reviewed_at"] = row[5]

        return proposal


    def review(self, proposal_id, status):

        reviewed_at = datetime.now(
            timezone.utc
        ).isoformat()

        with self.connection:

            cursor = self.connection.execute("""
                UPDATE proposals
                SET status = ?, reviewed_at = ?
                WHERE id = ? AND status = 'pending'
            """, (
                status,
                reviewed_at,
                proposal_id
            ))

            if cursor.rowcount == 0:

                proposal = self.get_proposal(proposal_id)

                if proposal is None:
                    return {"error": "Proposal not found."}

                return {
                    "error": "Proposal already reviewed."
                }

        return self.get_proposal(proposal_id)


    def approve(self, proposal_id):

        result = self.review(
            proposal_id,
            "approved"
        )

        if "error" in result:
            return result

        if self.persistent:

            folder = Path("approved_plans")

            folder.mkdir(exist_ok=True)

            file_path = folder / f"{proposal_id}.json"

            try:

                with file_path.open(
                    "x",
                    encoding="utf-8"
                ) as file:

                    json.dump(result, file, indent=4)

            except OSError as error:

                result["export_warning"] = str(error)

        return result


    def reject(self, proposal_id):

        return self.review(
            proposal_id,
            "rejected"
        )


    def get_pending(self):

        rows = self.connection.execute("""
            SELECT id, action, details,
                   status, created_at, reviewed_at
            FROM proposals
            WHERE status = 'pending'
            ORDER BY created_at DESC
        """).fetchall()

        return [
            self.format_row(row)
            for row in rows
        ]


    def get_history(self):

        rows = self.connection.execute("""
            SELECT id, action, details,
                   status, created_at, reviewed_at
            FROM proposals
            WHERE status IN ('approved', 'rejected')
            ORDER BY reviewed_at DESC
        """).fetchall()

        return [
            self.format_row(row)
            for row in rows
        ]


    def close(self):

        self.connection.close()
