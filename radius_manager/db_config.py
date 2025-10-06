import os, json

CONFIG_FILE = 'db_config.json'

def get_db_settings():
    # If environment variables exist (Docker mode)
    env_host = os.environ.get("POSTGRES_HOST")
    env_db = os.environ.get("POSTGRES_DB")
    env_user = os.environ.get("POSTGRES_USER")
    env_pass = os.environ.get("POSTGRES_PASSWORD")
    env_port = os.environ.get("POSTGRES_PORT", "5432")

    if env_host and env_db and env_user and env_pass:
        print("Using PostgreSQL settings from environment variables.")
        return {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env_db,
            'USER': env_user,
            'PASSWORD': env_pass,
            'HOST': env_host,
            'PORT': env_port,
        }

    # Otherwise, check local JSON config file
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            print("Loaded PostgreSQL config from db_config.json")
            return json.load(f)

    # Finally, interactive setup for local dev
    print("=== PostgreSQL Connection Setup ===")
    host = input("Enter PostgreSQL host (default host.docker.internal): ") or "host.docker.internal"
    port = input("Port (default 5432): ") or "5432"
    name = input("Database name: ")
    user = input("User: ")
    password = input("Password: ")

    db_settings = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': name,
        'USER': user,
        'PASSWORD': password,
        'HOST': host,
        'PORT': port,
    }

    with open(CONFIG_FILE, 'w') as f:
        json.dump(db_settings, f)

    return db_settings
