# JobPortal - Flask Job Board Application

## Overview

JobPortal is a comprehensive job board web application built with Flask that enables users to browse and apply for jobs, while allowing administrators to manage job postings and review applications. The system supports role-based access control with separate interfaces for regular users and administrators.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask web framework with Python
- **Database**: SQLAlchemy ORM with configurable database backends (defaults to SQLite, supports PostgreSQL via DATABASE_URL environment variable)
- **Authentication**: Flask-Login for session management with password hashing using Werkzeug
- **Forms**: Flask-WTF for form handling and validation with CSRF protection
- **File Handling**: Werkzeug for secure file uploads with size limits

### Frontend Architecture
- **Templates**: Jinja2 templating engine with template inheritance
- **CSS Framework**: Bootstrap 5 with dark theme support
- **Icons**: Font Awesome for consistent iconography
- **JavaScript**: Vanilla JavaScript with Bootstrap components for interactive elements

### Database Schema
The application uses three main models:
- **User**: Handles user accounts with role-based permissions (regular users vs administrators)
- **Job**: Stores job postings with company information, requirements, and application deadlines
- **Application**: Links users to jobs they've applied for with status tracking

## Key Components

### Authentication System
- User registration and login functionality
- Password hashing for security
- Session-based authentication with Flask-Login
- Role-based access control (admin vs regular users)

### Job Management
- Job posting creation and editing (admin only)
- Job browsing with search and filtering capabilities
- Job detail pages with application functionality
- Application deadline tracking

### Application System
- Resume upload functionality with file validation
- Application status tracking (pending, reviewed, accepted, rejected)
- Cover letter support
- Application history for users

### Admin Dashboard
- Statistics overview (total jobs, applications, etc.)
- Job management interface
- Application review system with status updates
- User management capabilities

### File Upload System
- Secure file upload handling
- 16MB file size limit
- Upload directory management
- File type validation for resumes

## Data Flow

1. **User Registration/Login**: Users create accounts or authenticate through the login system
2. **Job Browsing**: Users can search and filter available job postings
3. **Job Application**: Authenticated users can apply to jobs with resumes and cover letters
4. **Admin Review**: Administrators can review applications and update their status
5. **User Tracking**: Users can monitor their application status through their dashboard

## External Dependencies

### Python Packages
- Flask: Web framework
- Flask-SQLAlchemy: Database ORM
- Flask-Login: Authentication management
- Flask-WTF: Form handling and validation
- Werkzeug: WSGI utilities and security functions

### Frontend Libraries
- Bootstrap 5: CSS framework with dark theme
- Font Awesome: Icon library
- Custom CSS and JavaScript for enhanced user experience

### Database Support
- SQLite: Default development database
- PostgreSQL: Production database support via DATABASE_URL environment variable

## Deployment Strategy

### Configuration Management
- Environment-based configuration using os.environ
- Separate settings for development and production
- Database URL configuration for different environments
- Session secret management

### File Storage
- Local file storage in uploads directory
- Configurable upload path
- File size and type restrictions

### Security Features
- CSRF protection on all forms
- Password hashing
- Secure file upload handling
- ProxyFix middleware for proper header handling behind proxies

### Development Setup
- Debug mode enabled for development
- SQLite database for local development
- Hot reloading for development efficiency

The application is designed to be easily deployable on platforms like Replit, with environment variable configuration for database connections and session management.
