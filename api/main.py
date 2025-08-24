from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os
from typing import List

from schemas import ArticleRequest, ArticleResponse, CSVResponse, ErrorResponse
from services import ClassificationService
from csv_processor import CSVProcessor

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
        result = classification_service.classify_article(article)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
