# FastAPI Assignment

This repository contains an assignment/project built using [FastAPI](https://fastapi.tiangolo.com/), a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

## Features

- **FastAPI**: Leverages the speed and efficiency of FastAPI to create robust APIs.
- **MongoDB**: Utilizes MongoDB as the database for data storage and retrieval.
- **Modular Structure**: Organized into a clean and maintainable folder structure.

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
   DATABASE_URL=mongodb://<username>:<password>@localhost:27017/<database_name>
   SECRET_KEY=your_secret_key_here
   ```

## Folder Structure

```plaintext
fastapi_assign/
|-- main.py         # Entry point of the application
|-- config.py       # Configuration settings
|-- database.py     # Database connection setup
|-- .env            # Environment variables
|-- requirements.txt # Project dependencies
|-- users/          # User-related functionality
|   |-- routers/    # API endpoints
|   |-- models/     # Data models
|   |-- utils/      # Helper functions
|-- orders/         # Order-related functionality
|   |-- routers/    # API endpoints
|   |-- models/     # Data models
|   |-- utils/      # Helper functions
|-- admin/          # Admin-related functionality
    |-- routers/    # API endpoints
    |-- models/     # Data models
    |-- utils/      # Helper functions
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

## Testing

To run tests (if available), use:
```bash
pytest
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork this repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push them to your fork.
4. Submit a pull request with a detailed description of your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or feedback, please reach out to the repository owner or create an issue in this repository.

