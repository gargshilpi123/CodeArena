from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from ..database import get_db

from ..models import Submission

from ..auth import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me")
def profile(
    user=Depends(get_current_user)
):

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at
    }


@router.get("/progress")
def progress(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    submissions = db.query(
        Submission
    ).filter(
        Submission.user_id == user.id
    ).all()

    accepted = [
        s for s in submissions
        if s.status == "Accepted"
    ]

    solved = set(
        s.problem_id
        for s in accepted
    )

    return {
        "total_submissions": len(submissions),
        "accepted_submissions": len(accepted),
        "problems_solved": len(solved)
    }