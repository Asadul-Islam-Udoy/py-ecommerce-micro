# 🛒 Scalable Microservices E-Commerce Platform

A production-ready microservices-based eCommerce system built with Django, Next.js, PostgreSQL, Docker, and Nginx.  
This project demonstrates enterprise-level architecture, including API Gateway, payment integration, and scalable service design.

---

## 🚀 Features

- Microservices-based architecture  
- JWT Authentication & Role-Based Access Control  
- Cart & Order Management
- Redis for caching & performance
- RabbitMQ for asynchronous communication
- Stripe & PayPal Payment Integration  
- Webhook-based Payment Verification  
- Modern frontend with Next.js
- PostgreSQL database per service
- Nginx reverse proxy for routing
- Dockerized environment for easy setup
- Fully Dockerized Environment  
- Scalable & Fault-tolerant Design  

---

---

## 🧩 Microservices

- **Auth Service** → Authentication & JWT  
- **User Service** → User profile & address  
- **Product Service** → Products & categories  
- **Order Service** → Cart & order lifecycle  
- **Payment Service** → Stripe & PayPal integration  
- **API Gateway** → Central routing & security  

---

## 🛠️ Tech Stack

- Frontend: Next.js  
- Backend: Django REST Framework  
- Database: PostgreSQL  
- Proxy: Nginx  
- Messaging: RabbitMQ (optional)  
- Cache: Redis  
- DevOps: Docker, Docker Compose  

---

## 📁 Project Structure

---

## 🚀 Getting Started

### 📋 Prerequisites

- Docker
- Docker Compose
- Git

---

### 📥 Clone Repository

```bash
git clone https://github.com/your-username/ecommerce-microservices.git
cd ecommerce-microservices
### ⚙️ Setup Environment Variables
cp  .env


### 🐳 Run Project
docker compose up --build -d

### 🌐 Access Application
| Service     | URL                                              |
| ----------- | ------------------------------------------------ |
| Frontend    | [http://localhost](http://localhost)             |
| API         | [http://localhost/api](http://localhost/api)     |
| Admin Panel | [http://localhost/admin](http://localhost/admin) |


### 🗄️ PostgreSQL Usage
Each microservice has its own database

### 🔄 Payment Flow
User places order
Order service creates PENDING order
Payment service generates payment URL
User completes payment
Webhook updates payment status
Order marked as PAID

### 🔐 Authentication
JWT-based authentication
Token required for protected routes
Ensures isolation and scalability
Managed via Docker containers

### 🚀 Production Notes
Use Gunicorn with Django
Configure HTTPS with Nginx
Use managed PostgreSQL (AWS RDS)
Enable caching (Redis)
