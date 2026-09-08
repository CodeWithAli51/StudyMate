# StudyMate — Product Plan & Agentic Build Roadmap

> A student-first study companion that makes daily studying structured, measurable, motivating, and personalized — without becoming another boring task manager.

---

## 1. Product Vision

**StudyMate** is a web app where a student opens the site every day and immediately knows:

1. What should I study today?
2. How much have I completed?
3. What am I weak at?
4. What should I revise?
5. What should I do next?
6. Where can AI help me?

The product should feel like a **personal study command center**, not a school ERP.

The design principle is:

> **Plan → Study → Practice → Review → Improve**

The system should work for different students, classes, boards, and subjects. It can have **Maharashtra SSC / Class 10** as a strong initial preset, but the underlying data model should remain generic.

---

# 2. Core Product Principles

### Keep it simple
A student should understand the home screen within 10 seconds.

### Build progressively
Do not build AI, analytics, gamification, quizzes, reminders, and authentication all at once.

### Server-rendered first
The project should prioritize Python and HTML/CSS. Avoid a heavy JavaScript framework.

### Every feature must be useful
No feature should exist merely because it looks impressive.

### Track meaningful progress
Do not measure only "hours spent." Track:
- topics completed
- questions attempted
- accuracy
- revision status
- consistency
- confidence
- weak topics

### AI should assist, not replace studying
AI should explain, quiz, summarize, give hints, and help plan — not simply hand out answers.

---

# 3. Recommended Technical Direction

## Backend

**Python + Django**

Why:
- mature web framework
- authentication included
- database models and migrations
- admin panel
- forms
- secure defaults
- easy deployment
- excellent for a long-lived student platform

## Frontend

**Django Templates + HTML + CSS**

Avoid React/Next/Vue for the initial version.

Use:
- semantic HTML
- modern CSS
- small amounts of vanilla JavaScript only where interaction genuinely needs it

Optional later:
- HTMX for small partial-page interactions
- no SPA architecture unless the product eventually proves it needs one

## Database

Start with:

**SQLite**

Move to:

**PostgreSQL**

when deployment/scale requires it.

## AI

Keep AI behind a dedicated Python service/module.

Do not scatter API calls throughout the project.

Example architecture:

```text
study_mate/
├── config/
├── accounts/
├── academics/
├── planner/
├── progress/
├── practice/
├── revision/
├── assistant/
├── gamification/
├── dashboard/
├── templates/
├── static/
├── tests/
├── requirements.txt
├── .env.example
├── manage.py
└── README.md
```

The exact app names can be adjusted during implementation, but the separation of responsibilities should remain.

---

# 4. Main Student Experience

## A. Onboarding

First-time student creates a profile.

Collect only useful information:

- name
- class/grade
- education board
- school year
- subjects
- target/goal
- optional exam date
- preferred study duration
- difficulty preference

Example:

```text
Welcome to StudyMate 👋

Class: 10
Board: Maharashtra SSC
Year: 2026–27

Subjects:
☑ Mathematics
☑ Science
☑ English
☑ Marathi
☑ History & Political Science
☑ Geography

Goal:
Score 90%+

Preferred daily study time:
2 hours
```

Do not overwhelm the student with 30 settings.

---

# 5. Dashboard

The dashboard is the most important screen.

It should answer:

### "What do I do today?"

Suggested structure:

```text
Good evening, Ayesha 👋

STREAK
🔥 7 days

TODAY
────────────────────────
Maths — Algebra
45 min
[ Start Study ]

Science — Life Processes
30 min
[ Start Study ]

English — Grammar
20 min
[ Start Study ]

TODAY'S PROGRESS
██████████████░░ 72%

3 / 4 tasks completed

────────────────────────
QUICK ACTIONS

[ Study Now ]
[ Practice Quiz ]
[ Revise Weak Topics ]
[ Ask AI ]

────────────────────────
YOUR PROGRESS

Weekly: 78%
Quiz accuracy: 84%
Topics mastered: 42 / 58

────────────────────────
AI TIP

"You have improved in algebra,
but quadratic equations still
need revision."
```

Important:

**Do not make the dashboard an analytics wall.**

The dashboard is primarily an action screen.

---

# 6. Daily Study System

This is the heart of StudyMate.

A student should have:

### Today's Plan

Each task contains:

- subject
- chapter
- topic
- task type
- estimated duration
- priority
- completion state

Task types:

- Learn
- Practice
- Revise
- Test
- Homework
- Reading
- Doubt solving

Example:

```text
Today's Plan

☐ Learn: Trigonometry — 30 min
☐ Practice: Trigonometry — 20 questions
☐ Revise: Chemical Reactions — 15 min
☐ Quiz: Geography Chapter 3 — 10 questions
```

