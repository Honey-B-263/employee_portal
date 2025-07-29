<h1>🧑‍💼 Employee Management Portal</h1>

## 📌 Project Overview

The **Employee Management Portal** is a full-stack multi-user web application designed to simplify and centralize employee interactions in an organization. This portal provides different access levels for **Admins** and **Employees**.

- **Employees** can log in to:
  - Mark attendance through **AI-based facial recognition**.
  - Create and manage their personal **to-do lists**.
  - Use a **calendar** to track important events or deadlines.
  - View **announcements** made by admins.
  - Access their **personal and professional details** (e.g., phone number, address, attendance records, etc.)

- **Admins** can:
  - Add, update, or delete employee profiles.
  - Manage and view all employee data.
  - Broadcast announcements to all employees.
  
This system is aimed at enhancing employee productivity and improving administrative efficiency.

---

## ⚙️ Technology Stack

| Technology | Purpose |
|-----------|---------|
| **Python** | Backend logic and server-side scripting |
| **Flask** | Lightweight web framework for Python |
| **REST API** |	Used for communication between the frontend and backend (data exchange through HTTP methods)|
| **MySQL** | Relational database to store user and attendance data |
| **HTML/CSS** | Structuring and styling the frontend |
| **JavaScript** | Dynamic behavior and client-side logic |
| **Jinja2** | Templating engine for rendering HTML with dynamic data |
| **OpenCV + Deep Learning Model (dlib)** | Facial recognition for AI-based attendance system |



---

## 🧠 AI-Based Attendance System

The application integrates **facial recognition** using **OpenCV** and deep learning models like **dlib** for verifying employee identity. Once verified, attendance is marked automatically, ensuring a seamless and secure check-in experience.

---

## 🖥️ Features & Functionality

### 🔐 Login System
- Secure login page with role-based authentication.
- Admins and employees are redirected to their respective dashboards.
<img width="959" alt="image" src="https://github.com/Honey-B-263/employee_portal/assets/80630634/3b5710bc-dfca-4869-be39-55c31bb27bd2">
---
### 👩‍💼 Employee Dashboard
- **Face Recognition Attendance**: Employees can mark their attendance using their webcam.
- **To-Do List**: Create, update, and delete tasks for daily planning.
- **Calendar Integration**: Mark important events or reminders.
- **Announcements**: View messages and updates broadcasted by the admin.
- **Personal Details**: Access to work profile, contact information, and attendance history.
<img width="959" alt="image" src="https://github.com/Honey-B-263/employee_portal/assets/80630634/310f0eab-d9c6-48ee-9e1d-2cf696a6bd9e">
---

### 👨‍💼 Admin Dashboard
- **Employee Management**: Add new employees, edit existing profiles, or delete users.
- **Announcement Module**: Post announcements that instantly reflect across all employee dashboards.
- **Full Access Control**: View all employee information and attendance logs.
<img width="960" alt="image" src="https://github.com/Honey-B-263/employee_portal/assets/80630634/a7b2f8b0-2073-4c79-a435-7fc8263eafd8">
---








