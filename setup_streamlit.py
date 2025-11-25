import subprocess
import sys
import os

def setup_database():
    """Run the data pipeline to set up the database"""
    print("Setting up CoinFlow database...")
    
    # Check if database already exists
    if os.path.exists("coinflow.duckdb"):
        print("Database already exists, skipping setup")
        return True
    
    try:
        # Run the ingestion pipeline
        print("Running ingestion pipeline...")
        result = subprocess.run(
            [sys.executable, "pipelines/crypto_source.py"],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode != 0:
            print(f"Pipeline failed: {result.stderr}")
            return False
        
        print("Ingestion complete!")
        
        # Run dbt transformations
        print("Running dbt transformations...")
        result = subprocess.run(
            ["dbt", "run", "--profiles-dir", "."],
            cwd="dbt_project",
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode != 0:
            print(f"dbt failed: {result.stderr}")
            return False
        
        print("Setup complete!")
        return True
        
    except Exception as e:
        print(f"Setup failed: {e}")
        return False

if __name__ == "__main__":
    setup_database()
