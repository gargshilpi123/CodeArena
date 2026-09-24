import subprocess
import tempfile
import os
import time


def normalize_output(output: str):

    return " ".join(
        output.strip().split()
    )


def run_code(
    code: str,
    language: str,
    test_cases
):

    language = language.lower()

    if language not in ["cpp", "python"]:

        return {
            "status": "Unsupported Language",
            "passed": 0,
            "total": len(test_cases),
            "runtime": "0 ms"
        }

    passed = 0

    total = len(test_cases)

    start = time.perf_counter()

    with tempfile.TemporaryDirectory() as temp_dir:

        if language == "cpp":

            source = os.path.join(
                temp_dir,
                "solution.cpp"
            )

            executable = os.path.join(
                temp_dir,
                "solution.exe"
            )

            with open(
                source,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(code)

            compile_result = subprocess.run(
                [
                    "g++",
                    source,
                    "-O2",
                    "-std=c++17",
                    "-o",
                    executable
                ],
                capture_output=True,
                text=True,
                timeout=10
            )

            if compile_result.returncode != 0:

                return {
                    "status": "Compilation Error",
                    "passed": 0,
                    "total": total,
                    "runtime": "0 ms",
                    "error": compile_result.stderr
                }

            command = [executable]

        else:

            source = os.path.join(
                temp_dir,
                "solution.py"
            )

            with open(
                source,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(code)

            command = [
                "python",
                source
            ]

        for testcase in test_cases:

            try:

                result = subprocess.run(
                    command,
                    input=testcase.input,
                    capture_output=True,
                    text=True,
                    timeout=2
                )

            except subprocess.TimeoutExpired:

                return {
                    "status": "Time Limit Exceeded",
                    "passed": passed,
                    "total": total,
                    "runtime": "2000+ ms"
                }

            if result.returncode != 0:

                return {
                    "status": "Runtime Error",
                    "passed": passed,
                    "total": total,
                    "runtime": f"{int((time.perf_counter() - start) * 1000)} ms",
                    "error": result.stderr
                }

            actual = normalize_output(
                result.stdout
            )

            expected = normalize_output(
                testcase.expected_output
            )

            if actual != expected:

                return {
                    "status": "Wrong Answer",
                    "passed": passed,
                    "total": total,
                    "runtime": f"{int((time.perf_counter() - start) * 1000)} ms"
                }

            passed += 1

    runtime = int(
        (time.perf_counter() - start) * 1000
    )

    return {
        "status": "Accepted",
        "passed": passed,
        "total": total,
        "runtime": f"{runtime} ms"
    }