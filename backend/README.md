# SmartSense Inbox Backend

## Overview
SmartSense Inbox is an intelligent SMS summarizer that provides users with a concise overview of their SMS messages. The backend is built using FastAPI, which allows for fast and efficient handling of API requests.

## Project Structure
The backend is organized into several key directories and files:

- **app**: Contains the main application code.
  - **main.py**: Entry point for the FastAPI application.
  - **api**: Contains the API endpoints.
    - **v1**: Version 1 of the API.
      - **endpoints**: Contains specific API endpoint definitions.
        - **sms.py**: API endpoints for managing SMS messages.
        - **summary.py**: API endpoints for summarizing SMS messages.
      - **deps.py**: Dependency injection functions.
  - **core**: Contains core configuration and logging settings.
    - **config.py**: Configuration settings for the application.
    - **logging.py**: Logging setup for the application.
  - **services**: Contains business logic for SMS handling and summarization.
    - **sms_client.py**: Logic for interacting with the SMS inbox.
    - **summarizer.py**: Logic for summarizing SMS messages.
  - **models**: Data models for SMS messages.
    - **sms_model.py**: Defines the structure of SMS data.
  - **schemas**: Pydantic schemas for data validation.
    - **sms.py**: Defines schemas for SMS data.
  - **tests**: Contains unit tests for the application.
    - **test_summary.py**: Tests for the summarization functionality.

## Installation
To set up the backend, ensure you have Python 3.7 or higher installed. Then, install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application
To run the FastAPI application, execute the following command:

```bash
uvicorn app.main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

## API Documentation
The API documentation can be accessed at `http://127.0.0.1:8000/docs` once the application is running.

## Testing
To run the tests, use the following command:

```bash
pytest
```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.