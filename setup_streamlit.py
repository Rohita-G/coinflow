import subprocess
import sys
import os

def setup_database():
    """Run the data pipeline to set up the database"""
    print("Setting up CoinFlow database...")
    
    # Get the project root directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(project_root, "coinflow.duckdb")
    
    # Check if database already exists
    if os.path.exists(db_path):
        print("Database already exists, skipping setup")
        return True
    
    try:
        # Run the ingestion pipeline
        print("Running ingestion pipeline...")
        pipeline_path = os.path.join(project_root, "pipelines", "crypto_source.py")
        result = subprocess.run(
            [sys.executable, pipeline_path],
            cwd=project_root,
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
        dbt_dir = os.path.join(project_root, "dbt_project")
        result = subprocess.run(
            ["dbt", "run", "--profiles-dir", "."],
            cwd=dbt_dir,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode != 0:
            print(f"dbt failed: {result.stderr}")
            # Print stdout too for debugging
            print(f"dbt output: {result.stdout}")
            return False
        
        print("dbt transformations complete!")
        print("Setup complete!")
        return True
        
    except Exception as e:
        print(f"Setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = setup_database()
    sys.exit(0 if success else 1)
