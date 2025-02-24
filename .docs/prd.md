# ScribeX Product Requirements Document

## Overview
ScribeX transforms English language arts education by making grammar and writing practice engaging and personalized for middle school students. Our platform combines adaptive learning technology with game-like elements to help students develop strong writing skills while staying motivated.

## Description
ScribeX delivers personalized writing instruction through:
- Reflexive  Exercise on Direct Instruction: Interactive lessons that adapt to each student's skill level
- Open World Learning: Story-driven exercises that build into larger narratives
- Immediate feedback and progress tracking
- Accessibility tools for diverse learning needs
- Game-like elements for sustained engagement
- Progressive and iterative writing assignments that build into a larger narrative
- Freeform writing allowing to use platform tools for personal expression and engagement according to stdents enjoyment and engagement.

Think Duolingo's engagement model, but specifically crafted for mastering English writing and grammar skills in a classroom context.

## License
This project is licensed under the BSD 3-Clause License. See LICENSE file for full details.


## Core User Stories

### Student Experience

#### Essential Features
1. Writing Portfolio Management
   ```user-story
   As a student, I want to:
   - learn through engaging lessons with automated feedback
   - Track my progress through visual indicators
   - Create writing pieces that build into a larger narrative
   - Have my work automatically compiled into a portfolio
   ```

2. Accessibility & Accommodations
   ```user-story
   As a student with learning accommodations, I want to:
   - Use voice-to-text features to overcome writing barriers
   - Have my work automatically formatted to support my learning needs
   - Receive prompts adapted to my specific learning goals
   ```

3. Privacy & Sharing
   ```user-story
   As a student, I want to:
   - Choose privacy settings for each piece of my work
   - Share achievements with teachers and family
   - Control who can view my writing portfolio
   ```

### Teacher Experience

#### Essential Features
1. Curriculum Management
   ```user-story
   As a teacher, I want to:
   - Customize curriculum paths for different classes
   - Review and modify AI-generated prompts
   - Create IEP-aligned learning objectives
   ```

2. Student Progress Tracking
   ```user-story
   As a teacher, I want to:
   - Monitor student progress in real-time
   - Access analytics about student engagement
   - Generate IEP progress reports
   - Provide efficient feedback through integrated tools
   ```

### Parent/Guardian Experience

#### Essential Features
1. Progress Monitoring
   ```user-story
   As a parent/guardian, I want to:
   - View my student's progress within authorized access levels
   - See examples of shared work
   - Access relevant data for educational planning
   ```

### Administrative Features

#### Essential Features
1. Content Management
   ```user-story
   As a curriculum writer, I want to:
   - Create base prompt templates for AI personalization
   - Tag and categorize prompts for easy discovery
   - Track prompt effectiveness
   ```

2. System Administration
   ```user-story
   As an org admin, I want to:
   - Manage user accounts and permissions
   - Handle access issues quickly
   - Set organization-wide privacy policies
   ```

## Interface Requirements

### Student Interface
#### Mobile-First Design
- Primary access through progressive web app
- Optimized for phone and tablet use
- Secondary access through web browsers
- Views:
  - Home
    - Settings
    - Profile
  - Writing
    - Assignments
    - Open World Learning
    - Freeform Writing
  - Social
    - Posts
    - Teacher Messages
    - Leaderboard
### Teacher Interface
#### Web-Only Design
- Optimized for desktop/laptop browsers
- Dashboard-focused layout
- Breadcrumb Navigation
- Views
  - class list
    - split view of students and assignments
      - student
        - grades
        - leaderboard topline number and position
        - IEP deatails (goals and targets)
        - writing samples
        - assignment details
      - assignment
        - assignments list
          - assignment details
        - assignments x students 2d grid with selectable completion status and grades. 
        

### Parent/Guardian Interface
#### Desktop-First Design
- Primary access through web 
- Views
  - Home
    - child writing samlples with child view filter
    - teacher messages
    - sidebar with child summary card
      - child name
      - child leaderboard topline number
      - child grade
      - child class name


### Cross-Platform Considerations
- Consistent branding and visual language (cyberpunk botanical futurism, synthwave)
- Shared notification system
- Synchronized data across all platforms
- Accessibility compliance on all interfaces
- Security features appropriate to each access type

## Technical Requirements
[Condensed version from preprd_techs.md, focusing on key architecture decisions]

### Core Architecture
- Python FastAPI Microservices
- PostgreSQL + MongoDB for different data needs
- React Progressive Web App frontend

### AI Integration
- Three-Layer Analysis:
  - Mechanics & Grammar: Sapling API
  - Sequencing & Logic: GPT-4 (to be refined)
  - Voice & Rhetoric: GPT-4 (to be refined)
- Voice-to-Text: Whisper API
- Writer's Block Assistance: GPT-4

### Learning Outcomes
- Writing complexity improvement
- Grammar error reduction rate
- IEP goal achievement rate

### Teacher Effectiveness
- Feedback response time
- Curriculum customization frequency
- Student progress monitoring activity

## Development Phases

### Phase 1: MVP (1 week)
- Basic writing interface
- Core student/teacher views
- Basic AI grammar checking

### Phase 2: Enhanced Features (2 weeks)
- Portfolio system
- Essential accessibility features
- Parent portal

### Phase 3: Platform Expansion (3 months)
- Advanced analytics
- Integration capabilities
- Enhanced AI features
- Performance optimization

## Security & Compliance

### Data Protection
- FERPA compliance
- COPPA compliance
- End-to-end encryption
- Regular security audits

### Access Control
- Role-based permissions
- Session management
- Audit logging
