#!/usr/bin/env python3
"""
Complete PostgreSQL + FreeRADIUS Setup Script
Fully automated setup - just run with sudo and configure your AP IPs afterward
"""
import subprocess
import sys
import os
from datetime import datetime

# Configuration
DB_NAME = "gildesecops"
DB_USER = "radiususer"
DB_PASS = "radiuspassword"
RADIUS_SECRET = "SuperSecretKey123"  # Change this to your preferred secret
TEST_USERNAME = "testuser"
TEST_PASSWORD = "testpass"

# -------------------------------------------------------------------
# Utility Functions
# -------------------------------------------------------------------
def print_header(text):
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")

def run_command(cmd, description, ignore_errors=False):
    """Execute shell command and return result"""
    print(f"🔹 {description}")
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    
    if result.returncode == 0:
        print("   ✅ Success")
        if result.stdout.strip():
            print(f"   Output: {result.stdout.strip()[:200]}")
    else:
        if ignore_errors:
            print(f"   ⚠️  Warning: {result.stderr.strip()[:200]}")
        else:
            print(f"   ❌ Failed: {result.stderr.strip()}")
            if not ignore_errors:
                print(f"\n🛑 Setup failed at: {description}")
                sys.exit(1)
    
    return result

def check_root():
    """Ensure script is run with sudo"""
    if os.geteuid() != 0:
        print("❌ This script must be run with sudo privileges!")
        print("   Please run: sudo python3 setup_radius.py")
        sys.exit(1)

# -------------------------------------------------------------------
# PostgreSQL Setup
# -------------------------------------------------------------------
def install_postgresql():
    print_header("STEP 1: Installing PostgreSQL")
    
    run_command("apt update -y", "Updating package lists")
    run_command("apt install -y postgresql postgresql-contrib", "Installing PostgreSQL")
    run_command("systemctl enable postgresql", "Enabling PostgreSQL on boot")
    run_command("systemctl start postgresql", "Starting PostgreSQL service")
    run_command("systemctl status postgresql --no-pager", "Verifying PostgreSQL is running", ignore_errors=True)

def setup_database():
    print_header("STEP 2: Creating Database and User")
    
    # Create database
    run_command(
        f'sudo -u postgres psql -c "DROP DATABASE IF EXISTS {DB_NAME};"',
        f"Dropping existing {DB_NAME} database (if exists)",
        ignore_errors=True
    )
    run_command(
        f'sudo -u postgres psql -c "CREATE DATABASE {DB_NAME};"',
        f"Creating database: {DB_NAME}"
    )
    
    # Create user
    run_command(
        f'sudo -u postgres psql -c "DROP USER IF EXISTS {DB_USER};"',
        f"Dropping existing user {DB_USER} (if exists)",
        ignore_errors=True
    )
    run_command(
        f'sudo -u postgres psql -c "CREATE USER {DB_USER} WITH PASSWORD \'{DB_PASS}\';"',
        f"Creating user: {DB_USER}"
    )
    
    # Grant privileges
    run_command(
        f'sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO {DB_USER};"',
        f"Granting privileges to {DB_USER}"
    )
    run_command(
        f'sudo -u postgres psql -d {DB_NAME} -c "GRANT ALL ON SCHEMA public TO {DB_USER};"',
        "Granting schema privileges"
    )

def configure_pg_authentication():
    print_header("STEP 3: Configuring PostgreSQL Authentication")
    
    # Find pg_hba.conf file
    result = run_command(
        "sudo -u postgres psql -t -P format=unaligned -c 'SHOW hba_file;'",
        "Finding pg_hba.conf location"
    )
    hba_file = result.stdout.strip()
    
    print(f"   📄 Using config file: {hba_file}")
    
    # Backup original
    run_command(
        f"cp {hba_file} {hba_file}.backup",
        "Backing up pg_hba.conf"
    )
    
    # Add authentication rule for radiususer (insert at line 2, after first comment block)
    auth_line = f"local   {DB_NAME}   {DB_USER}   md5"
    run_command(
        f"sed -i '/^# TYPE/a {auth_line}' {hba_file}",
        f"Adding authentication rule for {DB_USER}"
    )
    
    # Reload PostgreSQL configuration
    run_command("systemctl reload postgresql", "Reloading PostgreSQL configuration")

# -------------------------------------------------------------------
# FreeRADIUS Setup
# -------------------------------------------------------------------
def install_freeradius():
    print_header("STEP 4: Installing FreeRADIUS")
    
    run_command("apt install -y freeradius freeradius-postgresql", "Installing FreeRADIUS with PostgreSQL support")
    run_command("systemctl stop freeradius", "Stopping FreeRADIUS (for configuration)", ignore_errors=True)

