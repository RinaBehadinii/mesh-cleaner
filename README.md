# Mesh Cleaner System

A full-stack application for uploading, processing, and downloading 3D mesh files.

- **Frontend:** React (`mesh-cleaner-fe`)
- **Backend:** FastAPI (`mesh-cleaner-service`)
- **Database:** PostgreSQL
- **Containerized:** Docker Compose

---

## Features

- **Upload Mesh:** Upload and process 3D mesh files for cleaning and optimization.
- **View Individual Logs:** See detailed logs for each mesh after processing via the `/clean-mesh` response.
- **View All Logs:** See processing history and summary stats for all processed meshes.
- **Download Mesh:** Download the processed mesh files.

---

### API Endpoints

- `POST /clean-mesh`
- `GET /logs`
- `GET /download-mesh/{filename}`

---

## Running the Project with Docker Compose

**Requirements:**

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

**Steps:**

1. **Clone the repository:**
    ```sh
    git clone <your-repo-url>
    cd <project-root>
    ```

2. **Build and start all services:**
    ```sh
    docker-compose up --build
    ```

3. **Access the applications:**
    - Frontend: [http://localhost:3000](http://localhost:3000)
    - Backend API & docs: [http://localhost:8000/docs](http://localhost:8000/docs)

4. **Stopping & Cleaning Up:**
    ```sh
    docker-compose down -v
    ```


