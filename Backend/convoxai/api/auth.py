"""
Authentication API Endpoints

This module provides authentication endpoints for user signup, signin, signout, and user info.
"""

from fastapi import APIRouter, HTTPException, status, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from convoxai.core.models import (
    UserSignUp, UserSignIn, AuthResponse, UserResponse, TokenResponse
)
from convoxai.utils.supabase_client import (
    sign_up_user, sign_in_user, sign_out_user, get_user_from_token
)
from typing import Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserSignUp):
    """
    Register a new user
    
    Args:
        user_data: User signup information (email, password, optional full_name)
        
    Returns:
        User information and authentication tokens
    """
    try:
        # Prepare metadata
        metadata = {}
        if user_data.full_name:
            metadata["full_name"] = user_data.full_name
        
        # Sign up user
        result = await sign_up_user(
            email=user_data.email,
            password=user_data.password,
            metadata=metadata
        )
        
        if not result.get("user") or not result.get("session"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create user account"
            )
        
        user = result["user"]
        session = result["session"]
        
        # Format response
        user_response = UserResponse(
            id=user.id,
            email=user.email,
            full_name=user.user_metadata.get("full_name") if user.user_metadata else None,
            created_at=user.created_at
        )
        
        token_response = TokenResponse(
            access_token=session.access_token,
            refresh_token=session.refresh_token,
            user=user_response
        )
        
        return AuthResponse(user=user_response, session=token_response)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Signup error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to sign up: {str(e)}"
        )


@router.post("/signin", response_model=AuthResponse)
async def signin(credentials: UserSignIn):
    """
    Sign in an existing user
    
    Args:
        credentials: User signin credentials (email, password)
        
    Returns:
        User information and authentication tokens
    """
    try:
        result = await sign_in_user(
            email=credentials.email,
            password=credentials.password
        )
        
        if not result.get("user") or not result.get("session"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        user = result["user"]
        session = result["session"]
        
        # Format response
        user_response = UserResponse(
            id=user.id,
            email=user.email,
            full_name=user.user_metadata.get("full_name") if user.user_metadata else None,
            created_at=user.created_at
        )
        
        token_response = TokenResponse(
            access_token=session.access_token,
            refresh_token=session.refresh_token,
            user=user_response
        )
        
        return AuthResponse(user=user_response, session=token_response)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Signin error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )


@router.post("/signout")
async def signout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Sign out the current user
    
    Args:
        credentials: Bearer token from Authorization header
        
    Returns:
        Success message
    """
    try:
        await sign_out_user(credentials.credentials)
        return {"message": "Successfully signed out"}
    except Exception as e:
        logger.error(f"Signout error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to sign out"
        )


@router.get("/user", response_model=UserResponse)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Get current user information
    
    Args:
        credentials: Bearer token from Authorization header
        
    Returns:
        Current user information
    """
    try:
        user = await get_user_from_token(credentials.credentials)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        
        return UserResponse(
            id=user.id,
            email=user.email,
            full_name=user.user_metadata.get("full_name") if user.user_metadata else None,
            created_at=user.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get user error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )


# Dependency for protected routes
async def get_authenticated_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Dependency to get authenticated user from token
    
    Args:
        credentials: Bearer token from Authorization header
        
    Returns:
        User information dictionary
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        user = await get_user_from_token(credentials.credentials)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"}
        )
