## User Management

### Create Student Account
`POST /users/students { "username": "string", "password": "string", "email": "string", "profile": {} }`  
Description: Allows new students to register or be registered by an admin. Includes initial profile details (grade level, accommodations, etc.).

Response Codes:
- 201: Successfully created new student account (returns user object with profile)
- 400: Bad Request
  - Missing required fields (username, password, email)
  - Invalid email format
  - Password doesn't meet requirements (min length: 8, must include numbers and special chars)
  - Invalid profile data (e.g., grade level out of range)
- 409: Conflict - Username or email already exists

Example Request:
```json
{
  "username": "student123",
  "password": "SecurePass123!",
  "email": "student@school.edu",
  "profile": {
    "first_name": "John",
    "last_name": "Doe",
    "grade_level": 6,
    "has_iep": false,
    "iep_summary": null,
    "accommodations": null,
    "iep_goals": null,
    "last_iep_review": null
  }
}
```

Example Success Response:
```json
{
  "id": "uuid-string",
  "username": "student123",
  "email": "student@school.edu",
  "profile": {
    "id": "uuid-string",
    "user_id": "uuid-string",
    "user_type": "student",
    "first_name": "John",
    "last_name": "Doe",
    "type": "student",
    "grade_level": 6,
    "has_iep": false,
    "iep_summary": null,
    "accommodations": null,
    "iep_goals": null,
    "last_iep_review": null
  }
}
```

### Create Teacher Account
`POST /users/teachers { "username": "string", "password": "string", "email": "string", "profile": {} }`  
Description: Allows new teachers to register or be registered by an admin. Includes teacher-specific profile details.

Response Codes:
- 201: Successfully created new teacher account (returns user object with profile)
- 400: Bad Request
  - Missing required fields (username, password, email)
  - Invalid email format
  - Password doesn't meet requirements (min length: 8, must include numbers and special chars)
  - Invalid profile data
- 409: Conflict - Username or email already exists

Example Request:
```json
{
  "username": "teacher123",
  "password": "SecurePass123!",
  "email": "teacher@school.edu",
  "profile": {
    "first_name": "Jane",
    "last_name": "Smith",
    "subject_area": "English"
  }
}
```

Example Success Response:
```json
{
  "id": "uuid-string",
  "username": "teacher123",
  "email": "teacher@school.edu",
  "profile": {
    "id": "uuid-string",
    "user_id": "uuid-string",
    "user_type": "teacher",
    "first_name": "Jane",
    "last_name": "Smith",
    "type": "teacher",
    "subject_area": "English"
  }
}
```

### Create Parent/Guardian Account
`POST /users/guardians { "username": "string", "password": "string", "email": "string", "profile": {} }`  
Description: Allows parents/guardians to set up access for viewing and monitoring their child's progress.

Response Codes:
- 201: Successfully created new guardian account (returns user object with profile)
- 400: Bad Request
  - Missing required fields (username, password, email)
  - Invalid email format
  - Password doesn't meet requirements (min length: 8, must include numbers and special chars)
  - Invalid profile data
- 409: Conflict - Username or email already exists

Example Request:
```json
{
  "username": "parent123",
  "password": "SecurePass123!",
  "email": "parent@email.com",
  "profile": {
    "first_name": "Robert",
    "last_name": "Johnson",
    "student_ids": []
  }
}
```

Example Success Response:
```json
{
  "id": "uuid-string",
  "username": "parent123",
  "email": "parent@email.com",
  "profile": {
    "id": "uuid-string",
    "user_id": "uuid-string",
    "user_type": "parent",
    "first_name": "Robert",
    "last_name": "Johnson",
    "type": "parent",
    "student_ids": []
  }
}
```

### Create Administrative Account
`POST /users/admins { "username": "string", "password": "string", "email": "string", "profile": {} }`  
Description: Used by system administrators to create other administrator accounts.

Response Codes:
- 201: Successfully created new admin account (returns user object with profile)
- 400: Bad Request
  - Missing required fields (username, password, email)
  - Invalid email format
  - Password doesn't meet requirements (min length: 8, must include numbers and special chars)
  - Invalid profile data
- 409: Conflict - Username or email already exists

Example Request:
```json
{
  "username": "admin123",
  "password": "SecurePass123!",
  "email": "admin@school.edu",
  "profile": {
    "first_name": "Admin",
    "last_name": "User",
    "department": "IT"
  }
}
```

