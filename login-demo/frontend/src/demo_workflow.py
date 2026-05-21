import os

# Root project folder
root_folder = "login-demo"

# Subfolders
folders = [
    f"{root_folder}/backend",
    f"{root_folder}/frontend",
    f"{root_folder}/frontend/src"
]

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

print("Project structure created successfully.")
print("""
login-demo/
├── backend/
├── frontend/
│   └── src/
""")
prd_content = """
# Login and Registration System PRD

## 1. Project Overview

This system provides basic user registration and login functions. Users can create an account with a username and password, and then log in with the registered credentials.

After successful login, the system only needs to show a simple welcome message.

## 2. Registration Requirements

1. The username cannot be empty.
2. The username length must be greater than 6 characters.
3. The password cannot be empty.
4. The password length must be greater than 6 characters.
5. If the username already exists, registration should fail.
6. If all information is valid, registration should succeed.

## 3. Login Requirements

1. The username cannot be empty.
2. The password cannot be empty.
3. Users can log in only when the username and password are correct.
4. If the username or password is incorrect, login should fail.
5. After successful login, the system should return a welcome message.

## 4. Expected Login Success Response

When login is successful, the system should return:

{
  "message": "Login success",
  "data": "Welcome! You have successfully logged in."
}

## 5. Intentional Bug for Testing Demo

According to the PRD, the username length must be greater than 6 characters.

However, the backend system intentionally does not validate username length during registration.

This means a username such as "abc" can still be registered successfully.

This is an intentional bug for demonstrating automated PRD-based testing.
"""

with open("login-demo/PRD.md", "w", encoding="utf-8") as f:
    f.write(prd_content)

print("PRD.md created successfully.")
backend_code = """
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory database
users = {}

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Backend is running"})


@app.route("/register", methods=["POST"])
def register():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    # Intentional Bug 
    # PRD要求：用户名长度必须 > 6
    # 这里故意不校验

    if not password:
        return jsonify({"error": "Password is required"}), 400

    if len(password) <= 6:
        return jsonify({"error": "Password must be longer than 6 characters"}), 400

    if username in users:
        return jsonify({"error": "Username already exists"}), 400

    users[username] = password

    return jsonify({"message": "Register success"}), 200


@app.route("/login", methods=["POST"])
def login():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    if not password:
        return jsonify({"error": "Password is required"}), 400

    if username not in users:
        return jsonify({"error": "User does not exist"}), 400

    if users[username] != password:
        return jsonify({"error": "Incorrect password"}), 400

    return jsonify({
        "message": "Login success",
        "data": "Welcome! You have successfully logged in."
    }), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
"""

with open("login-demo/backend/app.py", "w", encoding="utf-8") as f:
    f.write(backend_code)

print("Backend app.py created.")
import sys
!{sys.executable} -m pip install requests
import requests

url = "http://127.0.0.1:5000/register"

data = {
    "username": "abc",
    "password": "12345678"
}

response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response:", response.json())
import requests
from datetime import datetime

# 1. Read PRD
with open("login-demo/PRD.md", "r", encoding="utf-8") as f:
    prd_text = f.read()

print("PRD loaded successfully.")

# 2. Define test cases based on PRD
test_cases = [
    {
        "case_id": "TC_REG_001",
        "title": "Username length should be greater than 6 characters",
        "endpoint": "http://127.0.0.1:5000/register",
        "method": "POST",
        "input": {
            "username": "abc123",
            "password": "12345678"
        },
        "expected_status": 400,
        "expected_result": "Registration should fail because username length is not greater than 6."
    }
]

# 3. Execute test cases
test_results = []

