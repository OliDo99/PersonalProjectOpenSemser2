# Employee Scheduling System - Project Documentation

## Project Overview
This project implements an employee scheduling system for Dominos with user authentication, availability management, and automated schedule generation. The system allows employees to input their availability and administrators to generate and manage work schedules based on staffing requirements.

## Key Performance Indicators

### 1. Manage & Control
- **Infrastructure Management:**
  - Implemented Flask-based web application with clear separation of concerns
  - Utilized JSON file storage for data persistence ( will use DB for final Demo)
  - Established user authentication system with admin and regular user roles
  - Maintained version control and project structure

**Evidence:**
- Authentication system in `auth.py`
- Structured data storage in JSON files (`availability.json`, `schedule.json`, etc.)
- Later I will use a DB
- Clear project organization with separate static and template directories

### 2. Realise
- **Software Development:**
  - Developed core scheduling algorithm in `schedule.py`
  - Implemented user interface with HTML templates and CSS styling
  - Created REST API endpoints for data management
  - Integrated authentication with application features

**Evidence:**
- Schedule generation algorithm in `ScheduleGenerator` class
- REST endpoints in `main.py` for availability and schedule management
- Responsive UI design in `static/css/style.css`
- Integration testing capabilities in `templates/testing.html`

### 3. Design
- **Component Architecture:**
  - Designed modular system with separate components for:
    - Authentication (auth.py)
    - Schedule Generation (schedule.py)
    - User Interface (templates/)
    - API Endpoints (main.py)
  - Implemented responsive and user-friendly interface
  - Created reusable CSS components

**Evidence:**
- Modular blueprint system for authentication
- Reusable UI components in templates
- Structured CSS with clear naming conventions
- JSON-based data models for flexibility

### 4. Advise
- **Process Organization:**
  - Implemented clear user workflows for:
    - Availability submission
    - Schedule generation
    - Administrative controls
  - Established data validation procedures
  - Created user-friendly error handling

**Evidence:**
- Structured route handlers in `main.py`
- Form validation and error handling in templates
- Clear separation between admin and user functionalities
- Informative flash messages for user feedback

### 5. Analysis
- **Development Process:**
  - Analyzed requirements for:
    - User authentication
    - Schedule generation algorithm
    - Data storage needs
  - Implemented solutions using established patterns
  - Created structured error handling and validation

**Evidence:**
- Requirements implementation in schedule generation algorithm
- Data validation in route handlers
- Error handling in availability management
- Clear separation of concerns in codebase

## Technical Stack
- **Backend:** Python with Flask framework
- **Frontend:** HTML, CSS, JS
- **Data Storage:** JSON files, DB
- **Authentication:** Flask-Login
- **UI Framework:** Custom CSS

## To Do
1. Database Implementation: Replace JSON storage with a DB
2. Scadule Implementation: Make the scedule dynamically chose the workers
3. Scalibilty Issues: Reslove the issules when scaling the app
4. Enhanced Error Handling: Add more comprehensive error messages
5. Performance Optimization: Improve schedule generation algorithm efficiency

## Development Log
**11.4**: 
  - Initial research on Linux systems and development environment setup
  - Installed Ubuntu WSL for development
  - Researched Flask framework capabilities
  - Discused with my brother

**13.4**: 
  - Development of environment
  - Configured Ubuntu development environment
  - Created initial project documentation

**14.4**: 
  - Authentication system implementation
  - Developed user authentication system
  - Implemented login/logout functionality
  - Created user roles (admin/employee)

**15.4**: 
  - Data storage implementation
  - Updating JSON file structure for data storage
  - Created basic CRUD operations
  - Feedback session with my brother


**1.5**: 
  - UI development
  - Designed basic HTML templates
  - Implemented CSS styling
  - Created responsive layout

**2.5**: 
  - Calendar functionality
  - Implemented calendar view
  - Added availability input system
  - Created date handling utilities

**3.5**: 
  - Schedule generation algorithm
  - Developed core scheduling logic
  - Implemented employee availability checking
  - Added basic conflict resolution

**4.5**: 
  - Admin dashboard development
  - Created admin interface
  - Implemented staff requirement settings
  - Added schedule management features

**5.5**: 
  - Testing and debugging
  - Implemented error handling
  - Added input validation
  - Fixed authentication issues

**10.5**: 
  - Enhancement and optimization
  - Schedule generation algorithm // still not working 
  - Optimized data loading
  - Error handling

**15.5**: Documentation and code cleanup
  - Schedule generation algorithm // still not working 
  - Updated project documentation
  - Refactored code for better maintainability

**17.5**: 
  - Enhanced schedule timeline view
    - Implemented daily view with time-based grid
    - Added visual timeline for employee availability
    - Improved navigation between days
  - Optimized CSS structure
    - Removed redundant styles and duplicates
    - Consolidated shared styles using CSS variables
    - Improved maintainability with better organization
  - Extended availability data
    - Added more comprehensive test data
    - Extended availability through end of May 2025
    - Varied shift patterns for better testing