Example Success Response:
```json
{
  "id": "uuid-string",
  "username": "admin123",
  "email": "admin@school.edu",
  "profile": {
    "id": "uuid-string",
    "user_id": "uuid-string",
    "user_type": "admin",
    "first_name": "Admin",
    "last_name": "User",
    "type": "admin",
    "department": "IT"
  }
}
```

### Retrieve User Profile
`GET /users/{userId}`  
Description: Fetches all relevant user profile information, including roles, accommodations, and associated data.

Response Codes:
- 200: Successfully retrieved user profile
- 404: User not found

Example Success Response:
```json
{
  "id": "uuid-string",
  "username": "student123",
  "email": "student@school.edu",
  "profile": {
    "id": "uuid-string",
    "user_id": "uuid-string",
    "user_type": "student",
    "first_name": "John",
    "last_name": "Doe",
    "type": "student",
    "grade_level": 6,
    "has_iep": false,
    "iep_summary": null,
    "accommodations": null,
    "iep_goals": null,
    "last_iep_review": null
  }
}
```

### Update User Profile
`POST /users/{userId}`  
Description: Updates user information and profile data. Automatically handles different profile types and performs partial updates, preserving existing values for unspecified fields. Cannot modify the user type/role.

Request Body:
```json
{
  "email": "string",  // Optional
  "profile": {
    "first_name": "string",  // Optional
    "last_name": "string",   // Optional
    // Profile-specific fields based on user type:
    
    // For students:
    "grade_level": 6,
    "has_iep": false,
    "iep_summary": "string",
    
    // For teachers:
    "subject_area": "string",
    
    // For parents:
    "student_ids": [],
    
    // For admins:
    "department": "string"
  }
}
```

Response Codes:
- 200: Successfully updated user profile
- 400: Bad Request
  - Invalid email format
  - Invalid profile data for user type
  - Attempt to modify user type/role
- 404: User not found

Example Request (updating a student):
```json
{
  "email": "new.email@school.edu",
  "profile": {
    "first_name": "Johnny",
    "grade_level": 7,
    "iep_summary": "Updated accommodations needed"
  }
}
```

Example Success Response:
```json
{
  "id": "uuid-string",
  "username": "student123",
  "email": "new.email@school.edu",
  "profile": {
    "id": "uuid-string",
    "user_id": "uuid-string",
    "user_type": "student",
    "first_name": "Johnny",
    "last_name": "Doe",
    "type": "student",
    "grade_level": 7,
    "has_iep": false,
    "iep_summary": "Updated accommodations needed",
    "accommodations": null,
    "iep_goals": null,
    "last_iep_review": null
  }
}
```

### Delete User
`DELETE /users/{userId}`  
Description: Permanently removes a user and their associated profile from the system. This action cannot be undone.

Response Codes:
- 204: Successfully deleted user (no content returned)
- 404: User not found
- 403: Forbidden - Insufficient permissions to delete user

---

## Authentication & Session

### Login
`POST /auth/login`  
Description: Authenticates a user and returns access and refresh tokens in the response.

Request Body:
```json
{
  "username": "string",
  "password": "string"
}
```

Response Codes:
- 200: Successfully authenticated
- 400: Bad Request - Missing or invalid credentials
- 401: Unauthorized - Invalid username or password

Example Success Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Logout
`POST /auth/logout`  
Description: Invalidates the current user's session and blacklists their tokens.

Headers:
- Authorization: Bearer {access_token}

Response Codes:
- 200: Successfully logged out
- 401: Unauthorized - Invalid or missing token

### Refresh Token
`POST /auth/refresh`  
Description: Issues a new access token using a valid refresh token.

Headers:
- Authorization: Bearer {refresh_token}

Response Codes:
- 200: Successfully refreshed access token
- 401: Unauthorized - Invalid or expired refresh token

Example Success Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

---

## Writing Portfolio & Assignments

### Create Writing Piece
`POST /students/{studentId}/portfolio`  
Description: Adds a new piece of writing to the student's portfolio. Supports rich text content, privacy settings, and optional metadata like narrative chapter assignments. Teachers can also create pieces on behalf of students.

Headers:
- Authorization: Bearer {access_token}

