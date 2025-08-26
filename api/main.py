import logging
import os
import tempfile

import uvicorn
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from app.config.schemas import (
    ArticleRequest,
    ArticleResponse,
    CSVResponse,
    DashboardResponse,
    MetricsRequest,
    MetricsResponse,
)
from app.services.classification import ClassificationService
from app.services.csv_processor import CSVProcessor
from app.services.metrics_service import MetricsService

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "uvicorn.access": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "my_app": {"handlers": ["console"], "level": "DEBUG", "propagate": False},
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Article Classification API",
    description="API for classifying articles based on title and abstract",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Initialize services
classification_service = ClassificationService()
csv_processor = CSVProcessor()
metrics_service = MetricsService()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "http://frontend:3000",  # Docker container name
        "http://article-label-frontend:3000"  # Full container name
    ],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=dict)
async def root():
    """Health check endpoint"""
    return {
        "message": "Article Classification API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health", response_model=dict)
async def health_check():
    """Detailed health check endpoint"""
    try:
        # Check if classifier can be initialized
        classification_service._ensure_classifier_loaded()
        
        return {
            "status": "healthy",
            "message": "API and classifier are ready",
            "ollama_connected": True
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "message": f"Classifier initialization failed: {str(e)}",
            "ollama_connected": False
        }


@app.post("/warmup", response_model=dict)
async def warmup_model():
    """Warmup endpoint to preload the model"""
    try:
        logger.info("Starting model warmup...")
        
        # Initialize classifier if not already done
        classification_service._ensure_classifier_loaded()
        
        # Test with a simple prediction to warm up the model
        test_article = ArticleRequest(
            title="Test article for warmup",
            abstract="This is a test article to warm up the model and ensure it's loaded in memory."
        )
        
        result = classification_service.classify_article(test_article)
        
        logger.info("Model warmup completed successfully")
        return {
            "status": "success",
            "message": "Model warmed up successfully",
            "test_prediction": result.labels
        }
    except Exception as e:
        logger.error(f"Model warmup failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Model warmup failed: {str(e)}")


@app.post("/classify_article", response_model=ArticleResponse)
async def classify_article(article: ArticleRequest):
    """
    Classify a single article based on title and abstract
    
    Args:
        article: ArticleRequest containing title and abstract
        
    Returns:
        ArticleResponse with title and predicted labels
    """
    try:
        logger.info(f"Classifying article: {article.title[:50]}...")
        result = classification_service.classify_article(article)
        logger.info(f"Classification completed successfully")
        return result
    except Exception as e:
        logger.error(f"Classification failed: {str(e)}")
        # Return a more detailed error response
        return JSONResponse(
            status_code=500,
            content={
                "error": "Classification failed",
                "detail": str(e),
                "title": article.title,
                "labels": []
            }
        )


@app.post("/classify_articles_in_csv", response_model=CSVResponse)
async def classify_articles_in_csv(file: UploadFile = File(...)):
    """
    Classify articles from a CSV file and return the processed file
    
    Args:
        file: CSV file with 'title' and 'abstract' columns
        
    Returns:
        CSVResponse with processing status and file download link
    """
    try:
        # Validate file type
        if not file.filename.endswith('.csv'):
            raise HTTPException(
                status_code=400, 
                detail="File must be a CSV file"
            )
        
        # Create temporary file to store uploaded CSV
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            print(f"Processing CSV file: {temp_file_path}")
            # Process the CSV file
            output_path, processed_rows = csv_processor.process_csv(temp_file_path)
            print(f"CSV processed successfully: {output_path}, {processed_rows} rows")
            
            return CSVResponse(
                message="CSV processed successfully",
                processed_rows=processed_rows,
                output_filename=os.path.basename(output_path)
            )
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in classify_articles_in_csv: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download/{filename}")
async def download_processed_csv(filename: str):
    """
    Download a processed CSV file
    
    Args:
        filename: Name of the processed CSV file
        
    Returns:
        FileResponse with the CSV file
    """
    file_path = os.path.join("processed_csvs", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="text/csv"
    )


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "service": "article-classification-api"}


# Metrics endpoints
@app.post("/calculate_metrics", response_model=MetricsResponse)
async def calculate_metrics(request: MetricsRequest):
    """
    Calculate comprehensive metrics for multi-label classification
    
    Args:
        request: MetricsRequest containing true and predicted labels
        
    Returns:
        MetricsResponse with all calculated metrics
    """
    try:
        metrics = metrics_service.update_metrics_from_predictions(request.y_true, request.y_pred)
        return metrics_service.get_dashboard_data()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard_data():
    """
    Get dashboard data with all metrics
    
    Returns:
        DashboardResponse with formatted metrics for dashboard display
    """
    try:
        dashboard_data = metrics_service.get_dashboard_data()
        return DashboardResponse(**dashboard_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics/overall")
async def get_overall_metrics():
    """
    Get overall metrics only
    
    Returns:
        Dictionary with overall metrics
    """
    try:
        dashboard_data = metrics_service.get_dashboard_data()
        if not dashboard_data.get("has_data"):
            raise HTTPException(status_code=404, detail="No metrics data available")
        
        return dashboard_data.get("overall_metrics", {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





@app.get("/metrics/confusion_matrix")
async def get_overall_confusion_matrix():
    """
    Get overall confusion matrix
    
    Returns:
        Dictionary with overall confusion matrix data
    """
    try:
        dashboard_data = metrics_service.get_dashboard_data()
        if not dashboard_data.get("has_data"):
            raise HTTPException(status_code=404, detail="No metrics data available")
        
        return dashboard_data.get("overall_confusion_matrix", {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "detail": f"HTTP {exc.status_code} error"
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc)
        }
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_config=LOGGING_CONFIG, reload=True)
