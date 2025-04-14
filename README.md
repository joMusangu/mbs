# 🎟️ Movie Booking System (MBS)

The **Movie Booking System (MBS)** is a user-friendly, web-based platform that lets customers browse and book tickets for movies currently playing. With a simple interface for users and a powerful admin panel, MBS makes movie selection and ticket booking a breeze.

---

## 🚀 Features

- 🎬 **Browse Movies** – Discover movies by genre, language, or availability  
- 🗓️ **View Showtimes** – Easily access up-to-date movie schedules  
- 💳 **Secure Online Booking** – Book tickets and make payments securely  
- 🎟️ **Ticket Confirmation** – Receive email confirmations with your ticket details  
- 🛠️ **Admin Dashboard** – Manage movie listings, schedules, and bookings efficiently  
- 📊 **Reporting Tools** – Analyze sales and occupancy data  

---

## 🛠️ Running the Backend

### 📋 Prerequisites

- Python 3.x installed  

---

### ⚙️ Setup Instructions

#### 1. Clone the Repository

```bash
git clone https://github.com/joMusangu/mbs.git
```

#### 2. Navigate to the Backend Folder
```bash
cd mbs_backend
```
#### 3. Install Dependencies
If Django is giving you errors after cloning, install the necessary packages:
```bash
pip install django
pip install django djangorestframework
```
#### 4. Run Migrations on the Shared DB:
After setting up the shared database, run the migrations to synchronize the database schema:

```bash
python manage.py makemigrations
python manage.py migrate
```
#### 5.Run the Server
Start the server:

```bash
python manage.py runserver
```
## 🔌 API Testing

### Endpoint Overview

| Endpoint       | Method | Description                          |
|----------------|--------|--------------------------------------|
| `/api/users/`  | `GET`  | Retrieves a list of all users        |

---

### ➕ Create a New User

- **URL:** `/api/users/create/`  
- **Method:** `POST`  
- **Description:** Creates a new user with the provided data  

#### Body (JSON example):

```json
{
  "username": "joseph",
  "email": "joseph@example.com",
  "password": "securepassword123"
}
```
### 🔍 Get, Update, or Delete a User by ID

- **URL Pattern:** `/api/users/<int:pk>/`

#### Methods & Descriptions:

| Method  | Description                                          |
|---------|------------------------------------------------------|
| `GET`   | Retrieves the details of a specific user by their ID |
| `PUT`   | Updates the details of a specific user by their ID  |
| `DELETE`| Deletes a specific user by their ID                 |

