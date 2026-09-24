from openai import OpenAI

import os
import json

from dotenv import load_dotenv


load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def review_code(
    problem_title,
    problem_description,
    difficulty,
    topic,
    language,
    code,
    judge_status
):

    prompt = f"""
You are an expert coding interview reviewer.

Analyze the submitted solution carefully.

Problem:
{problem_title}

Description:
{problem_description}

Difficulty:
{difficulty}

Topic:
{topic}

Programming Language:
{language}

Judge Result:
{judge_status}

Submitted Code:
```{language}
{code}