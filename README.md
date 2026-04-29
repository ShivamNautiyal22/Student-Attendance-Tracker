# Student Attendance Tracker

A comprehensive web-based application for managing student attendance digitally.

## Features

- Real-time attendance marking
- Student enrollment management
- Attendance reports and analytics
- Role-based access (Students, Teachers, Admins)
- RESTful APIs
- Responsive design

## Quick Start

### Installation

1. Clone the repository
```bash
git clone https://github.com/YOUR_ORG/student-attendance-tracker.git
cd student-attendance-tracker
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Setup database
```bash
python manage.py migrate
python manage.py createsuperuser
```

5. Run development server
```bash
python manage.py runserver
```

Access the application at http://localhost:8000

## Team Structure

- **HE38409**: DevOps & Project Coordinator
- **HE38712**: Frontend Developer
- **HE38711**: Backend Developer (Student Service)
- **HE39026**: Backend Developer (Attendance Service)
- **HE38698**: Site Reliability Engineer
- **HE38379**: Testing & QA Engineer