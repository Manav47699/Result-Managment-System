from django.db import connection
from typing import List, Tuple, Optional, Any


class BaseRepository:
    """Base repository with common database operations using raw SQL"""
    
    @staticmethod
    def execute_query(query: str, params: Optional[Tuple] = None) -> List[Tuple]:
        """
        Execute a SELECT query and return results
        
        Args:
            query: SQL SELECT statement
            params: Query parameters for safe execution
            
        Returns:
            List of tuples containing query results
        """
        with connection.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()
    
    @staticmethod
    def execute_insert(query: str, params: Tuple) -> int:
        """
        Execute an INSERT query and return the ID
        
        Args:
            query: SQL INSERT statement with RETURNING id
            params: Values to insert
            
        Returns:
            ID of newly inserted row
        """
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchone()
            return result[0] if result else None
    
    @staticmethod
    def execute_update(query: str, params: Tuple) -> int:
        """
        Execute an UPDATE query
        
        Args:
            query: SQL UPDATE statement
            params: Values to update
            
        Returns:
            Number of rows affected
        """
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.rowcount
    
    @staticmethod
    def execute_delete(query: str, params: Tuple) -> int:
        """
        Execute a DELETE query
        
        Args:
            query: SQL DELETE statement
            params: Conditions for deletion
            
        Returns:
            Number of rows deleted
        """
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.rowcount