---

# 7. Study Session

When the student clicks **Start Study**:

```text
TRIGONOMETRY

Goal
Understand basic trigonometric ratios.

Estimated time
30 minutes

Checklist
☐ Read concept
☐ Study examples
☐ Solve 5 basic questions
☐ Mark difficult areas

[ Start Session ]

Optional timer
25:00
```

At the end:

```text
Session Complete 🎉

How confident are you?

○ Very weak
○ Weak
○ Okay
○ Good
○ Very confident

What should happen next?

[ Practice questions ]
[ Schedule revision ]
[ Done ]
```

The confidence rating becomes useful data later.

---

# 8. Progress Tracking

Track more than hours.

## Student-level metrics

- tasks completed
- study sessions
- total study minutes
- weekly consistency
- current streak
- longest streak
- quiz accuracy
- topic mastery
- revision completion
- weak areas

## Subject-level metrics

Example:

```text
Mathematics
━━━━━━━━━━━━━━━━
78% progress

Algebra        92%
Geometry       73%
Statistics     68%
Trigonometry   51%  ← needs attention
```

## Topic-level state

Every topic should eventually have a state such as:

```text
Not Started
Learning
Practicing
Needs Revision
Strong
Mastered
```

---

# 9. Smart Revision System

A strong study product should automatically tell the student what to revise.

A simple first version can use:

- confidence rating
- quiz accuracy
- time since last revision

Example:

```text
REVISION QUEUE

🔴 High Priority
Quadratic Equations
Last revised: 8 days ago
Quiz accuracy: 54%

🟠 Medium Priority
Chemical Reactions
Last revised: 5 days ago
Quiz accuracy: 71%

🟢 Due Soon
Resources and Development
Last revised: 2 days ago
Quiz accuracy: 84%
```

Later, this can evolve into spaced repetition.

---

# 10. Practice / Quiz System

Quizzes make the site interactive.

Question types for V1:

- MCQ
- true/false
- short answer

Later:
- fill in the blank
- matching
- image-based questions
- mixed mock tests

Quiz flow:

```text
Science — Chapter Quiz

Question 4 / 10

Which process produces oxygen
during photosynthesis?

A. Respiration
B. Transpiration
C. Photolysis
D. Fermentation

[ Submit ]
```

After the quiz:

```text
Score: 8 / 10

Accuracy: 80%

Strong:
✓ Photosynthesis basics
✓ Chlorophyll

Review:
⚠ Light reaction
⚠ Photolysis
```

Every quiz should feed into the progress system.

---

# 11. AI Assistant

The AI assistant is a major feature, but it should be introduced only after the non-AI study system works.

Name it something friendly such as:

**StudyMate AI**

Possible modes:

### Explain
"Explain photosynthesis like I'm in class 10."

### Simplify
"Make this easier to understand."

### Quiz Me
"Ask me 5 questions on this chapter."

### Hint
"Give me a hint, not the answer."

### Check My Answer
Student submits an answer and AI evaluates it.

### Study Plan
"I have 2 hours tonight. What should I study?"

### Revision
"What should I revise today?"

### Doubt Solver
Student asks a question and receives an explanation.

---

# 12. AI Guardrails

The AI layer should be carefully designed.

The assistant should:

- ask clarifying questions when context is insufficient
- prefer explanations over direct answer dumping
- give hints before full solutions when requested
- adapt to the student's grade/board/subject
- avoid pretending to know curriculum facts it cannot verify
- clearly distinguish generated guidance from official textbook content
- never expose API keys to the browser
- have rate limits
- log only the minimum information needed

The AI code should live behind a clean service boundary:

```python
assistant/
    services/
        llm.py
        prompts.py
        context.py
```

Do not place provider-specific code directly inside templates/views.

---

# 13. StudyMate AI Context

Eventually the AI should know:

```text
Student:
Class 10
Board: Maharashtra SSC

Current subject:
Mathematics

Current chapter:
Trigonometry

Weak topics:
Quadratic equations
Trigonometric identities

Recent quiz:
7/10

Current goal:
90%

Today's remaining study time:
55 minutes
```

This allows the AI to be genuinely useful instead of being a generic chatbot.

---

# 14. Motivation & Gamification

Gamification should support learning, not distract from it.

## V1

Use simple elements:

- streak
- XP
- daily goal
- completion ring
- milestone badges

Example badges:

```text
🔥 7 Day Streak
📚 10 Study Sessions
🎯 90% Quiz Accuracy
🧠 10 Topics Mastered
🏆 100 Tasks Completed
```

Avoid creating a noisy game interface.

---

# 15. Daily Challenges

Add small optional challenges.

