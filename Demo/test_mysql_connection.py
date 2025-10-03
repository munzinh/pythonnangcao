#!/usr/bin/env python3
"""
Test MySQL connection script.

This script tests the MySQL database connection using the configuration
from .env file.

Usage:
    python test_mysql_connection.py
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

def test_mysql_connection():
    """Test MySQL database connection."""
    print("Testing MySQL connection...")
    
    # Get database URI from environment
    database_uri = os.getenv('DATABASE_URI', 'mysql+pymysql://todo_user:password@localhost/todo_db')
    print(f"Database URI: {database_uri}")
    
    try:
        # Create engine
        engine = create_engine(database_uri, echo=False)
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 as test"))
            test_value = result.scalar()
            
            if test_value == 1:
                print("✅ MySQL connection successful!")
                
                # Test database exists
                result = conn.execute(text("SELECT DATABASE()"))
                current_db = result.scalar()
                print(f"✅ Connected to database: {current_db}")
                
                # Test if tasks table exists
                result = conn.execute(text("""
                    SELECT COUNT(*) 
                    FROM information_schema.tables 
                    WHERE table_schema = DATABASE() 
                    AND table_name = 'tasks'
                """))
                table_exists = result.scalar()
                
                if table_exists:
                    print("✅ Tasks table exists")
                    
                    # Count tasks
                    result = conn.execute(text("SELECT COUNT(*) FROM tasks"))
                    task_count = result.scalar()
                    print(f"✅ Found {task_count} tasks in database")
                else:
                    print("ℹ️  Tasks table does not exist yet (will be created on first run)")
                
                return True
            else:
                print("❌ Connection test failed")
                return False
                
    except Exception as e:
        print(f"❌ MySQL connection failed: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Check if MySQL server is running")
        print("2. Verify database credentials in .env file")
        print("3. Ensure database exists")
        print("4. Check network connectivity")
        return False

def main():
    """Main function."""
    print("=" * 50)
    print("MySQL Connection Test")
    print("=" * 50)
    
    success = test_mysql_connection()
    
    print("=" * 50)
    if success:
        print("✅ All tests passed! MySQL is ready to use.")
    else:
        print("❌ Connection test failed. Please check your configuration.")
    print("=" * 50)

if __name__ == '__main__':
    main()
