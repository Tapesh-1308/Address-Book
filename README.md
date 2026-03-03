# Address Book API

Minimal FastAPI application for managing addresses with geospatial search.

## Features

* Create address
* Update address
* Delete address
* Retrieve addresses within a given distance
* SQLite database
* ORM (SQLAlchemy)
* Input validation
* Structured logging
* Externalized configuration

---

## Tech Stack

* FastAPI
* SQLAlchemy
* SQLite
* Geopy

---

## Setup (Under 5 Minutes)

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd address_book
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

(Windows: `venv\Scripts\activate`)

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
uvicorn app.main:app --reload
```

---

## API Documentation

Open in browser:

```
http://127.0.0.1:8000/docs
```

Swagger UI is enabled by default.

---

## Environment Variables

Create a `.env` file in project root:

```
DATABASE_URL=sqlite:///./address.db
LOG_LEVEL=INFO
```

---

## Notes

* Coordinates are validated:
  * Latitude: -90 to 90
  * Longitude: -180 to 180
* Nearby search uses geodesic distance via `geopy`.
* Suitable for small to moderate datasets (SQLite limitation).

---