Examples:

```text
TODAY'S CHALLENGE

Solve 5 Maths problems
without checking the solution.

Reward:
+25 XP
```

or:

```text
Memory Challenge

Close your notes and write
everything you remember about
Photosynthesis.

[ Start ]
```

This encourages active recall.

---

# 16. Focus Mode

A distraction-free mode:

```text
FOCUS MODE

Current task:
Trigonometric Ratios

25:00

Focus checklist:
☑ Phone away
☐ Read concept
☐ Solve examples

[ Finish Session ]
```

Do not build a complex Pomodoro engine immediately.

Start with a simple study timer/session tracker.

---

# 17. Homework / Assignment Tracking

Useful fields:

- title
- subject
- description
- due date
- priority
- status
- optional attachment later

Statuses:

```text
Not Started
In Progress
Submitted
Completed
```

---

# 18. Notes

Students should eventually be able to create notes connected to a topic.

Example:

```text
Mathematics
└── Algebra
    └── Quadratic Equations
        ├── Formula
        ├── Important identities
        └── My mistakes
```

V1 notes can be plain text.

Do not build a Notion clone.

---

# 19. Mistake Book

This is one of the most valuable advanced features.

After a quiz or practice session:

```text
MY MISTAKES

Maths — Trigonometry

Question:
...

My answer:
...

Correct answer:
...

Why I got it wrong:
Concept confusion

Revision status:
Needs review
```

Eventually AI can help identify recurring mistake patterns.

---

# 20. Analytics

Create a separate Analytics page.

Show:

### Weekly
- study minutes
- completed tasks
- quiz accuracy
- consistency

### Subjects
- strongest
- weakest
- improving
- neglected

### Trends
Example:

```text
Quiz Accuracy

Week 1   61%
Week 2   68%
Week 3   74%
Week 4   82%
```

Keep charts simple.

The goal is insight, not dashboard decoration.

---

# 21. Calendar

Eventually connect study tasks and exams to a calendar view.

Useful events:

- exams
- homework deadlines
- study sessions
- revision dates

V1 can be an internal calendar.

External calendar integrations are optional later.

---

# 22. Notifications

Later feature.

Possible notifications:

- daily plan reminder
- upcoming exam
- overdue task
- revision due
- streak warning
- weekly summary

Do not build browser push notifications first.

Start with in-app reminders.

---

# 23. Exam Mode

A major later feature.

Student chooses:

```text
Exam:
Science Unit Test

Date:
20 days away

Syllabus:
Chapters 1–6
```

StudyMate generates:

```text
20-DAY PLAN

Days 1–10
Complete concepts

Days 11–15
Practice

Days 16–18
Revision

Days 19
Mock test

Day 20
Light revision
```

This is where the planner and AI become especially powerful.

---

# 24. Parent / Teacher Features

Do not build this in V1.

Eventually:

### Parent view
- attendance-like study consistency
- completed work
- upcoming exams
- weak subjects

### Teacher view
- assign practice
- create quizzes
- monitor class progress

These should be separate roles and permissions.

---

# 25. Multi-Student / Reusable Architecture

StudyMate should support multiple students from the beginning at the data-model level.

Do not hard-code:

```text
Ayesha
Class 10
SSC
```

Instead use:

```text
User
StudentProfile
Board
Grade
AcademicYear
Subject
Chapter
Topic
Task
StudySession
Quiz
Question
Attempt
RevisionItem
Note
Mistake
Achievement
```

This makes StudyMate reusable for other students.

---

# 26. Suggested Data Model

Initial models:

```text
User
StudentProfile

Subject
Chapter
Topic

StudyPlan
StudyTask
StudySession

Quiz
Question
QuizAttempt
AnswerAttempt

RevisionItem

Achievement
StudentAchievement

Homework
Note

AIConversation
AIMessage
```

Later models:

```text
Exam
ExamPlan
Mistake
Notification
ParentProfile
TeacherProfile
Assignment
```

Do not create all models on day one.

Create them when their feature is built.

---

# 27. Navigation

Keep the primary navigation small:

```text
Home
Plan
Practice
Progress
AI
```

Secondary navigation:

```text
Revision
Notes
Homework
Achievements
Settings
```

Mobile navigation can become:

```text
Home | Plan | Practice | AI | More
```

---

# 28. UI / Visual Direction

The UI should feel:

- modern
- friendly
- calm
- youthful
- clean
- encouraging

Avoid:

- childish cartoon overload
- corporate ERP appearance
- excessive gradients
- huge dashboards
- too many cards
- constant animations

Use a consistent design system:

```text
Border radius
Spacing scale
Typography scale
Button styles
Card styles
Form styles
Status badges
Progress indicators
```

