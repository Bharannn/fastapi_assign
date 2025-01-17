# FastAPI Assignment

This repository contains an assignment/project built using [FastAPI](https://fastapi.tiangolo.com/), a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

## Features

- **FastAPI**: Leverages the speed and efficiency of FastAPI to create robust APIs.
- **MongoDB**: Utilizes MongoDB as the database for data storage and retrieval.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.9 or above
- MongoDB
- pip (Python package manager)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Bharannn/fastapi_assign.git
   cd fastapi_assign
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the environment variables**:
   Create a `.env` file in the root directory and add the following:
   ```env
   DATABASE_URL=
   MONGO_INITDB_DATABASE=
   
   ACCESS_TOKEN_EXPIRES_IN=
   REFRESH_TOKEN_EXPIRES_IN=
   JWT_ALGORITHM=
   
   CLIENT_ORIGIN=
   
   EMAIL_HOST=
   EMAIL_PORT=
   EMAIL_USERNAME=
   EMAIL_PASSWORD=
   EMAIL_FROM=
   EMAIL_FROM_NAME=
   JWT_PRIVATE_KEY=
   JWT_PUBLIC_KEY=
   
   ADMIN_KEY=
   USER_KEY=
   GUEST_KEY=
   ```

## Running the Application

1. **Start the MongoDB server**:
   Ensure your MongoDB instance is running locally or on the specified server in your `.env` file.

2. **Run the FastAPI server**:
   ```bash
   uvicorn main:app --reload
   ```

3. **Access the API documentation**:
   - Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the interactive Swagger UI.
   - Alternatively, visit [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) for ReDoc documentation.