Response Codes:
- 201: Successfully created writing piece
- 400: Bad Request
  - Missing required fields (title, content)
  - Invalid privacy setting
  - Invalid narrative chapter number
- 401: Unauthorized - Not authenticated
- 403: Forbidden - Not authorized to create for this student
- 404: Student not found

Example Request:
```json
{
    "title": "My First Essay",
    "content": "This is the content of my essay...",
    "privacy": "private",
    "narrativeChapter": 1,
    "tags": ["draft", "essay", "narrative"],
    "metadata": {
        "assignmentId": "uuid-string",
        "dueDate": "2024-03-20T00:00:00Z",
        "status": "draft"
    }
}
```

Example Success Response:
```json
{
    "id": "uuid-string",
    "studentId": "uuid-string",
    "title": "My First Essay",
    "content": "This is the content of my essay...",
    "privacy": "private",
    "narrativeChapter": 1,
    "tags": ["draft", "essay", "narrative"],
    "metadata": {
        "assignmentId": "uuid-string",
        "dueDate": "2024-03-20T00:00:00Z",
        "status": "draft"
    },
    "created_at": "2024-03-19T15:30:00Z",
    "updated_at": "2024-03-19T15:30:00Z"
}
```

### Retrieve Student Portfolio
`GET /students/{studentId}/portfolio`  
Description: Returns all writing pieces associated with a student. Supports filtering by chapter, status, privacy, tags, and date range. Results are paginated and can be sorted by various fields.

Headers:
- Authorization: Bearer {access_token}

Query Parameters:
- chapter: (optional) Filter by narrative chapter
- status: (optional) Filter by status (draft, submitted, graded)
- privacy: (optional) Filter by privacy setting
- tags: (optional) Filter by comma-separated tags
- from: (optional) Start date for filtering
- to: (optional) End date for filtering
- limit: (optional) Number of items per page (default: 10)
- offset: (optional) Pagination offset (default: 0)
- sort: (optional) Sort field (created_at, updated_at, title)
- order: (optional) Sort order (asc, desc)

Response Codes:
- 200: Successfully retrieved portfolio
- 401: Unauthorized - Not authenticated
- 403: Forbidden - Not authorized to view this student's portfolio
- 404: Student not found

Example Success Response:
```json
{
    "total": 45,
    "limit": 10,
    "offset": 0,
    "items": [
        {
            "id": "uuid-string",
            "title": "My First Essay",
            "preview": "First 100 characters...",
            "privacy": "private",
            "narrativeChapter": 1,
            "tags": ["draft", "essay"],
            "metadata": {
                "status": "draft",
                "dueDate": "2024-03-20T00:00:00Z"
            },
            "created_at": "2024-03-19T15:30:00Z",
            "updated_at": "2024-03-19T15:30:00Z"
        }
    ]
}
```

### Retrieve Single Writing Piece
`GET /students/{studentId}/portfolio/{writingId}`  
Description: Retrieves a specific writing piece with full content, feedback history, and version tracking. Teachers can access pieces shared with them or their class.

Headers:
- Authorization: Bearer {access_token}

Response Codes:
- 200: Successfully retrieved writing piece
- 401: Unauthorized - Not authenticated
- 403: Forbidden - Not authorized to view this writing piece
- 404: Writing piece not found

Example Success Response:
```json
{
    "id": "uuid-string",
    "studentId": "uuid-string",
    "title": "My First Essay",
    "content": "Full essay content...",
    "privacy": "private",
    "narrativeChapter": 1,
    "tags": ["draft", "essay"],
    "metadata": {
        "assignmentId": "uuid-string",
        "dueDate": "2024-03-20T00:00:00Z",
        "status": "draft"
    },
    "feedback": [
        {
            "id": "uuid-string",
            "teacherId": "uuid-string",
            "comment": "Great start! Consider expanding your conclusion.",
            "score": 85,
            "created_at": "2024-03-19T16:00:00Z"
        }
    ],
    "version_history": [
        {
            "version": 1,
            "saved_at": "2024-03-19T15:30:00Z",
            "changes": "Initial draft"
        }
    ],
    "created_at": "2024-03-19T15:30:00Z",
    "updated_at": "2024-03-19T15:30:00Z"
}
```

