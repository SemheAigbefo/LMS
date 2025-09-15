# Library Management System - Testing Guide

## Database Authentication Testing

### Pre-requisites
- PostgreSQL installed and running
- LMS database created (automatically handled by the application)
- Test librarian credentials available

### Test Librarian Accounts
The system comes with these pre-configured test accounts:

| Librarian ID | Name          |
|--------------|---------------|
| 70552        | Chloe Smith   |
| 70704        | Ben Carter    |
| 70895        | Alice Johnson |

### Testing Scenarios

#### 1. Successful Authentication
- Select "Librarian" at main menu
- Enter valid ID (e.g., 70552)
- Expected: Access granted with welcome message

#### 2. Failed Authentication
- Select "Librarian" at main menu  
- Enter invalid ID (e.g., 99999)
- Expected: "Access denied" message

#### 3. Database Connection Issues
- Stop PostgreSQL service
- Attempt librarian login
- Expected: Appropriate error message

### Reset Database State
Run the application again to reinitialize with test data:
```bash
python your_main_file.py