Build these once and reuse them.

---

# 29. Accessibility

From the beginning:

- keyboard-friendly
- readable contrast
- visible focus state
- proper labels
- semantic headings
- buttons instead of clickable divs
- mobile-friendly layout
- reduced-motion friendly

Do not treat accessibility as a final polish step.

---

# 30. Security Requirements

At minimum:

- password hashing through Django auth
- CSRF protection
- server-side authorization checks
- environment variables for secrets
- never expose AI API keys
- validate user input
- rate-limit AI endpoints
- prevent users from accessing another student's data
- secure production settings
- safe file handling once uploads exist

---

# 31. Testing Strategy

Every meaningful feature should include tests.

Prioritize:

### Model tests
Does the data behave correctly?

### Service tests
Does business logic work?

### View tests
Can the user access the feature?

### Permission tests
Can one student access another student's data?

### Regression tests
Does an old feature still work after a new feature is added?

The agent must run the relevant tests before every commit.

---

# 32. Definition of Done

A feature is not complete merely because the page exists.

Each feature is complete when:

```text
☐ Data model works
☐ UI works
☐ Empty state exists
☐ Validation exists
☐ Error state exists
☐ Mobile layout is acceptable
☐ Permissions are correct
☐ Tests pass
☐ Existing tests still pass
☐ Documentation is updated
☐ Git commit created
```

---

# 33. Development Rule: One Safe Step at a Time

The most important rule for the coding agent:

> **Do not build multiple unrelated features in one step.**

Each prompt below should result in:

```text
1. Inspect current repository
2. Make a small change
3. Run tests
4. Run lint/format checks
5. Manually verify the feature
6. Update documentation if needed
7. Show changed files
8. Give suggested commit message
9. Stop
```

Never ask the agent to implement the entire application in one prompt.

---

# 34. Git Strategy

Use conventional commits.

Examples:

```text
chore: initialize django project
feat: add student profile
feat: add subject and topic hierarchy
feat: add daily study tasks
feat: add study session tracking
feat: add dashboard
feat: add quiz engine
feat: add revision queue
feat: add progress analytics
feat: add ai assistant
fix: prevent cross-user task access
test: add quiz scoring coverage
refactor: isolate ai provider service
```

Recommended cycle:

```text
Prompt
↓
Code
↓
Test
↓
Review
↓
Commit
↓
Next prompt
```

---

# 35. Master Build Order

## Phase 0 — Foundation

1. Repository inspection
2. Project structure
3. Django setup
4. Settings/environment configuration
5. Base layout/design system
6. Health check
7. Test infrastructure
8. Git hygiene

## Phase 1 — Accounts

9. Registration
10. Login/logout
11. Student profile
12. Profile editing

## Phase 2 — Academic Structure

13. Subject
14. Chapter
15. Topic
16. Student subject selection

## Phase 3 — Study Planner

17. Study task model
18. Create/edit/delete tasks
19. Daily plan
20. Mark tasks complete
21. Task filtering

## Phase 4 — Study Sessions

22. Start session
23. Session tracking
24. Confidence rating
25. Session history

## Phase 5 — Dashboard

26. Daily overview
27. Progress summary
28. Streak
29. Recommended next action

## Phase 6 — Practice

30. Question model
31. Quiz model
32. Quiz attempt
33. Scoring
34. Results
35. Topic accuracy

## Phase 7 — Revision

36. Revision queue
37. Weak topic detection
38. Revision completion
39. Simple spaced-review rules

## Phase 8 — Motivation

40. XP
41. Streak
42. Achievements
43. Daily challenge

## Phase 9 — Progress

44. Subject analytics
45. Weekly analytics
46. Trends
47. Weak/strong topic insights

## Phase 10 — AI

48. AI service abstraction
49. AI chat UI
50. Subject/topic context
51. Explain mode
52. Quiz-me mode
53. Hint mode
54. Check-answer mode
55. Study-plan mode
56. AI safety/rate limits

## Phase 11 — Advanced Learning

57. Notes
58. Mistake book
59. Exam planning
60. Homework
61. Calendar
62. Notifications

## Phase 12 — Production

63. PostgreSQL support
64. Production settings
65. Deployment
66. Monitoring/logging
67. Backup strategy
68. Security review
69. Accessibility review
70. Performance review

---

# 36. Agentic Coder Prompt Rules

Paste the following behavior into your coding agent's project instructions if supported:

