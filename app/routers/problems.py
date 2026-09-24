from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from ..database import get_db

from ..models import Problem, TestCase

from ..schemas import (
    ProblemCreate,
    ProblemResponse,
    TestCaseCreate
)

from ..auth import get_current_user


router = APIRouter(
    prefix="/problems",
    tags=["Problems"]
)


@router.post(
    "/",
    response_model=ProblemResponse
)
def create_problem(
    data: ProblemCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    problem = Problem(
        title=data.title,
        description=data.description,
        difficulty=data.difficulty,
        topic=data.topic,
        constraints=data.constraints
    )

    db.add(problem)
    db.commit()
    db.refresh(problem)

    return problem


@router.get(
    "/",
    response_model=list[ProblemResponse]
)
def get_problems(
    difficulty: str | None = None,
    topic: str | None = None,
    db: Session = Depends(get_db)
):

    query = db.query(Problem)

    if difficulty:

        query = query.filter(
            Problem.difficulty == difficulty
        )

    if topic:

        query = query.filter(
            Problem.topic == topic
        )

    return query.order_by(
        Problem.id
    ).all()


@router.get(
    "/{problem_id}",
    response_model=ProblemResponse
)
def get_problem(
    problem_id: int,
    db: Session = Depends(get_db)
):

    problem = db.query(Problem).filter(
        Problem.id == problem_id
    ).first()

    if not problem:

        raise HTTPException(
            status_code=404,
            detail="Problem not found"
        )

    return problem


@router.post(
    "/{problem_id}/testcases"
)
def add_testcase(
    problem_id: int,
    data: TestCaseCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    problem = db.query(Problem).filter(
        Problem.id == problem_id
    ).first()

    if not problem:

        raise HTTPException(
            status_code=404,
            detail="Problem not found"
        )

    testcase = TestCase(
        problem_id=problem_id,
        input=data.input,
        expected_output=data.expected_output
    )

    db.add(testcase)
    db.commit()
    db.refresh(testcase)

    return {
        "message": "Test case created",
        "id": testcase.id
    }