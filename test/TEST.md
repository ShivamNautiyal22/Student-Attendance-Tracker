# Testing Document — Student Attendance Tracker (Manual QA)

**Role:** Tester / QA Engineer  
**Goal:** Quickly confirm the main student + teacher workflows work and don’t crash.

---

## 1) What we tested (Scope)

**P0 (Must work)**
- Register / Login / Logout
- Student: open dashboard, mark attendance
- Teacher: open dashboard, verify/reject attendance
- Access control (student can’t open teacher page, and vice‑versa)
- Pages don’t throw errors (no blank page / 500)

**P1 (Nice to have)**
- Profile page loads
- Friendly error messages for invalid inputs


## 2) How to run for testing (no tools required)

1. Start the app:

```bash
python manage.py migrate
python manage.py runserver
```

2. Open in browser:
- Home: `http://localhost:8000/`
- Login: `http://localhost:8000/login/`
- Register: `http://localhost:8000/register/`
- Student dashboard: `http://localhost:8000/attendance/student/`
- Teacher dashboard: `http://localhost:8000/attendance/teacher/`

---

## 3) Test data (simple)

- Create **one student** account (Role = student)
- Create **one teacher** account (Role = teacher, set a Subject if needed by the app)

If a page requires login, test both:
- **Not logged in** (should redirect to login)
- **Logged in** (should allow access)

---

## 4) Manual test cases (easy table)

**Legend**
- **P0** = must pass for demo
- **P1** = nice-to-have

| ID | Test case | Steps | Expected result | Priority |
|----|----------|-------|-----------------|----------|
| TC-01 | Register (student) | Open `/register/` → fill form → choose role student → submit | Account created and user can log in | P0 |
| TC-02 | Register (teacher) | `/register/` → fill form → choose role teacher → submit | Account created and user can log in | P0 |
| TC-03 | Login success | Open `/login/` → enter valid credentials → submit | Login succeeds, user reaches home/dashboard | P0 |
| TC-04 | Login invalid password | `/login/` → valid username + wrong password | Error message, still on login page | P0 |
| TC-05 | Logout | Click logout button | Session ends; protected pages require login again | P0 |
| TC-06 | Protected page requires login | Open `/attendance/student/` while logged out | Redirect to login page | P0 |
| TC-07 | Student dashboard loads | Login as student → open `/attendance/student/` | Student dashboard loads (no error) | P0 |
| TC-08 | Teacher dashboard blocked for student | Login as student → open `/attendance/teacher/` | Access denied (403 / error JSON / message) | P0 |
| TC-09 | Mark attendance (student) | Login student → on student dashboard submit “mark attendance” | Success message; record created (pending verification) | P0 |
| TC-10 | Prevent duplicate mark (same day/subject) | Mark the same subject again on same day | App prevents duplicate or shows “already marked” | P1 |
| TC-11 | Teacher dashboard loads | Login teacher → open `/attendance/teacher/` | Teacher dashboard loads; pending records visible | P0 |
| TC-12 | Verify attendance (teacher) | Teacher dashboard → verify a pending record | Status becomes Verified; success response | P0 |
| TC-13 | Reject attendance (teacher) | Teacher dashboard → reject a pending record | Status becomes Rejected; success response | P0 |
| TC-14 | Student cannot verify/reject | Login student → try teacher verify/reject URL | Access denied (403 / message) | P0 |
| TC-15 | Profile page loads | Login → open `/profile/` | Profile page opens without error | P1 |

---