### Update Writing Piece
`PATCH /students/{studentId}/portfolio/{writingId}`  
Description: Updates an existing writing piece. Supports partial updates and maintains version history. Students can only update their own pieces unless a teacher override is present.

Headers:
- Authorization: Bearer {access_token}
- If-Match: "etag" (optional) - Ensures update only if the piece hasn't been modified

Response Codes:
- 200: Successfully updated writing piece
- 400: Bad Request - Invalid update data
- 401: Unauthorized - Not authenticated
- 403: Forbidden - Not authorized to update this writing piece
- 404: Writing piece not found
- 409: Conflict - Piece was modified by another user

Example Request:
```json
{
    "title": "My Improved Essay",
    "content": "Updated content...",
    "privacy": "class",
    "tags": ["essay", "final"],
    "metadata": {
        "status": "submitted"
    }
}
```

Example Success Response:
```json
{
    "id": "uuid-string",
    "studentId": "uuid-string",
    "title": "My Improved Essay",
    "content": "Updated content...",
    "privacy": "class",
    "narrativeChapter": 1,
    "tags": ["essay", "final"],
    "metadata": {
        "assignmentId": "uuid-string",
        "dueDate": "2024-03-20T00:00:00Z",
        "status": "submitted"
    },
    "created_at": "2024-03-19T15:30:00Z",
    "updated_at": "2024-03-19T16:45:00Z"
}
```

### Delete Writing Piece
`DELETE /students/{studentId}/portfolio/{writingId}`  
Description: Permanently removes a writing piece from the student's portfolio. This action cannot be undone. Teachers can only delete pieces in specific circumstances (e.g., inappropriate content).

Headers:
- Authorization: Bearer {access_token}
- If-Match: "etag" (optional) - Ensures deletion only if the piece hasn't been modified

Response Codes:
- 204: Successfully deleted writing piece
- 401: Unauthorized - Not authenticated
- 403: Forbidden - Not authorized to delete this writing piece
- 404: Writing piece not found

Additional Notes:
- All endpoints require a valid access token in the Authorization header
- All endpoints support ETags for caching
- List endpoints include pagination headers (X-Total-Count, Link)
- Rate limiting headers are included (X-RateLimit-Limit, X-RateLimit-Remaining)
- All timestamps are in ISO 8601 format with UTC timezone
- All IDs are UUIDs

---

## Accessibility & Accommodations

### Update Accommodations
`PATCH /users/{userId}/accommodations { "voiceToText": true, "formatMode": "dyslexiaFriendly", ... }`  
Description: Allows students, teachers (with permissions), or admins to modify a user's accommodations settings.

Headers:
- Authorization: Bearer {access_token}

### Retrieve Accommodations
`GET /users/{userId}/accommodations`  
Description: Fetches a user's current accommodations setup for dynamic display and usage in the app.

Headers:
- Authorization: Bearer {access_token}

---

## Privacy & Sharing

### Update Privacy Settings for a Writing Piece
`PATCH /students/{studentId}/portfolio/{writingId}/privacy { "privacy": "private|class|public" }`  
Description: Allows students to set or change who can see their work (e.g., private, shared with teacher, or shared with class).

Headers:
- Authorization: Bearer {access_token}
- If-Match: "etag" (optional)

### Retrieve Sharing / Visibility Options
`GET /students/{studentId}/portfolio/{writingId}/privacy`  
Description: Returns the current sharing or visibility setting for that piece of writing.

Headers:
- Authorization: Bearer {access_token}

---

## Teacher & Student Progress

### Get Student Progress (Teacher or Student)
`GET /progress/{studentId}`  
Description: Provides analytics, achievements, and progress indicators (e.g. grammar improvement, narrative completion) to teachers or the student themselves.

Headers:
- Authorization: Bearer {access_token}

### Update Student Progress
`PATCH /progress/{studentId} { "metrics": { "grammarErrors": 5, "writingComplexity": 7 }, "feedbackNotes": "string" }`  
Description: Enables teachers (or automated AI routines) to record new progress metrics or feedback.

Headers:
- Authorization: Bearer {access_token}
- If-Match: "etag" (optional)

### Provide Feedback on Writing
`POST /students/{studentId}/portfolio/{writingId}/feedback { "comments": "string", "score": 85 }`  
Description: Teachers can comment on a writing piece and optionally add a score or other rubric-based evaluations.