def import_radius_schema():
    print_header("STEP 5: Importing FreeRADIUS Schema")
    
    # Find schema file
    schema_paths = [
        "/etc/freeradius/3.0/mods-config/sql/main/postgresql/schema.sql",
        "/etc/freeradius/3.2/mods-config/sql/main/postgresql/schema.sql"
    ]
    
    schema_file = None
    for path in schema_paths:
        if os.path.exists(path):
            schema_file = path
            break
    
    if not schema_file:
        print("❌ Could not find FreeRADIUS PostgreSQL schema file!")
        sys.exit(1)
    
    print(f"   📄 Using schema: {schema_file}")
    
    # Import schema
    run_command(
        f"PGPASSWORD={DB_PASS} psql -h localhost -U {DB_USER} -d {DB_NAME} -f {schema_file}",
        "Loading FreeRADIUS schema into database"
    )
    
    print("   ✅ Database schema loaded successfully")

def configure_freeradius_sql():
    print_header("STEP 6: Configuring FreeRADIUS SQL Module")
    
    # Find FreeRADIUS config directory
    config_dirs = ["/etc/freeradius/3.0", "/etc/freeradius/3.2"]
    config_dir = None
    for d in config_dirs:
        if os.path.exists(d):
            config_dir = d
            break
    
    if not config_dir:
        print("❌ Could not find FreeRADIUS configuration directory!")
        sys.exit(1)
    
    print(f"   📁 Using config directory: {config_dir}")
    
    sql_file = f"{config_dir}/mods-available/sql"
    
    # Backup original SQL config
    run_command(f"cp {sql_file} {sql_file}.backup", "Backing up SQL module config")
    
    # Configure SQL module
    replacements = [
        ('driver = "rlm_sql_null"', 'driver = "rlm_sql_postgresql"'),
        ('dialect = "sqlite"', 'dialect = "postgresql"'),
        ('#\tserver = "localhost"', '\tserver = "localhost"'),
        ('#\tport = 3306', '\tport = 5432'),
        ('#\tlogin = "radius"', f'\tlogin = "{DB_USER}"'),
        ('#\tpassword = "radpass"', f'\tpassword = "{DB_PASS}"'),
        ('radius_db = "radius"', f'radius_db = "{DB_NAME}"'),
    ]
    
    for old, new in replacements:
        run_command(
            f"sed -i 's|{old}|{new}|g' {sql_file}",
            f"Updating: {new.split('=')[0].strip() if '=' in new else 'SQL config'}"
        )
    
    # Enable SQL module
    run_command(
        f"ln -sf {config_dir}/mods-available/sql {config_dir}/mods-enabled/sql",
        "Enabling SQL module"
    )
    
    # Enable SQL in default site
    run_command(
        f"sed -i '/^\\tauth_log$/a \\\\tsql' {config_dir}/sites-enabled/default",
        "Enabling SQL in default site (authorize section)",
        ignore_errors=True
    )
    
    # Enable SQL in inner-tunnel
    run_command(
        f"sed -i '/^\\tauth_log$/a \\\\tsql' {config_dir}/sites-enabled/inner-tunnel",
        "Enabling SQL in inner-tunnel site",
        ignore_errors=True
    )

def configure_radius_clients():
    print_header("STEP 7: Configuring RADIUS Clients")
    
    config_dirs = ["/etc/freeradius/3.0", "/etc/freeradius/3.2"]
    config_dir = next((d for d in config_dirs if os.path.exists(d)), None)
    
    clients_file = f"{config_dir}/clients.conf"
    
    # Backup original
    run_command(f"cp {clients_file} {clients_file}.backup", "Backing up clients.conf")
    
    # Update localhost secret
    run_command(
        f"sed -i 's/secret = testing123/secret = {RADIUS_SECRET}/g' {clients_file}",
        f"Setting RADIUS shared secret for localhost"
    )
    
    print(f"\n   🔑 RADIUS Shared Secret: {RADIUS_SECRET}")
    print(f"   📝 Configure your Access Points with this secret!")

def add_test_user():
    print_header("STEP 8: Adding Test User")
    
    # Add test user to radcheck table
    sql = f"""
    INSERT INTO radcheck (username, attribute, op, value)
    VALUES ('{TEST_USERNAME}', 'Cleartext-Password', ':=', '{TEST_PASSWORD}')
    ON CONFLICT DO NOTHING;
    """
    
    run_command(
        f"PGPASSWORD={DB_PASS} psql -h localhost -U {DB_USER} -d {DB_NAME} -c \"{sql}\"",
        f"Adding test user: {TEST_USERNAME}"
    )
    
    print(f"\n   👤 Test Username: {TEST_USERNAME}")
    print(f"   🔐 Test Password: {TEST_PASSWORD}")