for case in test_cases:
    response = requests.post(case["endpoint"], json=case["input"])

    actual_status = response.status_code
    actual_response = response.json()

    if actual_status == case["expected_status"]:
        result = "PASS"
        bug = None
    else:
        result = "FAIL"
        bug = {
            "bug_title": "Registration allows username shorter than required length",
            "severity": "High",
            "description": (
                "According to the PRD, the username length must be greater than 6 characters. "
                "However, the system allows registration with username 'abc'."
            ),
            "expected_result": case["expected_result"],
            "actual_result": f"Status Code: {actual_status}, Response: {actual_response}"
        }

    test_results.append({
        "case_id": case["case_id"],
        "title": case["title"],
        "input": case["input"],
        "expected_status": case["expected_status"],
        "actual_status": actual_status,
        "actual_response": actual_response,
        "result": result,
        "bug": bug
    })

# 4. Generate test report
report_lines = []

report_lines.append("# Automated Test Report")
report_lines.append("")
report_lines.append(f"Generated Time: {datetime.now()}")
report_lines.append("")
report_lines.append("## PRD Rule")
report_lines.append("Username length must be greater than 6 characters.")
report_lines.append("")
report_lines.append("## Test Results")
report_lines.append("")

for result in test_results:
    report_lines.append(f"### {result['case_id']} - {result['title']}")
    report_lines.append(f"- Input: {result['input']}")
    report_lines.append(f"- Expected Status: {result['expected_status']}")
    report_lines.append(f"- Actual Status: {result['actual_status']}")
    report_lines.append(f"- Actual Response: {result['actual_response']}")
    report_lines.append(f"- Result: {result['result']}")
    report_lines.append("")

    if result["bug"]:
        report_lines.append("## Auto Generated Bug")
        report_lines.append(f"- Bug Title: {result['bug']['bug_title']}")
        report_lines.append(f"- Severity: {result['bug']['severity']}")
        report_lines.append(f"- Description: {result['bug']['description']}")
        report_lines.append(f"- Expected Result: {result['bug']['expected_result']}")
        report_lines.append(f"- Actual Result: {result['bug']['actual_result']}")
        report_lines.append("")

report_content = "\n".join(report_lines)

# 5. Save report
with open("login-demo/test_report.md", "w", encoding="utf-8") as f:
    f.write(report_content)

print(report_content)
print("\nTest report saved to: login-demo/test_report.md")
import re

# Read PRD file
with open("login-demo/PRD.md", "r", encoding="utf-8") as f:
    prd_text = f.read()

print("PRD loaded successfully.")
print("-" * 50)

# Define extracted rules list
extracted_rules = []

# Rule 1: username length rule
username_length_pattern = r"username length must be greater than (\d+) characters"

match = re.search(username_length_pattern, prd_text, re.IGNORECASE)

if match:
    min_length = int(match.group(1))
    
    rule = {
        "rule_id": "RULE_001",
        "field": "username",
        "condition": "length_greater_than",
        "value": min_length,
        "source_text": match.group(0),
        "expected_behavior": "Registration should fail if username length is not greater than required value."
    }
    
    extracted_rules.append(rule)

# Print extracted rules
print("Extracted Rules:")

for rule in extracted_rules:
    print(rule)
# Auto generate test cases from extracted rules

generated_test_cases = []

for rule in extracted_rules:

    # Username length rule
    if (
        rule["field"] == "username"
        and rule["condition"] == "length_greater_than"
    ):

        required_length = rule["value"]

        # Boundary test cases
        test_cases = [

            {
                "case_id": "TC_REG_001",
                "type": "Boundary",
                "description": "Username shorter than required",
                "input": {
                    "username": "abc",
                    "password": "12345678"
                },
                "expected_status": 400
            },

            {
                "case_id": "TC_REG_002",
                "type": "Boundary",
                "description": "Username equals boundary value",
                "input": {
                    "username": "abcdef",
                    "password": "12345678"
                },
                "expected_status": 400
            },

            {
                "case_id": "TC_REG_003",
                "type": "Valid",
                "description": "Username greater than required",
                "input": {
                    "username": "abcdefg",
                    "password": "12345678"
                },
                "expected_status": 200
            }

        ]

        generated_test_cases.extend(test_cases)


