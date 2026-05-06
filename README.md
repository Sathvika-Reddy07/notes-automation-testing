📘 SECTION 1 — Requirements, Test Design, RTM & Manual QA Plan
🎯 Objective

This section focuses on manual QA engineering design, including:

Requirement analysis
Test planning
Test scenario design
Test case creation
Requirement Traceability Matrix (RTM)

It ensures 100% functional coverage before automation begins.

📌 Application Under Test (AUT)
UI:

https://practice.expandtesting.com/notes/app

API:

https://practice.expandtesting.com/notes/api/api-docs/

🧩 1.1 Requirement Breakdown
Req ID	Description
FR-01	UI login should work
FR-02	Create note via UI
FR-03	Note should appear instantly in UI
FR-04	API GET /notes returns notes
FR-05	UI-created note must appear in API
FR-06	Delete note via API
FR-07	Deleted note must disappear from UI
FR-08	API response time < 2 seconds
FR-09	Negative scenarios (UI + API validation)
📋 1.2 Manual Test Plan
🎯 Purpose

To validate UI, API, and integration flows before automation.

📌 Scope
UI Testing:
Login functionality
Create notes
UI validation (DOM updates)
API Testing:
Authentication
GET /notes
POST /notes
DELETE /notes
Integration:
UI ↔ API data consistency
Negative Testing:
Invalid login
Missing fields
Invalid API tokens
🧪 Test Strategy
Layer	Approach
UI	Exploratory + Structured testing
API	Postman / manual REST validation
E2E	UI ↔ API data comparison
Defects	Logged with steps + evidence
🧪 1.3 Test Scenarios
TS-01: Validate UI Login
Ensure valid login works
Ensure invalid login shows error
TS-02: Create Note via UI
Enter title & description
Click save
Validate note appears instantly
TS-03: UI → API Sync
Create note in UI
Validate same note in GET /notes API
TS-04: API → UI Sync
Delete note using API
Validate note removed from UI
TS-05: API Validation
GET /notes returns correct data
Response time < 2 sec
TS-06: Negative UI Scenarios
Empty title
Empty description
Invalid login
TS-07: Negative API Scenarios
Invalid token
Missing payload
Wrong endpoints
🧾 1.4 Sample Test Case
TC-UI-04: Validate UI → API Data Consistency
Objective:

Ensure UI-created note matches API data exactly.

Steps:
Login via UI
Create note (Title + Description)
Capture UI values
Call GET /notes API
Match UI vs API data
Expected Result:
Title matches exactly
Description matches exactly
No missing fields
Data consistency maintained
🔗 1.5 Requirement Traceability Matrix (RTM)
Req ID	Scenario	Test Case
FR-01	TS-01	TC-UI-01
FR-02	TS-02	TC-UI-02
FR-03	TS-02	TC-UI-03
FR-04	TS-05	TC-API-01
FR-05	TS-03	TC-E2E-01
FR-06	TS-04	TC-API-02
FR-07	TS-04	TC-E2E-02
FR-08	TS-05	TC-API-03
FR-09	TS-06	TC-NEG-01
📘 SECTION 2 — Selenium Python Automation Framework (UI + API + Hybrid)
🎯 Objective

Build a scalable automation framework using:

Selenium WebDriver (UI testing)
Requests (API testing)
Pytest (Test framework)
POM (Page Object Model)
Allure reporting
Parallel execution (pytest-xdist)
🏗 2.1 Framework Architecture
project/
│
├── tests/
│   ├── ui/
│   ├── api/
│   ├── e2e/
│   ├── debug/
│
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   ├── notes_page.py
│
├── api_client/
│   └── api_client.py
│
├── conftest.py
├── pytest.ini
├── requirements.txt
│
├── allure-results/
├── allure-report/
└── logs/
⚙️ 2.2 UI Automation (Selenium)
Key Features:
Page Object Model (POM)
Explicit waits (WebDriverWait)
JS executor for stability
Retry mechanism for flaky UI
Screenshot on failure
Stale element handling
Example Flow:
Open login page
Enter credentials
Create note
Validate UI update instantly
🌐 2.3 API Automation (Requests)
Features:
Central API client
Token-based authentication
CRUD operations:
Create note
Get notes
Delete note
Example Flow:
Login API → get token
GET /notes
POST /notes
DELETE /notes/{id}
🔗 2.4 Hybrid E2E Testing
🔹 Scenario 1: UI → API Validation
Flow:
Create note via UI
Capture title & description
Call GET /notes API
Validate data consistency
🔹 Scenario 2: API → UI Validation
Flow:
Create/Delete note via API
Refresh UI
Validate UI reflects backend changes
⚡ 2.5 Advanced Framework Features
🧵 Parallel Execution
pytest -n 3

✔ Runs tests in parallel workers
✔ Faster execution
✔ Independent browser sessions

📸 Failure Handling
Screenshot capture
Logs stored per test
Debug session tracking
🧪 Session Isolation

Each test uses:

✔ Independent WebDriver instance
✔ Unique session ID
✔ No shared state

📊 2.6 Reporting (Allure)
Features:
Test execution report
Screenshots on failure
API response attachments
Environment details
Step-by-step execution
Example API Attachment:
import allure

allure.attach(
    str(response.json()),
    name="API Response",
    attachment_type=allure.attachment_type.JSON
)
🚀 2.7 How to Run Tests
Install dependencies:
pip install -r requirements.txt
Run all tests:
pytest
Run parallel execution:
pytest -n 3
Generate report:
pytest --alluredir=allure-results
allure serve allure-results
🧠 Final Outcome

✔ UI Automation working
✔ API Automation working
✔ Hybrid E2E validation
✔ Parallel execution enabled
✔ Allure reporting integrated
✔ Scalable enterprise framework