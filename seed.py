from app.database import SessionLocal, engine, Base

from app.models import Problem, TestCase


Base.metadata.create_all(
    bind=engine
)


db = SessionLocal()


questions = [

    {
        "title": "Two Sum",
        "description": """
Given an array of integers and a target,
print the indices of two numbers whose sum
equals the target.

For this platform, print the two indices
separated by a space.
""",
        "difficulty": "Easy",
        "topic": "Array",
        "constraints": """
2 <= n <= 10000
""",
        "tests": [
            ("4\n2 7 11 15\n9", "0 1"),
            ("3\n3 2 4\n6", "1 2"),
            ("2\n3 3\n6", "0 1")
        ]
    },

    {
        "title": "Maximum Element",
        "description": """
Given an array of integers, print the
maximum element.
""",
        "difficulty": "Easy",
        "topic": "Array",
        "constraints": """
1 <= n <= 100000
""",
        "tests": [
            ("5\n1 5 3 9 2", "9"),
            ("4\n10 2 7 3", "10"),
            ("3\n-5 -2 -9", "-2")
        ]
    },

    {
        "title": "Palindrome Number",
        "description": """
Given an integer n, print YES if it is a
palindrome, otherwise print NO.
""",
        "difficulty": "Easy",
        "topic": "Math",
        "constraints": """
0 <= n <= 1000000000
""",
        "tests": [
            ("121", "YES"),
            ("123", "NO"),
            ("1221", "YES")
        ]
    },

    {
        "title": "Binary Search",
        "description": """
Given a sorted array and a target value,
print the index of the target.
Print -1 if it does not exist.
""",
        "difficulty": "Medium",
        "topic": "Binary Search",
        "constraints": """
Array is sorted in ascending order.
""",
        "tests": [
            ("5\n1 3 5 7 9\n7", "3"),
            ("5\n1 3 5 7 9\n4", "-1"),
            ("6\n2 4 6 8 10 12\n10", "4")
        ]
    },

    {
        "title": "Count Vowels",
        "description": """
Given a string, print the number of vowels
in the string.
""",
        "difficulty": "Easy",
        "topic": "String",
        "constraints": """
String contains lowercase English letters.
""",
        "tests": [
            ("hello", "2"),
            ("leetcode", "4"),
            ("python", "1")
        ]
    }

]


for data in questions:

    existing = db.query(Problem).filter(
        Problem.title == data["title"]
    ).first()

    if existing:
        continue

    problem = Problem(
        title=data["title"],
        description=data["description"].strip(),
        difficulty=data["difficulty"],
        topic=data["topic"],
        constraints=data["constraints"].strip()
    )

    db.add(problem)
    db.commit()
    db.refresh(problem)

    for input_data, output_data in data["tests"]:

        testcase = TestCase(
            problem_id=problem.id,
            input=input_data,
            expected_output=output_data
        )

        db.add(testcase)

    db.commit()


db.close()

print("Questions added successfully!")