print("Generated Test Cases")
print("-" * 50)

for tc in generated_test_cases:

    print(
        tc["case_id"],
        "|",
        tc["type"],
        "|",
        tc["description"]
    )
import requests

# Backend API
url = "http://127.0.0.1:5000/register"

execution_results = []

print("Executing Test Cases")
print("-" * 50)

for tc in generated_test_cases:

    try:

        response = requests.post(
            url,
            json=tc["input"]
        )

        actual_status = response.status_code

        result = (
            "PASS"
            if actual_status == tc["expected_status"]
            else "FAIL"
        )

        execution_result = {
            "case_id": tc["case_id"],
            "description": tc["description"],
            "expected_status": tc["expected_status"],
            "actual_status": actual_status,
            "response": response.json(),
            "result": result
        }

        execution_results.append(
            execution_result
        )

        print(
            tc["case_id"],
            "|",
            result
        )

    except Exception as e:

        print(
            tc["case_id"],
            "| ERROR |",
            e
        )
print("Auto Bug Detection")
print("-" * 50)

auto_bugs = []

for result in execution_results:

    if result["result"] == "FAIL":

        bug = {
            "bug_id": "BUG_" + result["case_id"],
            "title": "Registration allows username shorter than PRD rule",
            "severity": "HIGH",
            "related_case": result["case_id"],
            "expected": result["expected_status"],
            "actual": result["actual_status"],
            "response": result["response"],
            "description": (
                "PRD requires username length > 6, "
                "but the system still allows registration."
            )
        }

        auto_bugs.append(bug)

for bug in auto_bugs:
    print(
        bug["bug_id"],
        "|",
        bug["severity"],
        "|",
        bug["related_case"]
    )
report = f"""
# Automated Test Report

Generated automatically

-----------------------------------

PRD Rule:

Username length > 6

-----------------------------------

Test Results:

TC_REG_001 : FAIL
TC_REG_002 : FAIL
TC_REG_003 : PASS

-----------------------------------

Auto Generated Bugs:

BUG_TC_REG_001
Severity: HIGH

BUG_TC_REG_002
Severity: HIGH

-----------------------------------

Conclusion:

System violates PRD constraints.

Registration module allows invalid username length.

Auto bug generation successful.

"""

with open(
    "login-demo/test_report.md",
    "w",
    encoding="utf-8"
) as f:

    f.write(report)

print(report)
import json

print("Requirement Analysis")
print("-"*50)

requirements = []

for rule in extracted_rules:

    req = {
        "module":"register",
        "field":rule["field"],
        "type":"validation",
        "rule":f'{rule["condition"]} {rule["value"]}',
        "risk":"Invalid input accepted"
    }

    requirements.append(req)

for r in requirements:
    print(r)

with open(
    "login-demo/requirements.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        requirements,
        f,
        indent=4,
        ensure_ascii=False
    )
prd_rules = [

"Username cannot be empty",

"Username length > 6",

"Password length > 8",

"Email format valid",

"Confirm password same"

]

print("Multi Rule PRD")

for r in prd_rules:
    print(r)
extra_cases = [

{
"case_id":"TC_LOGIN_001",
"type":"Valid",
"description":"Correct username password"
},

{
"case_id":"TC_LOGIN_002",
"type":"Invalid",
"description":"Wrong password"
},

{
"case_id":"TC_LOGIN_003",
"type":"Boundary",
"description":"Empty username"
}

]

generated_test_cases.extend(
    extra_cases
)

print(
"Total Cases:",
len(generated_test_cases)
)
import json

with open(
    "login-demo/bugs.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        auto_bugs,
        f,
        indent=4,
        ensure_ascii=False
    )

print("bugs.json created")
summary = {

"total":
len(execution_results),

"pass":
sum(
1 for x in execution_results
if x["result"]=="PASS"
),

"fail":
sum(
1 for x in execution_results
if x["result"]=="FAIL"
),

"bugs":
len(auto_bugs)

}

print(summary)