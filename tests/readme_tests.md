# Running Tests

The project includes a comprehensive suite of automated tests.

### Prerequisites
Ensure you have the dependencies installed:
```bash
pip install -r requirements.txt
```

### Run All Tests
Execute the following command from the project root:
```bash
pytest tests/
```

The test suite uses **mocks** for all Google Cloud services, so no active GCP credentials or internet connection are required to run them.