def start_freeradius():
    print_header("STEP 9: Starting FreeRADIUS")
    
    # Test configuration first
    print("🔍 Testing FreeRADIUS configuration...")
    result = run_command("freeradius -C", "Checking configuration syntax", ignore_errors=True)
    
    if result.returncode != 0:
        print("\n⚠️  Configuration has issues. Running in debug mode...")
        print("   Check the output above for errors.")
    
    # Start service
    run_command("systemctl enable freeradius", "Enabling FreeRADIUS on boot")
    run_command("systemctl restart freeradius", "Starting FreeRADIUS service")
    run_command("systemctl status freeradius --no-pager", "Checking FreeRADIUS status", ignore_errors=True)

def test_authentication():
    print_header("STEP 10: Testing RADIUS Authentication")
    
    # Check if radtest is available
    radtest_check = subprocess.run("which radtest", shell=True, capture_output=True)
    if radtest_check.returncode != 0:
        run_command("apt install -y freeradius-utils", "Installing RADIUS test utilities")
    
    # Run authentication test
    print(f"🧪 Testing authentication for user: {TEST_USERNAME}")
    result = run_command(
        f"radtest {TEST_USERNAME} {TEST_PASSWORD} localhost 0 {RADIUS_SECRET}",
        "Running RADIUS authentication test",
        ignore_errors=True
    )
    
    if "Access-Accept" in result.stdout:
        print("\n   🎉 SUCCESS! RADIUS authentication is working!")
    else:
        print("\n   ⚠️  Authentication test failed.")
        print("   💡 Debug with: sudo freeradius -X")
        print("   💡 Check logs: sudo journalctl -u freeradius -n 50")

# -------------------------------------------------------------------
# Main Execution
# -------------------------------------------------------------------
def print_final_summary():
    print_header("🎉 Setup Complete!")
    
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                     CONFIGURATION SUMMARY                        ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  📦 Database Information:                                        ║
║     Database Name: {db_name:<44}║
║     Database User: {db_user:<44}║
║     Database Pass: {db_pass:<44}║
║                                                                  ║
║  🔐 RADIUS Configuration:                                        ║
║     Shared Secret: {radius_secret:<44}║
║                                                                  ║
║  👤 Test User:                                                   ║
║     Username: {test_user:<49}║
║     Password: {test_pass:<49}║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

📋 NEXT STEPS:

1️⃣  Configure Your Access Point:
   • Add your RADIUS server IP (this machine's IP)
   • Use shared secret: {radius_secret}
   • Authentication port: 1812
   • Accounting port: 1813

2️⃣  Add Access Points to RADIUS:
   Edit: /etc/freeradius/*/clients.conf
   
   Add for each AP:
   client your-ap-name {{
       ipaddr = YOUR_AP_IP_ADDRESS
       secret = {radius_secret}
   }}
   
   Then restart: sudo systemctl restart freeradius

3️⃣  Add Real Users:
   PGPASSWORD={db_pass} psql -h localhost -U {db_user} -d {db_name}
   
   INSERT INTO radcheck (username, attribute, op, value)
   VALUES ('username', 'Cleartext-Password', ':=', 'password');

4️⃣  Monitor RADIUS:
   • Debug mode: sudo freeradius -X
   • View logs: sudo journalctl -u freeradius -f
   • Service status: sudo systemctl status freeradius

📚 Configuration Files:
   • RADIUS config: /etc/freeradius/3.0/
   • Clients: /etc/freeradius/3.0/clients.conf
   • SQL module: /etc/freeradius/3.0/mods-available/sql
   • PostgreSQL: /etc/postgresql/

✅ Setup completed at: {timestamp}

    """.format(
        db_name=DB_NAME,
        db_user=DB_USER,
        db_pass=DB_PASS,
        radius_secret=RADIUS_SECRET,
        test_user=TEST_USERNAME,
        test_pass=TEST_PASSWORD,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

def main():
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║   PostgreSQL + FreeRADIUS Automated Setup Script          ║
    ║   Complete installation and configuration                 ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    check_root()
    
    try:
        install_postgresql()
        setup_database()
        configure_pg_authentication()
        install_freeradius()
        import_radius_schema()
        configure_freeradius_sql()
        configure_radius_clients()
        add_test_user()
        start_freeradius()
        test_authentication()
        print_final_summary()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user!")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
