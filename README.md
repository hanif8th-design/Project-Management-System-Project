# 🚀 Project Management System

A Django-based project management system designed to help users organize projects, manage tasks, and collaborate with team members efficiently.


## 📌 Overview

This application allows users to create and manage projects, assign tasks, and track progress in a structured way. It provides a collaborative environment with notifications and visual task tracking to improve productivity and organization.


## ✨ Features

### 🔐 Authentication

* User registration and login
* Secure logout functionality
* Password change and reset

### 👤 User Profiles

* Profile creation using Django signals
* Profile picture upload
* View user activity and details

### 📁 Projects

* Create, update, and delete projects
* Assign project ownership
* Track project progress and deadlines

### ✅ Tasks

* Create and manage tasks within projects
* Assign tasks to team members
* Set priorities, due dates, and statuses

### 👥 Team Collaboration

* Create and manage teams
* Assign users to projects
* Role-based permissions for actions

### 📊 Kanban Board

* Visual representation of tasks
* Organize tasks by status
* Drag-and-drop interaction (frontend supported)

### 💬 Comments

* Add comments to projects
* View discussions among team members
* Pagination for better performance

### 🔔 Notifications

* Real-time notifications for:

  * Task assignments
  * Project updates
  * Comments
* Mark notifications as read

### ⚙️ Background Tasks

* Celery for asynchronous processing
* Redis as message broker
* Scheduled alerts (Celery Beat) for deadlines and updates


## 🧠 Key Concepts Used

* Django Models & Relationships
* Class-Based Views (CBVs)
* Django Signals
* Custom Model Managers
* Authentication System
* AJAX (for dynamic updates)
* Celery & Redis (background tasks)
* Pagination & Query Optimization



## 🛠️ Tech Stack

* **Backend:** Django
* **Frontend:** HTML, CSS, JavaScript, AJAX
* **Task Queue:** Celery
* **Broker:** Redis
* **Database:** SQLite / PostgreSQL (configurable)


## 🎯 What I Learned

* Structuring large Django applications with multiple apps
* Managing complex relationships between models
* Implementing real-world features like task tracking and collaboration
* Using Celery and Redis for asynchronous tasks and scheduling
* Improving user experience with dynamic updates and notifications


## 🚧 Future Improvements

* Full frontend optimization for real-time interactions
* Role-based access control enhancements
* Deployment on cloud platforms
* API integration for mobile or external client

