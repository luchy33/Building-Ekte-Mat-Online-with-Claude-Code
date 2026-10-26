from datetime import datetime

from app.models.question import Question
from app.models.repositories.db import get_db


class QuestionRepository:
    def add(self, question: Question) -> Question:
        db = get_db()
        cur = db.execute(
            "INSERT INTO question (customer_id, name, email, subject, body, answer, created_at, answered_at)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (question.customer_id, question.name, question.email, question.subject, question.body,
             question.answer, question.created_at.isoformat(timespec="seconds"),
             question.answered_at.isoformat(timespec="seconds") if question.answered_at else None),
        )
        db.commit()
        question.id = cur.lastrowid
        return question

    def list_all(self) -> list[Question]:
        rows = get_db().execute("SELECT * FROM question ORDER BY created_at DESC").fetchall()
        return [self._to_question(r) for r in rows]

    @staticmethod
    def _to_question(row) -> Question:
        return Question(
            id=row["id"],
            customer_id=row["customer_id"],
            name=row["name"],
            email=row["email"],
            subject=row["subject"],
            body=row["body"],
            answer=row["answer"],
            created_at=datetime.fromisoformat(row["created_at"]),
            answered_at=datetime.fromisoformat(row["answered_at"]) if row["answered_at"] else None,
        )
