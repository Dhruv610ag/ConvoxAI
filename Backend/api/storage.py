"""
Storage API Endpoints

This module provides endpoints for uploading, retrieving, and managing audio files in Supabase Storage.
"""

from fastapi import APIRouter, File, UploadFile, HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials
from core.models import AudioFileMetadata, AudioFileUploadResponse
from utils.supabase_client import (
    upload_file_to_storage, delete_file_from_storage, 
    get_file_url, insert_record, get_records, delete_record
)
from utils.validation import validate_audio_file
from utils.db_helpers import get_user_file
from config import ALLOWED_AUDIO_EXTENSIONS, AUDIO_BUCKET_NAME
from api.auth import get_authenticated_user, security
from pathlib import Path
from typing import List
import logging
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/storage", tags=["Storage"])


@router.post("/upload", response_model=AudioFileUploadResponse)
async def upload_audio_file(
    audio_file: UploadFile = File(..., description="Audio file to upload"),
    user: dict = Depends(get_authenticated_user)
):
    """
    Upload an audio file to Supabase Storage
    
    Args:
        audio_file: Audio file to upload
        user: Authenticated user (from dependency)
        
    Returns:
        File metadata and storage URL
    """
    try:
        # Validate file
        await validate_audio_file(audio_file)
        
        # Read file data
        file_data = await audio_file.read()
        file_size = len(file_data)
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        filename = f"{file_id}{file_extension}"
        
        # Upload to Supabase Storage
        storage_url = await upload_file_to_storage(
            bucket_name=AUDIO_BUCKET_NAME,
            file_path=filename,
            file_data=file_data,
            content_type=audio_file.content_type or "audio/mpeg",
            user_id=user.id
        )
        
        # Save metadata to database
        metadata = {
            "id": file_id,
            "user_id": user.id,
            "filename": audio_file.filename,
            "storage_path": f"{user.id}/{filename}",
            "file_size": file_size,
            "created_at": datetime.utcnow().isoformat()
        }
        
        await insert_record("audio_files", metadata)
        
        return AudioFileUploadResponse(
            file_id=file_id,
            filename=audio_file.filename,
            storage_url=storage_url,
            message="File uploaded successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"File upload error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file: {str(e)}"
        )


@router.get("/files", response_model=List[AudioFileMetadata])
async def list_user_files(user: dict = Depends(get_authenticated_user)):
    """
    List all audio files for the authenticated user
    
    Args:
        user: Authenticated user (from dependency)
        
    Returns:
        List of audio file metadata
    """
    try:
        files = await get_records(
            table_name="audio_files",
            filters={"user_id": user.id},
            order_by="created_at",
            limit=100
        )
        
        return [AudioFileMetadata(**file) for file in files]
        
    except Exception as e:
        logger.error(f"List files error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve files"
        )


@router.get("/file/{file_id}")
async def get_file(
    file_id: str,
    user: dict = Depends(get_authenticated_user)
):
    """
    Get audio file URL by ID
    
    Args:
        file_id: File ID
        user: Authenticated user (from dependency)
        
    Returns:
        File metadata and URL
    """
    try:
        # Get file metadata
        file_metadata = await get_user_file(file_id, user.id)
        
        # Get file URL
        file_url = await get_file_url(AUDIO_BUCKET_NAME, file_metadata["storage_path"])
        
        return {
            "file_id": file_metadata["id"],
            "filename": file_metadata["filename"],
            "url": file_url,
            "file_size": file_metadata["file_size"],
            "created_at": file_metadata["created_at"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get file error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve file"
        )


@router.delete("/file/{file_id}")
async def delete_file(
    file_id: str,
    user: dict = Depends(get_authenticated_user)
):
    """
    Delete an audio file
    
    Args:
        file_id: File ID
        user: Authenticated user (from dependency)
        
    Returns:
        Success message
    """
    try:
        # Get file metadata
        file_metadata = await get_user_file(file_id, user.id)
        
        # Delete from storage
        await delete_file_from_storage(AUDIO_BUCKET_NAME, file_metadata["storage_path"])
        
        # Delete metadata from database
        await delete_record("audio_files", file_id)
        
        return {"message": "File deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete file error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete file"
        )
