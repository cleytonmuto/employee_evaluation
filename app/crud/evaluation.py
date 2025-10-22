# app/crud/evaluation.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.evaluation import Evaluation
from app.models.user import User
from uuid import UUID

def create_evaluation(db: Session, evaluator: User, evaluated_id: UUID, score: int, comments: str | None = None) -> Evaluation:
    evaluated = db.query(User).filter(User.id == evaluated_id).first()
    if evaluated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evaluated user not found")

    if evaluator.id == evaluated.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot evaluate yourself")

    # Enforce same-sector rule for non-admin evaluators
    if evaluator.role.name != "admin":
        if evaluator.sector_id is None or evaluated.sector_id is None or evaluator.sector_id != evaluated.sector_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You may only evaluate employees in your sector")

    ev = Evaluation(
        evaluator_id=evaluator.id,
        evaluated_id=evaluated.id,
        sector_id=evaluated.sector_id,
        score=score,
        comments=comments
    )
    db.add(ev)
    db.commit()
    db.refresh(ev)
    return ev

def get_evaluation(db: Session, eval_id: UUID):
    return db.query(Evaluation).filter(Evaluation.id == eval_id).first()

def list_evaluations(db: Session, *, current_user: User, skip: int = 0, limit: int = 100):
    query = db.query(Evaluation)
    if current_user.role.name == "admin":
        return query.offset(skip).limit(limit).all()
    # employees: evaluations within their sector only
    return query.filter(Evaluation.sector_id == current_user.sector_id).offset(skip).limit(limit).all()

def delete_evaluation(db: Session, ev: Evaluation):
    db.delete(ev)
    db.commit()
