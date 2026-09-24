from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from ..database import get_db

from ..models import (
    Problem,
    Submission
)

from ..schemas import SubmissionCreate

from ..auth import get_current_user

from ..judge import run_code


router = APIRouter(
    prefix="/submissions",
    tags=["Submissions"]
)


@router.post("/")
def submit(
    data: SubmissionCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    problem = db.query(Problem).filter(
        Problem.id == data.problem_id
    ).first()

    if not problem:

        raise HTTPException(
            status_code=404,
            detail="Problem not found"
        )

    if data.language.lower() not in [
        "cpp",
        "python"
    ]:

        raise HTTPException(
            status_code=400,
            detail="Only C++ and Python are currently supported"
        )

    test_cases = problem.test_cases

    if not test_cases:

        raise HTTPException(
            status_code=400,
            detail="No test cases found"
        )

    result = run_code(
        data.code,
        data.language,
        test_cases
    )

    submission = Submission(
        user_id=user.id,
        problem_id=problem.id,
        code=data.code,
        language=data.language.lower(),
        status=result["status"],
        passed=result["passed"],
        total=result["total"],
        runtime=result["runtime"]
    )

    db.add(submission)
    db.commit()
    db.refresh(submission)

    return {
        "submission_id": submission.id,
        "status": result["status"],
        "passed": result["passed"],
        "total": result["total"],
        "runtime": result["runtime"]
    }


@router.get("/history")
def history(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    submissions = db.query(
        Submission
    ).filter(
        Submission.user_id == user.id
    ).order_by(
        Submission.submitted_at.desc()
    ).all()

    return [
        {
            "id": s.id,
            "problem_id": s.problem_id,
            "language": s.language,
            "status": s.status,
            "passed": s.passed,
            "total": s.total,
            "runtime": s.runtime,
            "submitted_at": s.submitted_at
        }

        for s in submissions
    ]