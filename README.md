# Storage API Client

![CI](https://github.com/uriel-P-V/storage-api-client/actions/workflows/tests.yml/badge.svg)

A mock-based test suite for a storage management API client —
demonstrates advanced unittest.mock techniques for testing
HTTP clients without real API calls.

---

## Project Structure

```
storage-api-client/
├── client/
│   ├── __init__.py
│   └── storage_client.py        ← HTTP client for Storage API
├── tests/
│   ├── conftest.py              ← MagicMock fixtures
│   ├── test_client.py           ← Basic operation tests
│   └── test_client_advanced.py  ← side_effect, assert_called_once_with
├── .github/
│   └── workflows/
│       └── tests.yml            ← GitHub Actions CI
├── pytest.ini
└── requirements.txt
```

---

## Features

- **Full mock isolation** — 11 tests, zero real HTTP calls
- **MagicMock fixtures** — reusable fake responses
- **side_effect** — simulates Timeout and ConnectionError
- **assert_called_once_with** — verifies correct API call parameters
- **GitHub Actions CI** — runs on every push with coverage reporting

---

## Mock Techniques Demonstrated

```python
# Fake response factory
response = MagicMock()
response.json.return_value = {"id": "vol-001"}

# Simulate exceptions
mock_session.get.side_effect = Timeout()

# Verify call parameters
mock_session.post.assert_called_once_with(
    "https://api.com/volumes",
    json={"name": "test", "size_gb": 50},
    timeout=10
)
```

---

## Setup

```bash
git clone https://github.com/uriel-P-V/storage-api-client.git
cd storage-api-client
pip install -r requirements.txt
pytest tests/ -v
```

---

## Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=client --cov-report=term-missing
```

---

## Tech Stack

- **Python 3.10+**
- **unittest.mock** — MagicMock, patch, side_effect
- **Pytest** — test framework with fixtures
- **GitHub Actions** — CI/CD pipeline

---

## Author

**Uriel Alejandro Pérez Valdovinos**  
[github.com/uriel-P-V](https://github.com/uriel-P-V) · [linkedin.com/in/uriel-pv](https://linkedin.com/in/uriel-pv)