```text
You are building StudyMate incrementally.

Rules:
1. Never implement the whole roadmap at once.
2. Work only on the requested step.
3. Inspect the existing code before modifying it.
4. Preserve existing behavior.
5. Prefer simple Django/server-rendered solutions.
6. Avoid unnecessary JavaScript and frontend frameworks.
7. Never introduce a dependency without explaining why it is needed.
8. Write tests for meaningful business logic.
9. Run the relevant test suite after changes.
10. Run formatting/linting if configured.
11. Never silently rewrite large parts of the project.
12. Keep migrations clean and reversible where practical.
13. Never hard-code student-specific data.
14. Enforce user ownership at the server side.
15. Do not expose API secrets.
16. When something is ambiguous, choose the smallest reasonable implementation and document the assumption rather than expanding scope.
17. At the end of each task report:
   - what changed
   - files changed
   - tests run
   - result
   - anything intentionally deferred
   - proposed commit message
18. Stop after the requested step. Do not continue to the next roadmap item automatically.
```

---

# 37. Step-by-Step Prompts for the Agent

Below, each prompt is intentionally narrow.

---

## PROMPT 01 — Repository Audit

```text
You are starting work on StudyMate.

Do NOT build features yet.

Inspect the current repository thoroughly.

Determine:
- current language/framework
- package manager
- existing project structure
- existing tests
- existing configuration
- git status
- existing README/documentation
- whether there is already a Django project
- any existing frontend
- any potentially dangerous or obsolete files

Then propose the smallest safe foundation plan for this repository.

Do not modify application code yet.

Only documentation/configuration may be changed if necessary to record findings.

Run no destructive commands.

At the end, report:
1. repository findings
2. risks
3. recommended foundation
4. exact next step
5. proposed commit message

Stop.
```

Commit:
```text
docs: audit study mate repository
```

---

## PROMPT 02 — Initialize Python Environment

```text
Implement only the Python project foundation for StudyMate.

Use Django unless the repository already has a strong reason not to.

Requirements:
- create/use a virtual environment strategy
- create requirements/dependency file
- initialize Django if needed
- create clean project structure
- add a minimal settings structure
- add .gitignore
- add .env.example
- do not add study features
- do not add AI
- do not add authentication UI yet

Run:
- Django system checks
- existing tests

Make the smallest clean change.

At the end report changed files, checks, tests, and proposed commit message.

Stop.
```

Commit:
```text
chore: initialize django foundation
```

---

## PROMPT 03 — Base Template and Design System

```text
Build only the StudyMate visual foundation.

Create:
- base HTML template
- navigation shell
- typography scale
- spacing system
- buttons
- cards
- badges
- forms
- empty states
- success/error message styles
- responsive layout foundation

Use server-rendered Django templates and CSS.

Do not create student data models.
Do not create dashboard logic.
Do not add JavaScript unless absolutely necessary.

Create a simple placeholder home page to demonstrate the design system.

Run tests and Django checks.

Stop after this step.
```

Commit:
```text
feat: add studymate design foundation
```

---

## PROMPT 04 — Health Check and Test Infrastructure

```text
Add only application health and basic test infrastructure.

Implement:
- a simple health-check endpoint
- a basic test confirming it works
- a test setup suitable for future Django apps

Do not build any student features.

Run the full test suite.

Stop.
```

Commit:
```text
test: add health check infrastructure
```

---

## PROMPT 05 — Accounts

```text
Implement StudyMate authentication.

Requirements:
- registration
- login
- logout
- protected pages
- clear validation errors
- responsive forms
- Django's secure authentication mechanisms
- no custom password storage

Do not build profile fields yet.
Do not build subjects or study plans.

Add tests for:
- registration
- login
- logout
- unauthenticated access

Run all tests.

Stop.
```

Commit:
```text
feat: add student authentication
```

---

## PROMPT 06 — Student Profile

```text
Add a StudentProfile model linked safely to the authenticated user.

Fields should include only:
- display name
- grade
- board
- academic year
- goal
- preferred daily study minutes

Create:
- profile setup
- profile edit
- profile display

Do not add subjects yet.

Ensure users can only read/edit their own profile.

Add model, view, and permission tests.

Run all tests.

Stop.
```

Commit:
```text
feat: add student profiles
```

---

## PROMPT 07 — Subjects, Chapters, Topics

```text
Implement the academic hierarchy.

Create models for:
- Subject
- Chapter
- Topic

Relationships:

Subject
→ Chapter
→ Topic

Add:
- admin support
- basic list/detail pages
- sensible ordering
- validation

Do not build study tasks yet.

Create tests for model relationships and validation.

Stop.
```

Commit:
```text
feat: add academic structure
```

---

## PROMPT 08 — Student Subject Selection

```text
Allow a student to choose which subjects they study.

Requirements:
- show available subjects
- select/unselect subjects
- keep selection tied to the current student
- show selected subjects on profile/dashboard placeholder
- do not allow one user to modify another user's selections

Add tests for ownership and selection behavior.

Stop.
```

