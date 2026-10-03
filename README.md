# Face Recognition Attendance System

A full-stack attendance management system that uses face recognition to record student attendance.

The project provides an admin interface for managing batches and students, along with a student attendance interface that uses webcam-based face recognition.

## Screenshots

<!-- Add screenshots here -->

### Home Page


### Admin Dashboard


### Student Enrollment


### Attendance


### Student Management


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