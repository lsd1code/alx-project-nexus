# E-Commerce Backend API

A robust, scalable, and performant backend system for an e-commerce product catalog, built with Django and PostgreSQL. This project simulates a real-world development environment, emphasizing API design, database optimization, and secure authentication.

## 🚀 Overview

This project is the backend engine for a modern e-commerce platform. It provides all the necessary APIs to manage products, categories, and users, featuring advanced querying capabilities like filtering, sorting, and pagination. It's designed to be a foundation for frontend applications (web or mobile) to build upon.

## 🎯 Project Goals

*   **CRUD APIs:** Build complete Create, Read, Update, and Delete operations for products, categories, and user management.
*   **Advanced Querying:** Implement robust logic for filtering, sorting, and pagination to enable efficient product discovery.
*   **Database Optimization:** Design a high-performance, normalized relational database schema with proper indexing to ensure seamless and fast query execution.
*   **Security & Documentation:** Integrate secure user authentication and provide comprehensive, interactive API documentation.

## 🛠️ Technologies Used

*   **Framework:** ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
*   **Database:** ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
*   **Authentication:** ![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)
*   **API Documentation:** ![Swagger](https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=Swagger&logoColor=black)

## ✨ Key Features

### 1. CRUD Operations
- Full management of products (Create, List, Detail, Update, Delete).
- Full management of product categories.
- User registration, login, and profile management.
- Secure authentication using JSON Web Tokens (JWT).

### 2. Advanced API Features
- **Filtering:** Filter products by fields such as `category`, `price` range, and `availability`.
- **Sorting:** Sort product lists by attributes like `price`, `name`, and `date_created`.
- **Pagination:** Efficiently handle large datasets with page-based pagination for improved performance and UX.

### 3. Comprehensive API Documentation
- Interactive API documentation automatically generated with **Swagger / OpenAPI**.
- Hosted and easily accessible endpoint for frontend developers to explore and test all API functionality.

## 📦 Installation & Setup

Follow these steps to get the project running on your local machine.

1.  **Clone the repository**
    ```bash
    git clone https://github.com/lsd1code/alx_project_nexus.git
    cd alx_project_nexus
    ```

2.  **Create a Virtual Environment and Activate it**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Environment Variables**
    Create a `.env` file in the project root based on the `.env.example` file and configure your settings:
    ```bash
    # .env
    DEBUG=True
    SECRET_KEY=your-django-secret-key
    DB_NAME=your-database-name
    DB_USER=your-database-user
    DB_PASSWORD=your-database-password
    DB_HOST=localhost
    DB_PORT=5432
    ```

5.  **Run Database Migrations**
    ```bash
    python manage.py migrate
    ```

6.  **Create a Superuser (Optional)**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the Development Server**
    ```bash
    python manage.py runserver
    ```
    The API will be available at `http://localhost:8000`.

## 📚 API Documentation

Once the server is running, access the interactive API documentation:
- **Swagger UI:** `http://localhost:8000/swagger/`
- **ReDoc:** `http://localhost:8000/redoc/`

This documentation provides a complete overview of all available endpoints, required parameters, and allows you to make live API calls directly from the browser.

## 🔐 Authentication

This API uses JWT (JSON Web Tokens) for authentication.

1.  **Register** a new user at `/api/auth/register/`.
2.  **Login** with credentials at `/api/auth/login/` to receive your access and refresh tokens.
3.  **Use the Access Token** to authenticate subsequent requests by adding it to the header of your HTTP requests:
    ```
    Authorization: Bearer <access_token>
    ```

## 🗃️ Example API Endpoints

| Method | Endpoint | Description | Authentication |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/products/` | Get a paginated list of products (supports filtering & sorting) | Optional |
| `POST` | `/api/products/` | Create a new product | Required (Admin) |
| `GET` | `/api/products/{id}/` | Get details of a specific product | Optional |
| `POST` | `/api/auth/login/` | User login | No |
| `GET` | `/api/users/profile/` | Get current user profile | Required |

## 📝 License

This project is for educational and portfolio purposes.
