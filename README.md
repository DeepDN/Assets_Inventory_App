# Inventory Management Application

## Description
This is a Flask-based inventory management application designed to handle various types of assets. It features a PostgreSQL database for data storage and Dockerization for simplified hosting and testing.

## Features
- User login system (Admin and User roles).
- Add, view, and delete assets across multiple categories.
- Unique asset ID generation based on company name, asset number, and type.
- User management (add and remove users).
- Simple, attractive UI with asset-related icons.

---

## Installation and Setup

### Prerequisites
- [Docker](https://www.docker.com/products/docker-desktop)
- Python 3.9+
- pip (Python package manager)

---

### Step 1: Set Up PostgreSQL with Docker

1. **Create a Docker Network**:
   ```bash
   docker network create inventory-net
   ```

2. **Run a PostgreSQL Container**:
   ```bash
   docker run --name inventory-postgres \
   --network=inventory-net \
   -e POSTGRES_USER=username \
   -e POSTGRES_PASSWORD=password \
   -e POSTGRES_DB=inventory_db \
   -p 5432:5432 \
   -d postgres
   ```
   Replace `username` and `password` with your preferred credentials.

3. **Verify PostgreSQL**:
   - Use a database client (e.g., pgAdmin) or CLI to connect to `localhost:5432` using the credentials provided.

---

### Step 2: Clone the Repository
Clone the project repository to your local machine:
```bash
git clone https://github.com/DeepDN/Assets_Inventory_App.git
cd Assets_Inventory_App
```

---

### Step 3: Configure the Flask Application

1. Open the Flask application code (e.g., `app.py`).
2. Update the PostgreSQL connection string in the configuration:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@inventory-postgres:5432/inventory_db'
   ```
   Replace `username` and `password` with your database credentials.

---

### Step 4: Install Python Dependencies
Install the required Python packages:
```bash
pip install flask flask-sqlalchemy psycopg2
```

---

### Step 5: Initialize the Database

Run the following Python script to create the necessary tables:
```bash
from app import db
db.create_all()
```

---

### Step 6: Dockerize the Flask Application

1. **Create a `Dockerfile`** (already included in the repository):
   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   COPY . /app

   RUN pip install --no-cache-dir flask flask-sqlalchemy psycopg2

   EXPOSE 5000

   CMD ["python", "app.py"]
   ```

2. **Build the Docker Image**:
   ```bash
   docker build -t inventory-app .
   ```

3. **Run the Flask App**:
   ```bash
   docker run --name inventory-app \
   --network=inventory-net \
   -p 5000:5000 \
   -d inventory-app
   ```

---

### Step 7: Access the Application

1. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```
2. Log in using the admin credentials. (Admin users must be manually added to the database during setup.)

---

### Step 8: Testing and Troubleshooting

- **Check Logs**:
   ```bash
   docker logs inventory-app
   docker logs inventory-postgres
   ```

- **Reset Containers**:
   ```bash
   docker stop inventory-postgres inventory-app
   docker rm inventory-postgres inventory-app
   docker network rm inventory-net
   ```

---

## Application Structure

```
project-directory/
|-- app.py                 # Main application code
|-- Dockerfile             # Dockerfile for containerizing the app
|-- requirements.txt       # Python dependencies
|-- templates/             # HTML templates
|   |-- login.html         # Login page template
|   |-- index.html         # Main dashboard template
|-- static/                # Static files (CSS, images, etc.)
```

---

## Future Enhancements
- Add support for asset image uploads.
- Integrate email notifications for asset allocation.
- Add more detailed reporting features.

---

## License
This project is licensed under the MIT License.

## Created be Deepak Nemade
