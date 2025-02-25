## User Management

### Create Student Account
`POST /users/students { "username": "string", "password": "string", "email": "string", "profile": {} }`  
Description: Allows new students to register or be registered by an admin. Includes initial profile details (grade level, accommodations, etc.).

### Create Teacher Account
`POST /users/teachers { "username": "string", "password": "string", "email": "string", "profile": {} }`  
Description: Allows new teachers to register or be registered by an admin. Includes teacher-specific profile details.

### Create Parent/Guardian Account
`POST /users/guardians { "username": "string", "password": "string", "email": "string", "profile": {} }`  
Description: Allows parents/guardians to set up access for viewing and monitoring their child’s progress.

### Create Administrative Account
`POST /users/admins { "username": "string", "password": "string", "email": "string", "profile": {} }`  
Description: Used by system administrators to create other administrator accounts.

### Retrieve User Profile
`GET /users/{userId}`  
Description: Fetches all relevant user profile information, including roles, accommodations, and associated data.

### Update User Profile
`POST /users/{userId} { "email": "string", "profile": { ... } }`  
Description: Edits user profile information (e.g. name, accommodations, contact info).

### Delete User
`DELETE /users/{userId}`  
Description: Removes a user from the system and revokes all associated access.

---

## Authentication & Session

### Login
`POST /auth/login { "username": "string", "password": "string" }`  
Description: Authenticates a user and returns a session token or JWT for subsequent requests.

### Logout
`POST /auth/logout { "token": "jwtString" }`  
Description: Invalidates a user’s authentication session.

### Refresh Token
`POST /auth/refresh { "refreshToken": "jwtString" }`  
Description: Provides a new access token if a user’s current session is about to expire.

---

## Writing Portfolio & Assignments

### Create Writing Piece
`POST /students/{studentId}/portfolio { "title": "string", "content": "string", "privacy": "enum", "narrativeChapter": 1 }`  
Description: Adds a new piece of writing to the student’s portfolio with optional privacy settings and narrative chapter annotation.

### Retrieve Student Portfolio
`GET /students/{studentId}/portfolio`  
Description: Returns all writing pieces associated with a specific student, optionally filtered by narrative chapter, assignment type, or privacy.

### Retrieve Single Writing Piece
`GET /students/{studentId}/portfolio/{writingId}`  
Description: Gets one specific writing piece by ID.

### Update Writing Piece
`PATCH /students/{studentId}/portfolio/{writingId} { "title": "string", "content": "string", "privacy": "enum" }`  
Description: Edits an existing writing piece, including content or privacy settings.

### Delete Writing Piece
`DELETE /students/{studentId}/portfolio/{writingId}`  
Description: Permanently removes a writing piece from the student’s portfolio.

---

## Accessibility & Accommodations

### Update Accommodations
`PATCH /users/{userId}/accommodations { "voiceToText": true, "formatMode": "dyslexiaFriendly", ... }`  
Description: Allows students, teachers (with permissions), or admins to modify a user’s accommodations settings.

### Retrieve Accommodations
`GET /users/{userId}/accommodations`  
Description: Fetches a user’s current accommodations setup for dynamic display and usage in the app.

---

## Privacy & Sharing

### Update Privacy Settings for a Writing Piece
`PATCH /students/{studentId}/portfolio/{writingId}/privacy { "privacy": "private|class|public" }`  
Description: Allows students to set or change who can see their work (e.g., private, shared with teacher, or shared with class).

### Retrieve Sharing / Visibility Options
`GET /students/{studentId}/portfolio/{writingId}/privacy`  
Description: Returns the current sharing or visibility setting for that piece of writing.

---

## Teacher & Student Progress

### Get Student Progress (Teacher or Student)
`GET /progress/{studentId}`  
Description: Provides analytics, achievements, and progress indicators (e.g. grammar improvement, narrative completion) to teachers or the student themselves.

### Update Student Progress
`PATCH /progress/{studentId} { "metrics": { "grammarErrors": 5, "writingComplexity": 7 }, "feedbackNotes": "string" }`  
Description: Enables teachers (or automated AI routines) to record new progress metrics or feedback.

### Provide Feedback on Writing
`POST /students/{studentId}/portfolio/{writingId}/feedback { "comments": "string", "score": 85 }`  
Description: Teachers can comment on a writing piece and optionally add a score or other rubric-based evaluations.

---

## Curriculum & Assignment Management

### Create Curriculum Path
`POST /curriculum { "title": "string", "description": "string", "modules": [ ... ] }`  
Description: For teachers or curriculum writers to add a new structured path that includes various writing modules or lessons.

### Retrieve All Curricula
`GET /curriculum`  
Description: Lists all curriculum paths available for teachers or schools.

### Retrieve Single Curriculum
`GET /curriculum/{curriculumId}`  
Description: Fetches details about a specific curriculum path and its modules.

### Update Curriculum
`PATCH /curriculum/{curriculumId} { "title": "string", "description": "string", "modules": [ ... ] }`  
Description: Modifies an existing curriculum path.

### Delete Curriculum
`DELETE /curriculum/{curriculumId}`  
Description: Removes a specified curriculum path from the system.

### Assign Curriculum to Class
`POST /curriculum/{curriculumId}/assign { "classId": "string" }`  
Description: Lets a teacher link a specific curriculum path to a class or group of students.

---

## Parent/Guardian Access

### Retrieve Child Progress
`GET /guardians/{guardianId}/students/{studentId}/progress`  
Description: Shows a high-level snapshot of a child’s progress, achievements, or shared writing pieces.

### List Shared Writings
`GET /guardians/{guardianId}/students/{studentId}/shareable-writings`  
Description: Returns a list of writing pieces a student has marked as shareable with their guardian.

---

## Administrative Features

### Manage User Accounts & Permissions
`POST /admin/users/{userId}/role { "role": "teacher|student|guardian|admin" }`  
Description: Allows an admin to change or grant roles/permissions to a user.

### Set Organization-Wide Privacy Policy
`PATCH /admin/settings/privacy-policy { "policyText": "string", "restrictions": [ ... ] }`  
Description: Configures privacy constraints or disclaimers for the entire organization.

### Bulk User Import/Export
`POST /admin/users/bulk-import { "csvFile": "attachment" }`  
Description: Bulk import new or updated user data from a CSV file.

`GET /admin/users/bulk-export`  
Description: Generates a CSV file of current user data for administrative audits or data backup.

---

## Content & Prompt Management (Curriculum Writers)

### Create Base Prompt Template
`POST /prompts { "title": "string", "content": "string", "tags": [ "grammar", "narrative" ] }`  
Description: Lets curriculum writers create reusable prompt templates for AI personalization.

### Retrieve All Prompts
`GET /prompts`  
Description: Lists all available prompts with filtering options (e.g. tag-based).

### Retrieve Single Prompt
`GET /prompts/{promptId}`  
Description: Gets one prompt template for editing or reference.

### Update Prompt
`PATCH /prompts/{promptId} { "title": "string", "content": "string", "tags": [ ... ] }`  
Description: Allows refinement of an existing prompt template.

### Delete Prompt
`DELETE /prompts/{promptId}`  
Description: Removes an outdated or invalid prompt template.

### Track Prompt Effectiveness
`GET /prompts/{promptId}/analytics`  
Description: Provides details on how often a prompt is used and its impact on student engagement.
