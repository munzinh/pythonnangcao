"""
Database module for SQLAlchemy connection and session management.

This module provides database initialization and session management
using SQLAlchemy ORM.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from backend.config import Config

Base = declarative_base()

engine = None
SessionLocal = None


def init_db(app=None):
    """
    Initialize database connection and create tables.
    
    Args:
        app: Flask application instance (optional)
        
    Returns:
        tuple: (engine, SessionLocal) database engine and session factory
        
    Raises:
        Exception: If database initialization fails
    """
    global engine, SessionLocal
    
    try:
        if app:
            database_uri = app.config['SQLALCHEMY_DATABASE_URI']
        else:
            database_uri = Config.SQLALCHEMY_DATABASE_URI
            
        engine = create_engine(
            database_uri,
            echo=True,
            pool_pre_ping=True
        )
        
        SessionLocal = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=engine)
        )
        
        Base.metadata.create_all(bind=engine)
        
        print(f"Database initialized successfully at {database_uri}")
        return engine, SessionLocal
        
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        raise


def get_session():
    """
    Get database session.
    
    Returns:
        Session: SQLAlchemy session object
        
    Raises:
        RuntimeError: If database not initialized
    """
    if SessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return SessionLocal()


def close_session(session):
    """
    Close database session safely.
    
    Args:
        session: SQLAlchemy session to close
    """
    try:
        session.close()
    except Exception as e:
        print(f"Error closing session: {str(e)}")
