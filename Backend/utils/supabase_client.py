"""
Supabase Client Utility Module

This module provides a centralized Supabase client and helper functions
for authentication, storage, and database operations.
"""

from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_SERVICE_KEY
from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class SupabaseClient:
    """Singleton Supabase client wrapper"""
    
    _instance: Optional[Client] = None
    _service_instance: Optional[Client] = None
    
    @classmethod
    def get_client(cls) -> Client:
        """Get the Supabase client instance (anon key)"""
        if cls._instance is None:
            if not SUPABASE_URL or not SUPABASE_KEY:
                raise ValueError(
                    "Supabase credentials not configured. "
                    "Please set SUPABASE_URL and SUPABASE_KEY in your .env file"
                )
            cls._instance = create_client(SUPABASE_URL, SUPABASE_KEY)
        return cls._instance
    
    @classmethod
    def get_service_client(cls) -> Client:
        """Get the Supabase service client (service role key for admin operations)"""
        if cls._service_instance is None:
            if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
                raise ValueError(
                    "Supabase service credentials not configured. "
                    "Please set SUPABASE_URL and SUPABASE_SERVICE_KEY in your .env file"
                )
            cls._service_instance = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        return cls._service_instance


# Authentication Helper Functions
async def sign_up_user(email: str, password: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Sign up a new user
    
    Args:
        email: User email
        password: User password
        metadata: Optional user metadata
        
    Returns:
        User data and session information
    """
    try:
        client = SupabaseClient.get_client()
        response = client.auth.sign_up({
            "email": email,
            "password": password,
            "options": {"data": metadata} if metadata else {}
        })
        return {
            "user": response.user,
            "session": response.session
        }
    except Exception as e:
        logger.error(f"Sign up error: {str(e)}")
        raise


async def sign_in_user(email: str, password: str) -> Dict[str, Any]:
    """
    Sign in an existing user
    
    Args:
        email: User email
        password: User password
        
    Returns:
        User data and session information
    """
    try:
        client = SupabaseClient.get_client()
        response = client.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return {
            "user": response.user,
            "session": response.session
        }
    except Exception as e:
        logger.error(f"Sign in error: {str(e)}")
        raise


async def sign_out_user(access_token: str) -> None:
    """
    Sign out a user
    
    Args:
        access_token: User's access token
    """
    try:
        client = SupabaseClient.get_client()
        client.auth.sign_out()
    except Exception as e:
        logger.error(f"Sign out error: {str(e)}")
        raise


async def get_user_from_token(access_token: str) -> Optional[Dict[str, Any]]:
    """
    Get user information from access token
    
    Args:
        access_token: User's access token
        
    Returns:
        User information or None if invalid
    """
    try:
        client = SupabaseClient.get_client()
        response = client.auth.get_user(access_token)
        return response.user
    except Exception as e:
        logger.error(f"Get user error: {str(e)}")
        return None


# Storage Helper Functions
async def upload_file_to_storage(
    bucket_name: str,
    file_path: str,
    file_data: bytes,
    content_type: str = "audio/mpeg",
    user_id: Optional[str] = None
) -> str:
    """
    Upload a file to Supabase Storage
    
    Args:
        bucket_name: Storage bucket name
        file_path: Path within the bucket
        file_data: File binary data
        content_type: MIME type of the file
        user_id: Optional user ID for organizing files
        
    Returns:
        Public URL of the uploaded file
    """
    try:
        client = SupabaseClient.get_client()
        
        # Organize files by user if user_id provided
        if user_id:
            file_path = f"{user_id}/{file_path}"
        
        response = client.storage.from_(bucket_name).upload(
            file_path,
            file_data,
            {"content-type": content_type}
        )
        
        # Get public URL
        public_url = client.storage.from_(bucket_name).get_public_url(file_path)
        return public_url
    except Exception as e:
        logger.error(f"File upload error: {str(e)}")
        raise


async def delete_file_from_storage(bucket_name: str, file_path: str) -> None:
    """
    Delete a file from Supabase Storage
    
    Args:
        bucket_name: Storage bucket name
        file_path: Path within the bucket
    """
    try:
        client = SupabaseClient.get_client()
        client.storage.from_(bucket_name).remove([file_path])
    except Exception as e:
        logger.error(f"File deletion error: {str(e)}")
        raise


async def get_file_url(bucket_name: str, file_path: str) -> str:
    """
    Get public URL for a file in storage
    
    Args:
        bucket_name: Storage bucket name
        file_path: Path within the bucket
        
    Returns:
        Public URL of the file
    """
    try:
        client = SupabaseClient.get_client()
        return client.storage.from_(bucket_name).get_public_url(file_path)
    except Exception as e:
        logger.error(f"Get file URL error: {str(e)}")
        raise


# Database Helper Functions
async def insert_record(table_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Insert a record into a table
    
    Args:
        table_name: Name of the table
        data: Record data
        
    Returns:
        Inserted record
    """
    try:
        client = SupabaseClient.get_client()
        response = client.table(table_name).insert(data).execute()
        return response.data[0] if response.data else {}
    except Exception as e:
        logger.error(f"Insert error: {str(e)}")
        raise


async def get_records(
    table_name: str,
    filters: Optional[Dict[str, Any]] = None,
    order_by: Optional[str] = None,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Get records from a table
    
    Args:
        table_name: Name of the table
        filters: Optional filters (e.g., {"user_id": "123"})
        order_by: Optional column to order by
        limit: Optional limit on number of records
        
    Returns:
        List of records
    """
    try:
        client = SupabaseClient.get_client()
        query = client.table(table_name).select("*")
        
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)
        
        if order_by:
            query = query.order(order_by, desc=True)
        
        if limit:
            query = query.limit(limit)
        
        response = query.execute()
        return response.data
    except Exception as e:
        logger.error(f"Get records error: {str(e)}")
        raise


async def update_record(table_name: str, record_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a record in a table
    
    Args:
        table_name: Name of the table
        record_id: ID of the record to update
        data: Updated data
        
    Returns:
        Updated record
    """
    try:
        client = SupabaseClient.get_client()
        response = client.table(table_name).update(data).eq("id", record_id).execute()
        return response.data[0] if response.data else {}
    except Exception as e:
        logger.error(f"Update error: {str(e)}")
        raise


async def delete_record(table_name: str, record_id: str) -> None:
    """
    Delete a record from a table
    
    Args:
        table_name: Name of the table
        record_id: ID of the record to delete
    """
    try:
        client = SupabaseClient.get_client()
        client.table(table_name).delete().eq("id", record_id).execute()
    except Exception as e:
        logger.error(f"Delete error: {str(e)}")
        raise