Headers:
- Authorization: Bearer {access_token}

---

## Curriculum & Assignment Management

### Create Curriculum Path
`POST /curriculum { "title": "string", "description": "string", "modules": [ ... ] }`  
Description: For teachers or curriculum writers to add a new structured path that includes various writing modules or lessons.

Headers:
- Authorization: Bearer {access_token}

### Retrieve All Curricula
`GET /curriculum`  
Description: Lists all curriculum paths available for teachers or schools.

Headers:
- Authorization: Bearer {access_token}

### Retrieve Single Curriculum
`GET /curriculum/{curriculumId}`  
Description: Fetches details about a specific curriculum path and its modules.

Headers:
- Authorization: Bearer {access_token}

### Update Curriculum
`PATCH /curriculum/{curriculumId} { "title": "string", "description": "string", "modules": [ ... ] }`  
Description: Modifies an existing curriculum path.

Headers:
- Authorization: Bearer {access_token}
- If-Match: "etag" (optional)

### Delete Curriculum
`DELETE /curriculum/{curriculumId}`  
Description: Removes a specified curriculum path from the system.

Headers:
- Authorization: Bearer {access_token}
- If-Match: "etag" (optional)

### Assign Curriculum to Class
`POST /curriculum/{curriculumId}/assign { "classId": "string" }`  
Description: Lets a teacher link a specific curriculum path to a class or group of students.

Headers:
- Authorization: Bearer {access_token}

---

## Parent/Guardian Access

### Retrieve Child Progress
`GET /guardians/{guardianId}/students/{studentId}/progress`  
Description: Shows a high-level snapshot of a child's progress, achievements, or shared writing pieces.

Headers:
- Authorization: Bearer {access_token}

### List Shared Writings
`GET /guardians/{guardianId}/students/{studentId}/shareable-writings`  
Description: Returns a list of writing pieces a student has marked as shareable with their guardian.

Headers:
- Authorization: Bearer {access_token}

---

## Administrative Features

### Manage User Accounts & Permissions
`POST /admin/users/{userId}/role { "role": "teacher|student|guardian|admin" }`  
Description: Allows an admin to change or grant roles/permissions to a user.

Headers:
- Authorization: Bearer {access_token}

### Set Organization-Wide Privacy Policy
`PATCH /admin/settings/privacy-policy { "policyText": "string", "restrictions": [ ... ] }`  
Description: Configures privacy constraints or disclaimers for the entire organization.

Headers:
- Authorization: Bearer {access_token}
- If-Match: "etag" (optional)

### Bulk User Import/Export
`POST /admin/users/bulk-import { "csvFile": "attachment" }`  
Description: Bulk import new or updated user data from a CSV file.

Headers:
- Authorization: Bearer {access_token}
- Content-Type: multipart/form-data

`GET /admin/users/bulk-export`  
Description: Generates a CSV file of current user data for administrative audits or data backup.

Headers:
- Authorization: Bearer {access_token}

---

## Content & Prompt Management (Curriculum Writers)

### Create Base Prompt Template
`POST /prompts { "title": "string", "content": "string", "tags": [ "grammar", "narrative" ] }`  
Description: Lets curriculum writers create reusable prompt templates for AI personalization.

Headers:
- Authorization: Bearer {access_token}

### Retrieve All Prompts
`GET /prompts`  
Description: Lists all available prompts with filtering options (e.g. tag-based).

Headers:
- Authorization: Bearer {access_token}

### Retrieve Single Prompt
`GET /prompts/{promptId}`  
Description: Gets one prompt template for editing or reference.

Headers:
- Authorization: Bearer {access_token}

### Update Prompt
`PATCH /prompts/{promptId} { "title": "string", "content": "string", "tags": [ ... ] }`  
Description: Allows refinement of an existing prompt template.

Headers:
- Authorization: Bearer {access_token}
- If-Match: "etag" (optional)

### Delete Prompt
`DELETE /prompts/{promptId}`  
Description: Removes an outdated or invalid prompt template.

Headers:
- Authorization: Bearer {access_token}
- If-Match: "etag" (optional)

### Track Prompt Effectiveness
`GET /prompts/{promptId}/analytics`  
Description: Provides details on how often a prompt is used and its impact on student engagement.

Headers:
- Authorization: Bearer {access_token}
