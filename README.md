# 🛰️ Radius Monitoring System, radius and postgress setup

A Django project for managing RADIUS users in the gildesecops database and setting up radius server.

---
**Author**: Abdul G Zziwa
## 🚀 Prerequisites

Before you begin, make sure the following are installed on your system:

| Tool | Description | Download |
|------|--------------|-----------|
| **Python** | | |
| **Docker** | Required to build and run the Django application in a container | [https://www.docker.com/](https://www.docker.com/) |
| **Git** | To clone the repository | [https://git-scm.com/downloads](https://git-scm.com/downloads) |




## Setup Instructions

### 1. Clone and Navigate
```bash
sudo git clone https://github.com/abduzziwa/.kom_automatiseren_wifi.git
cd .kom_automatiseren_wifi/
```

### 2. Run Setup Script
```bash
cd documenten/
sudo python3 setup_radius.py
cd ..
```

### 3. Configure Docker
```bash
sudo nano docker-compose.yml
```
Update environment variables:
```yaml
environment:
  - POSTGRES_HOST=host.docker.internal
  - POSTGRES_DB=gildesecops
  - POSTGRES_USER=radiususer
  - POSTGRES_PASSWORD=radiuspassword
```

### 4. Configure PostgreSQL
```bash
sudo nano /etc/postgresql/<version>/main/postgresql.conf
```
Set:
```
listen_addresses = '*'
```
Restart PostgreSQL:
```bash
sudo systemctl restart postgresql
```

⚠️ Troubleshooting PostgreSQL Errors  
If you encounter errors with PostgreSQL connections, you may need to update the host settings in another PostgreSQL configuration file. Open the file with:

```bash
sudo nano /etc/postgresql/<version>/main/pg_hba.conf
--host    all    all    0.0.0.0/0    md5

### 5. Start Application
```bash
sudo docker compose up
```

### 6. Initialize Django (New Terminal)
```bash
docker exec -it radius_manager-web-1 bash
python manage.py migrate
python manage.py createsuperuser
```

## Testing (Optional)
Create a user in the Django admin, then test:
```bash
radtest testuser testpass 127.0.0.1 0 SuperSecretKey123
```

**Done! 👍**
