# 🛰️ Radius Monitoring System

A Django-based monitoring system for managing and tracking Radius server data.

---

## 🚀 Prerequisites

Before you begin, make sure the following are installed on your system:

| Tool | Description | Download |
|------|--------------|-----------|
| **Docker** | Required to build and run the Django application in a container | [https://www.docker.com/](https://www.docker.com/) |
| **PostgreSQL** | The application database | [https://www.postgresql.org/download/](https://www.postgresql.org/download/) |
| **Git** | To clone the repository | [https://git-scm.com/downloads](https://git-scm.com/downloads) |

> 💡 **Note for Linux users:**  
> Ensure your user is added to the `docker` group to avoid using `sudo` for every Docker command.  
> ```bash
> sudo usermod -aG docker $USER
> newgrp docker
> ```

---

## 🧩 Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/RadiusMonitoringSystem.git
cd RadiusMonitoringSystem/radius_manager
````

---

### 2️⃣ Prepare the PostgreSQL Database

#### 🪶 Option A — Using an existing PostgreSQL server

1. Start PostgreSQL service:

   * **Windows:** Start via pgAdmin or the Windows Services panel.
   * **Linux:**

     ```bash
     sudo systemctl start postgresql
     ```

2. Connect to PostgreSQL:

   ```bash
   psql -U postgres
   ```

3. Create a database and user:

   ```sql
   CREATE DATABASE gildeSecOps;
   CREATE USER postgres WITH PASSWORD 'Root';
   GRANT ALL PRIVILEGES ON DATABASE gildeSecOps TO postgres;
   \q
   ```

4. Load your **Radius server SQL dump file**:

   ```bash
   psql -U postgres -d gildeSecOps -f /path/to/radius_dump.sql
   ```

> Make sure the dump file is properly imported before running the Docker container.

---

### 3️⃣ Update Environment Variables

Edit the `docker-compose.yml` file to match your PostgreSQL setup:

```yaml
environment:
  - POSTGRES_HOST=host.docker.internal     # Linux users: use 'localhost' or container hostname
  - POSTGRES_DB=gildeSecOps
  - POSTGRES_USER=postgres
  - POSTGRES_PASSWORD=Root
```

> 🧠 **Tip for Linux users:**
> If you’re running PostgreSQL inside another container or VM, update `POSTGRES_HOST` accordingly (e.g. to a container name or IP).

---

### 4️⃣ Build and Run the Application

Run this command inside the `radius_manager` directory:

```bash
docker-compose up --build
```

Docker will:

* Build the Python/Django container using the provided `Dockerfile`
* Install dependencies from `requirements.txt`
* Launch the Django development server at port **8000**

---

### 5️⃣ Access the Application

After the container starts successfully, open:

🌐 [http://localhost:8000](http://localhost:8000)

---

## 🔐 Default Superuser

By default, the system may include a Django superuser account:

```
Username: admin
Password: admin
```

If that account does not exist, create one manually inside the running container:

```bash
docker exec -it <container_name> python manage.py createsuperuser
```

Follow the prompts to set up your admin user.

---

## 🧰 Common Docker Commands

| Command                                 | Description                                 |
| --------------------------------------- | ------------------------------------------- |
| `docker-compose up --build`             | Build and start the container               |
| `docker-compose down`                   | Stop and remove containers                  |
| `docker ps`                             | List running containers                     |
| `docker exec -it <container_name> bash` | Access a shell inside the running container |
| `docker logs <container_name>`          | View application logs                       |
| `docker system prune -f`                | Clean up unused Docker resources            |

---

## 🧱 Project Structure

```
RadiusMonitoringSystem/
│
├── radius_manager/
│   ├── radapp/                   # Main Django application
│   ├── radius_manager/           # Django project settings and URLs
│   ├── Dockerfile                # Docker build configuration
│   ├── docker-compose.yml        # Service definition
│   ├── manage.py                 # Django management entry point
│   └── requirements.txt          # Python dependencies
│
└── README.md
```

---

## 🪪 License

This project is proprietary to Abdul G Zziwa and his team.
Please contact the me before redistribution or modification.

---

**Happy deploying! 🧑‍💻**
