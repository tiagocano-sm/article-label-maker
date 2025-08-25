from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any


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


class MetricsRequest(BaseModel):
    """Schema for metrics calculation request"""
    y_true: List[List[str]] = Field(..., description="True labels for each sample")
    y_pred: List[List[str]] = Field(..., description="Predicted labels for each sample")


class MetricsResponse(BaseModel):
    """Schema for metrics response"""
    overall_metrics: Dict[str, Any] = Field(..., description="Overall classification metrics")
    overall_confusion_matrix: Dict[str, Any] = Field(..., description="Overall confusion matrix")
    labels: List[str] = Field(..., description="List of all labels")
    last_updated: str = Field(..., description="Last update timestamp")


class DashboardResponse(BaseModel):
    """Schema for dashboard data response"""
    overall_metrics: Dict[str, Any] = Field(..., description="Overall metrics")
    overall_confusion_matrix: Dict[str, Any] = Field(..., description="Overall confusion matrix")
    labels: List[str] = Field(..., description="Available labels")
    last_updated: str = Field(..., description="Last update timestamp")
    has_data: bool = Field(..., description="Whether metrics data is available")