Commit:
```text
feat: add student subject selection
```

---

## PROMPT 09 — Study Task Model

```text
Implement the smallest useful study task system.

Task fields:
- student
- title
- subject
- optional chapter
- optional topic
- task type
- estimated minutes
- due date
- priority
- status
- created timestamp
- completed timestamp

Task types:
- Learn
- Practice
- Revise
- Test
- Homework
- Reading
- Doubt

Statuses:
- Todo
- In Progress
- Completed

Add model tests.

Do not build the dashboard yet.

Stop.
```

Commit:
```text
feat: add study tasks
```

---

## PROMPT 10 — Study Task CRUD

```text
Build the Study Task UI.

Implement:
- task list
- create
- edit
- delete
- mark complete
- clear empty state
- filters by subject/status

Every operation must enforce student ownership.

Do not add drag-and-drop.
Do not add AI.
Do not add analytics.

Add tests for CRUD and permissions.

Stop.
```

Commit:
```text
feat: add study task management
```

---

## PROMPT 11 — Daily Plan

```text
Turn study tasks into a useful Today page.

Show:
- today's tasks
- completion state
- estimated total minutes
- completed minutes
- progress percentage
- priority
- next recommended task

Allow:
- mark complete
- start a task

Do not create a separate dashboard yet.

Add tests for today's filtering and progress calculation.

Stop.
```

Commit:
```text
feat: add daily study plan
```

---

## PROMPT 12 — Study Sessions

```text
Add StudySession tracking.

A session should record:
- student
- task
- started_at
- ended_at
- duration
- confidence rating
- optional reflection

Implement:
- start session
- finish session
- history
- confidence selection

Do not build a sophisticated Pomodoro system.

Ensure sessions belong to the correct student.

Add tests for duration and ownership.

Stop.
```

Commit:
```text
feat: track study sessions
```

---

## PROMPT 13 — First Real Dashboard

```text
Now build the main StudyMate dashboard using the existing data only.

The dashboard should answer:
"What should I do today?"

Show:
- greeting
- today's progress
- current task count
- estimated remaining study time
- recent study activity
- current streak if calculable
- quick actions
- next recommended task

Do not add fake statistics.
If there is not enough data, use a good empty state.

Do not add AI yet.

Add view/template tests.

Stop.
```

Commit:
```text
feat: add student dashboard
```

---

## PROMPT 14 — Streak Calculation

```text
Add a reliable study streak calculation.

Define a study day as a day on which the student completes at least one study task or study session.

Implement:
- current streak
- longest streak

Do not store redundant streak values unless necessary.
Prefer deriving them from source records.

Add edge-case tests:
- no activity
- one day
- consecutive days
- gap
- activity today
- activity yesterday but not today

Stop.
```

Commit:
```text
feat: add study streaks
```

---

## PROMPT 15 — Question and Quiz Foundation

```text
Build the quiz data model only.

Create:
- Question
- Quiz
- QuizQuestion relation
- QuizAttempt
- AnswerAttempt

Support initially:
- MCQ
- True/False

Include:
- subject
- chapter/topic when applicable
- explanation
- correct answer
- difficulty

Do not build the UI yet.

Add strong model validation and tests.

Stop.
```

Commit:
```text
feat: add quiz data model
```

---

## PROMPT 16 — Quiz Experience

```text
Build the student quiz experience using the existing quiz models.

Implement:
- quiz start
- one question at a time
- answer submission
- scoring
- result page
- explanations
- accuracy

Do not add AI-generated questions yet.

Ensure a student cannot submit/access another student's private attempt data.

Add tests for:
- scoring
- completed attempts
- invalid answers
- permissions

Stop.
```

Commit:
```text
feat: add quiz experience
```

---

## PROMPT 17 — Topic Accuracy

```text
Use completed quiz attempts to calculate topic/subject accuracy.

Add:
- subject accuracy
- topic accuracy
- questions attempted
- questions correct

Update the progress/dashboard UI with only a small summary.

Do not build charts yet.

Add tests for accurate aggregation.

Stop.
```

Commit:
```text
feat: calculate learning accuracy
```

---

## PROMPT 18 — Revision Queue

```text
Build a simple revision queue.

Prioritize a topic based on:
1. low quiz accuracy
2. low confidence
3. time since last revision

Create a RevisionItem or equivalent structure only if needed.

Show:
- high priority
- medium priority
- upcoming

Allow:
- mark revision complete
- start revision task

Do not implement machine learning or complicated spaced repetition.

Add tests for prioritization.

Stop.
```

Commit:
```text
feat: add revision queue
```

---

## PROMPT 19 — Achievements and XP

