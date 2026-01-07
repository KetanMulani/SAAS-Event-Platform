
# 🏢 Saas Event Platform (Multi-Tenant)

A RESTful backend API built with **FastAPI** for managing events with secure user authentication and role-based access control.  
This project demonstrates real-world backend development practices including JWT authentication, database modeling, and clean project structure.

---

## 📌 Features

- User registration and login
- Secure password hashing using bcrypt
- JWT-based authentication
- Role-based authorization (admin & normal users)
- Create and view events
- Admin-only event deletion
- Clean and modular project structure
- Interactive API documentation using Swagger UI

---

## 🛠️ Tech Stack

- **Backend Framework:** FastAPI
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Authentication:** JWT (python-jose)
- **Password Hashing:** Passlib (bcrypt)
- **Server:** Uvicorn
- **Validation:** Pydantic

---

## 📁 Project Structure

```

.
├── main.py           # Application entry point
├── models.py         # SQLAlchemy database models
├── schemas.py        # Pydantic schemas for validation
├── database.py       # Database connection & session management
├── security.py       # Authentication, JWT, password hashing
├── requirements.txt  # Project dependencies
├── README.md         # Project documentation
└── test.db           # SQLite database (optional, local use)

````

---

## ⚙️ Installation & Setup

Follow these steps to run the project locally:

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/event-management-api.git
cd event-management-api
````

### 2️⃣ Create and activate virtual environment

```bash
python -m venv venv
```

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the server

```bash
uvicorn main:app --reload
```

Server will start at:

```
http://127.0.0.1:8000
```

---

## 📖 API Documentation

FastAPI provides built-in interactive API docs:

* **Swagger UI:**

  ```
  http://127.0.0.1:8000/docs
  ```

* **ReDoc:**

  ```
  http://127.0.0.1:8000/redoc
  ```

---

## 🔐 Authentication Flow

1. User registers using `/register`
2. User logs in using `/login`
3. On successful login, a **JWT access token** is generated
4. Token must be passed in request headers as:

```
Authorization: Bearer <your_access_token>
```

5. Protected routes verify the token and fetch the current user

---

## 📡 API Endpoints

| Method | Endpoint                           | Description              | Access        |
| ------ | --------------------               | ------------------------ | ------------- |
| POST   | `/register`                        | Register a new user      | Public        |
| POST   | `/login`                           | Login and get JWT token  | Public        |
| GET    | `/me`                              | Get current user details | Authenticated |
| GET    | `/events`                          | Get all events           | Public        |
| PUT    | `/update-event/{event_id}`         | Update a event           | Admin only
| POST   | `/create-event`                    | Create a new event       | Admin only |
| DELETE | `/delete-event/{id}`               | Delete event             | Admin only    |
| POST   | `/register-event/{event_id}`       | register for a event     | Public        |
| POST   | `/events/{event_id}/announcements` | create a announcement for| Admin only    |
|        |                                    | a specific event         |               |
| GET    | `/events/{event_id}/announcements` | Get announcement of a    | Public        |
|        |                                    |  specific event          |               |

---

## 🧪 Database

* Uses **SQLite** for simplicity
* SQLAlchemy ORM for database operations
* Tables are automatically created on app startup

---

## 🚧 Future Improvements

* Input validation enhancements
* Pagination for event listing
* Ticket booking system
* Dockerization
* PostgreSQL integration
* Role-based permissions per event
* Logging & monitoring

---

## 👨‍💻 Author

**Ketan Mulani**
Backend Developer | Computer Science Student

---

## ⭐ Why This Project?

This project was built to:

* Learn real-world backend architecture
* Understand authentication & authorization deeply
* Practice clean FastAPI project structuring
* Prepare for internships and backend interviews