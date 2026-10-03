# Face Recognition Attendance System

A full-stack attendance management system that uses face recognition to record student attendance.

The project provides an admin interface for managing batches and students, along with a student attendance interface that uses webcam-based face recognition.

## Screenshots

<!-- Add screenshots here -->

### Home Page
<img width="1868" height="959" alt="Screenshot From 2026-10-03 12-40-42" src="https://github.com/user-attachments/assets/66ec518b-bdee-47e6-a0d6-9b8383e2d194" />

### Admin Dashboard
<img width="1868" height="959" alt="Screenshot From 2026-10-03 12-41-11" src="https://github.com/user-attachments/assets/84310c22-89d0-430d-bcfe-eb131f6bcd32" />

### Student Management
<img width="1868" height="959" alt="Screenshot From 2026-10-03 12-42-07" src="https://github.com/user-attachments/assets/21586c67-3487-46fa-b696-551b09ab8f7e" />
<img width="1868" height="959" alt="Screenshot From 2026-10-03 12-42-13" src="https://github.com/user-attachments/assets/afb421a2-f1f9-4d6d-8d44-6c8c0a732b36" />

---

## Features

### Admin

- Admin login and authentication
- Create and remove batches
- Add students to batches
- Remove students from batches
- Enroll student face embeddings using a webcam
- Manage student records

### Attendance

- Webcam-based face recognition
- Face embedding generation using InsightFace
- Match registered students using their face embeddings
- Automatically record attendance
- Prevent attendance from being manually entered by students

### Frontend

- HTML, CSS and JavaScript
- Dynamic UI updates using JavaScript
- REST API communication using `fetch()`
- Webcam access through the browser
- Responsive form and management interfaces

---

## How To use

- Download required packages from requirements.txt
- For CLI 
- python source/main.py
- For WebSite 
- start uvicorn server using 
- uvicorn source/app:app --reload --host 0.0.0.0 --port 8004
- then open main_menu.html on your browser


## Tech Stack

### Backend

- Python
- FastAPI
- SQLite
- NumPy
- InsightFace
- ArcFace

### Frontend

- HTML
- CSS
- JavaScript

---

## How It Works

The application is divided into a frontend and backend.

```text
                    Browser
                       |
                HTML / CSS / JS
                       |
                  HTTP / JSON
                       |
                       v
                  FastAPI API
                       |
          +------------+------------+
          |            |            |
          v            v            v
       SQLite      InsightFace    NumPy
          |            |            |
          |       Face Embeddings   |
          |            |            |
          +------------+------------+
                       |
                       v
                  Attendance