```text
Add lightweight gamification.

Implement:
- XP
- achievements
- current streak display
- milestone badges

Initial achievements:
- First Study Session
- 7 Day Streak
- 10 Study Sessions
- 10 Topics Completed
- 90% Quiz Accuracy

Do not create leaderboards.

Keep the UI subtle.

Add tests for achievement awarding and XP calculations.

Stop.
```

Commit:
```text
feat: add learning achievements
```

---

## PROMPT 20 — Daily Challenge

```text
Add an optional daily challenge system using deterministic rules.

Examples:
- complete 3 tasks
- solve 5 questions
- revise one weak topic
- study for 30 minutes

Do not use AI yet.

Show:
- challenge
- completion state
- reward

Add tests.

Stop.
```

Commit:
```text
feat: add daily challenges
```

---

## PROMPT 21 — Progress Page

```text
Build a dedicated Progress page.

Show:
- weekly study minutes
- completed tasks
- quiz accuracy
- current streak
- subject progress
- strongest subject
- weakest subject
- recently improving topics

Use simple visualizations built with HTML/CSS where possible.

Avoid introducing a chart framework unless genuinely necessary.

Do not add analytics that cannot be calculated from real data.

Add tests for the aggregation logic.

Stop.
```

Commit:
```text
feat: add progress analytics
```

---

## PROMPT 22 — AI Service Boundary

```text
Prepare StudyMate for AI without implementing the chat UI yet.

Create a clean AI service abstraction.

Requirements:
- provider configuration through environment variables
- no secret in source code
- dedicated service module
- clear request/response interface
- timeout/error handling
- rate-limit-ready design
- testable provider boundary
- ability to replace the provider later

Do not place AI calls in Django templates.

Add tests using a mocked provider.

Do not call a real paid AI service during tests.

Stop.
```

Commit:
```text
refactor: isolate ai service boundary
```

---

## PROMPT 23 — AI Chat MVP

```text
Implement the smallest useful StudyMate AI assistant.

Create:
- AI page
- conversation view
- user message
- assistant response
- clear loading/error state
- conversation history

The AI call must go through the AI service abstraction.

The browser must never receive the API secret.

Do not add advanced modes yet.

Add:
- authentication checks
- ownership checks
- rate-limit-ready handling
- tests with mocked AI responses

Stop.
```

Commit:
```text
feat: add ai study assistant
```

---

## PROMPT 24 — AI Study Context

```text
Improve StudyMate AI by providing relevant student context.

Include only useful context:
- grade
- board
- selected subjects
- current subject/topic if selected
- recent accuracy
- weak topics
- today's remaining tasks

Create a context builder service.

Do not dump the entire database into the prompt.

Add tests proving context is:
- correctly assembled
- scoped to the current student
- bounded in size

Stop.
```

Commit:
```text
feat: add student context to ai
```

---

## PROMPT 25 — AI Modes

```text
Add four explicit AI modes:

1. Explain
2. Quiz Me
3. Hint
4. Check My Answer

Each mode should have a clear prompt contract.

Behavior:
- Explain teaches step by step
- Quiz Me asks questions instead of immediately teaching
- Hint avoids revealing the full answer when possible
- Check My Answer evaluates the student's submitted response

Keep prompts centralized.

Do not let users arbitrarily change hidden system instructions.

Add tests for mode routing and mocked outputs.

Stop.
```

Commit:
```text
feat: add ai learning modes
```

---

## PROMPT 26 — AI Study Planner

```text
Add an AI-assisted study planning mode.

Input:
- available time
- upcoming exam date if available
- current weak topics
- today's incomplete tasks

Output should recommend a realistic sequence of study actions.

Important:
The AI should suggest actions, not silently modify the student's database.

Let the student approve recommendations before tasks are created.

Add tests for:
- context generation
- recommendation parsing/validation
- safe failure handling

Stop.
```

Commit:
```text
feat: add ai study planning
```

---

## PROMPT 27 — Notes

```text
Add simple topic-linked notes.

Requirements:
- create
- edit
- delete
- view
- subject/topic association
- ownership enforcement

Keep notes plain text for now.

Do not build a rich text editor.

Add tests.

Stop.
```

Commit:
```text
feat: add topic notes
```

---

## PROMPT 28 — Mistake Book

```text
Add a Mistake Book.

A mistake should connect to:
- student
- question/topic
- student's answer
- correct answer
- mistake reason
- revision status

Allow:
- save mistake from quiz result
- view mistakes
- mark reviewed

Do not add AI analysis yet.

Add ownership and workflow tests.

Stop.
```

Commit:
```text
feat: add mistake book
```

---

## PROMPT 29 — Exam Planner

