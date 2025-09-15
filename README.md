[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Library Management System
# LMS
A modern library management system built with Python, PostgreSQL, and Docker. Features full CRUD operations for managing books, members, and loans with a responsive console interface,including GUI administration with PG Admin.

### Database Operations Demonstrated:
- Schema design and migration
- CRUD operations implementation
- Connection pooling and error handling
- Automated database initialization

## Prerequisites

- Python 3.8+
- PostgreSQL 13+
- pip (Python package manager)
### Database Tools Experience:
- **PG Admin**: For GUI-based database management and query optimization
- **psql CLI**: For command-line database operations
- **Python psycopg2**: For programmatic database integration

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/SemheAigbefo/LMS.git
   cd LMS

2. Install Dependencies:
   ```bash
   pip install -r requirements.txt

3. Setup PostgreSQL (ensure it's installed and running)

4. Run the application:
  ```bash
  python main.py

## Troubleshooting

### If pip isn't found:
```bash
# Try pip3 instead
pip3 install -r requirements.txt

# Or ensure pip is in your PATH
python -m pip install -r requirements.txt