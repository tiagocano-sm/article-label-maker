from pydantic import BaseModel, Field
from typing import Dict, List, Optional
import pandas as pd


class ArticleRequest(BaseModel):
    """Schema for single article classification request"""
    title: str = Field(..., description="Article title", min_length=1)
    abstract: str = Field(..., description="Article abstract", min_length=1)


class ArticleResponse(BaseModel):
    """Schema for single article classification response"""
    title: str = Field(..., description="Article title")
    labels: List[str] = Field(..., description="Classification labels")


class CSVResponse(BaseModel):
    """Schema for CSV processing response"""
    message: str = Field(..., description="Processing status message")
    processed_rows: int = Field(..., description="Number of rows processed")
    output_filename: Optional[str] = Field(None, description="Output CSV filename")


class ErrorResponse(BaseModel):
    """Schema for error responses"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")