```text
Add an Exam model and basic exam planning.

Implement:
- exam name
- subject
- date
- syllabus topics
- status

Create an exam detail page showing:
- days remaining
- incomplete topics
- weak topics
- recommended existing tasks

Do not automatically create hundreds of tasks.

Keep recommendations reviewable.

Add tests.

Stop.
```

Commit:
```text
feat: add exam planning
```

---

## PROMPT 30 — Homework

```text
Add a basic Homework/Assignment feature.

Fields:
- title
- subject
- description
- due date
- priority
- status

Implement:
- list
- create
- edit
- complete
- filter overdue/upcoming

Reuse the existing design system.

Do not add file uploads yet.

Add tests.

Stop.
```

Commit:
```text
feat: add homework tracking
```

---

## PROMPT 31 — Internal Calendar

```text
Build a simple internal calendar page using existing:
- study tasks
- homework
- exams
- revision items

Do not add external calendar integration.

The calendar should link users back to the relevant item.

Keep the UI simple and mobile-friendly.

Add tests for date grouping.

Stop.
```

Commit:
```text
feat: add study calendar
```

---

## PROMPT 32 — Accessibility Review

```text
Perform an accessibility pass across the existing application.

Inspect:
- semantic headings
- form labels
- keyboard navigation
- focus visibility
- button/link semantics
- color contrast
- error messaging
- mobile layout
- reduced-motion considerations

Fix only issues you find.

Do not redesign the application.

Run all tests.

Report the accessibility issues found and fixed.

Stop.
```

Commit:
```text
fix: improve accessibility
```

---

## PROMPT 33 — Security Review

```text
Perform a security review of StudyMate.

Pay special attention to:
- authentication
- authorization
- cross-user data access
- CSRF
- XSS
- secret handling
- AI endpoint abuse
- rate limiting
- unsafe user-controlled content
- Django production settings

Do not add random security dependencies without justification.

Fix real issues.

Add regression tests for authorization boundaries.

Run the full test suite.

Stop.
```

Commit:
```text
fix: harden studymate security
```

---

## PROMPT 34 — Production Readiness

```text
Prepare StudyMate for production deployment.

Implement only well-justified production foundations:
- PostgreSQL-compatible configuration
- environment-based settings
- static file handling
- secure production settings
- logging
- error handling
- deployment documentation
- database migration instructions

Do not deploy automatically.

Add a production checklist to README.

Run all tests.

Stop.
```

Commit:
```text
chore: prepare studymate for production
```

---

# 38. Optional Future Features

Only consider these after the core app is stable:

### Learning
- spaced repetition algorithm
- flashcards
- formula sheets
- textbook progress
- chapter completion maps
- mock exams
- oral revision mode
- study resource library

### AI
- personalized tutor persona
- AI-generated quizzes
- AI-generated flashcards
- mistake pattern analysis
- voice conversation
- image/question solving
- document/PDF question answering
- textbook-aware assistant

### Social
- private study groups
- accountability partner
- shared challenges
- class groups

### Family/Teachers
- parent dashboard
- teacher dashboard
- assignments
- teacher-created tests

### Integrations
- Google Calendar
- email reminders
- mobile app/PWA

These should be treated as **Phase 2/3**, not MVP.

---

# 39. What NOT to Build Early

Avoid these until the core learning loop is strong:

- social feed
- public leaderboard
- complicated avatars
- real-time multiplayer
- full rich-text editor
- video hosting
- browser push notifications
- native mobile application
- microservices
- Kubernetes
- large frontend framework
- complex recommendation ML
- custom authentication
- huge admin dashboard

The first goal is not "many features."

The first goal is:

> **A student can open StudyMate every day and genuinely know what to study, complete it, practice it, and see improvement.**

---

# 40. The MVP Definition

StudyMate MVP is complete when a student can:

```text
1. Create an account
2. Set up a student profile
3. Select subjects
4. See subjects → chapters → topics
5. Create a daily study plan
6. Complete study tasks
7. Track study sessions
8. See progress
9. Take quizzes
10. See weak topics
11. Get revision recommendations
12. Maintain a streak
13. Earn simple achievements
14. Ask StudyMate AI for help
```

Everything else is secondary.

---

# 41. Final Product Loop

The final experience should feel like this:

```text
LOGIN
  ↓
TODAY'S DASHBOARD
  ↓
"What should I do?"
  ↓
STUDY
  ↓
PRACTICE
  ↓
QUIZ
  ↓
RESULT
  ↓
WEAK TOPICS FOUND
  ↓
REVISION QUEUE
  ↓
AI HELP WHEN STUCK
  ↓
PROGRESS IMPROVES
  ↓
NEXT DAY PLAN
```

That loop is the product.

