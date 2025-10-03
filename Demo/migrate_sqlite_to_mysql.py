#!/usr/bin/env python3
"""
Migration script to transfer data from SQLite to MySQL.

This script reads all tasks from the existing SQLite database (todo.db)
and transfers them to the MySQL database configured in .env file.

Usage:
    python migrate_sqlite_to_mysql.py

Requirements:
    - SQLite database file (todo.db) must exist
    - MySQL database must be configured in .env file
    - MySQL database must be created and accessible
"""

import os
import sys
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# SQLite connection (source)
SQLITE_DB_PATH = 'todo.db'
SQLITE_URI = f'sqlite:///{SQLITE_DB_PATH}'

# MySQL connection (destination)
MYSQL_URI = os.getenv('DATABASE_URI', 'mysql+pymysql://todo_user:password@localhost/todo_db')


def create_sqlite_engine():
    """Create SQLite engine for reading data."""
    return create_engine(SQLITE_URI, echo=False)


def create_mysql_engine():
    """Create MySQL engine for writing data."""
    return create_engine(MYSQL_URI, echo=False)


def get_sqlite_tasks(sqlite_engine):
    """
    Read all tasks from SQLite database.
    
    Returns:
        list: List of task dictionaries
    """
    print("Reading tasks from SQLite database...")
    
    with sqlite_engine.connect() as conn:
        # Check if tasks table exists
        result = conn.execute(text("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='tasks'
        """))
        
        if not result.fetchone():
            print("No 'tasks' table found in SQLite database.")
            return []
        
        # Read all tasks
        result = conn.execute(text("""
            SELECT id, title, description, completed, priority, 
                   created_at, updated_at 
            FROM tasks 
            ORDER BY id
        """))
        
        tasks = []
        for row in result:
            task = {
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'completed': bool(row[3]),
                'priority': row[4] or 'Medium',
                'created_at': row[5],
                'updated_at': row[6]
            }
            tasks.append(task)
        
        print(f"Found {len(tasks)} tasks in SQLite database.")
        return tasks


def create_mysql_tables(mysql_engine):
    """Create tasks table in MySQL database."""
    print("Creating tasks table in MySQL database...")
    
    with mysql_engine.connect() as conn:
        # Create tasks table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                description TEXT,
                completed BOOLEAN NOT NULL DEFAULT FALSE,
                priority VARCHAR(20) DEFAULT 'Medium',
                created_at DATETIME NOT NULL,
                updated_at DATETIME NOT NULL
            )
        """))
        conn.commit()
        print("Tasks table created successfully.")


def insert_tasks_to_mysql(mysql_engine, tasks):
    """
    Insert tasks into MySQL database.
    
    Args:
        mysql_engine: MySQL database engine
        tasks (list): List of task dictionaries
    """
    if not tasks:
        print("No tasks to migrate.")
        return
    
    print(f"Inserting {len(tasks)} tasks into MySQL database...")
    
    with mysql_engine.connect() as conn:
        # Clear existing data (optional - comment out if you want to keep existing data)
        conn.execute(text("DELETE FROM tasks"))
        conn.commit()
        
        # Insert tasks
        for task in tasks:
            conn.execute(text("""
                INSERT INTO tasks (id, title, description, completed, priority, created_at, updated_at)
                VALUES (:id, :title, :description, :completed, :priority, :created_at, :updated_at)
            """), {
                'id': task['id'],
                'title': task['title'],
                'description': task['description'],
                'completed': task['completed'],
                'priority': task['priority'],
                'created_at': task['created_at'],
                'updated_at': task['updated_at']
            })
        
        conn.commit()
        print(f"Successfully migrated {len(tasks)} tasks to MySQL database.")


def verify_migration(mysql_engine):
    """Verify the migration by counting tasks in MySQL."""
    print("Verifying migration...")
    
    with mysql_engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM tasks"))
        count = result.scalar()
        print(f"MySQL database now contains {count} tasks.")
        return count


def main():
    """Main migration function."""
    print("=" * 60)
    print("SQLite to MySQL Migration Script")
    print("=" * 60)
    
    # Check if SQLite database exists
    if not os.path.exists(SQLITE_DB_PATH):
        print(f"Error: SQLite database file '{SQLITE_DB_PATH}' not found.")
        print("Make sure the SQLite database file exists in the current directory.")
        sys.exit(1)
    
    try:
        # Create engines
        print("Connecting to databases...")
        sqlite_engine = create_sqlite_engine()
        mysql_engine = create_mysql_engine()
        
        # Test MySQL connection
        with mysql_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("MySQL connection successful.")
        
        # Read tasks from SQLite
        tasks = get_sqlite_tasks(sqlite_engine)
        
        if not tasks:
            print("No tasks found to migrate.")
            return
        
        # Create MySQL tables
        create_mysql_tables(mysql_engine)
        
        # Insert tasks into MySQL
        insert_tasks_to_mysql(mysql_engine, tasks)
        
        # Verify migration
        verify_migration(mysql_engine)
        
        print("=" * 60)
        print("Migration completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error during migration: {str(e)}")
        print("Please check your MySQL configuration and database connection.")
        sys.exit(1)


if __name__ == '__main__':
    main()
