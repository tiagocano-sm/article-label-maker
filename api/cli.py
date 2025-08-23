import typer
import requests
import json
import pandas as pd
from pathlib import Path
from typing import Optional

app = typer.Typer(help="Article Classification API CLI")


@app.command()
def classify_article(
    title: str = typer.Option(..., "--title", "-t", help="Article title"),
    abstract: str = typer.Option(..., "--abstract", "-a", help="Article abstract"),
    api_url: str = typer.Option("http://localhost:8000", "--api-url", help="API base URL")
):
    """Classify a single article"""
    try:
        response = requests.post(
            f"{api_url}/classify_article",
            json={"title": title, "abstract": abstract}
        )
        response.raise_for_status()
        
        result = response.json()
        typer.echo("Classification Results:")
        typer.echo(f"Title: {result['title']}")
        typer.echo("Labels:")
        for label, confidence in result['labels'].items():
            typer.echo(f"  - {label}: {confidence}")
            
    except requests.exceptions.RequestException as e:
        typer.echo(f"Error: {e}", err=True)
    except Exception as e:
        typer.echo(f"Unexpected error: {e}", err=True)


@app.command()
def classify_csv(
    file_path: Path = typer.Argument(..., help="Path to CSV file"),
    api_url: str = typer.Option("http://localhost:8000", "--api-url", help="API base URL"),
    output_path: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file path")
):
    """Classify articles from a CSV file"""
    try:
        # Validate input file
        if not file_path.exists():
            typer.echo(f"Error: File {file_path} does not exist", err=True)
            raise typer.Exit(1)
        
        if not file_path.suffix.lower() == '.csv':
            typer.echo("Error: File must be a CSV", err=True)
            raise typer.Exit(1)
        
        # Upload and process CSV
        with open(file_path, 'rb') as f:
            files = {'file': (file_path.name, f, 'text/csv')}
            response = requests.post(f"{api_url}/classify_articles_in_csv", files=files)
        
        response.raise_for_status()
        result = response.json()
        
        typer.echo(f"✅ {result['message']}")
        typer.echo(f"📊 Processed {result['processed_rows']} articles")
        
        if result['output_filename']:
            download_url = f"{api_url}/download/{result['output_filename']}"
            typer.echo(f"📥 Download processed file: {download_url}")
            
            # Download the file if output path is specified
            if output_path:
                download_response = requests.get(download_url)
                download_response.raise_for_status()
                
                with open(output_path, 'wb') as f:
                    f.write(download_response.content)
                
                typer.echo(f"💾 File saved to: {output_path}")
        
    except requests.exceptions.RequestException as e:
        typer.echo(f"Error: {e}", err=True)
    except Exception as e:
        typer.echo(f"Unexpected error: {e}", err=True)


@app.command()
def health_check(
    api_url: str = typer.Option("http://localhost:8000", "--api-url", help="API base URL")
):
    """Check API health status"""
    try:
        response = requests.get(f"{api_url}/health")
        response.raise_for_status()
        
        result = response.json()
        typer.echo(f"✅ API Status: {result['status']}")
        typer.echo(f"🔧 Service: {result['service']}")
        
    except requests.exceptions.RequestException as e:
        typer.echo(f"❌ API Error: {e}", err=True)
    except Exception as e:
        typer.echo(f"Unexpected error: {e}", err=True)


@app.command()
def serve(
    host: str = typer.Option("0.0.0.0", "--host", "-h", help="Host to bind to"),
    port: int = typer.Option(8000, "--port", "-p", help="Port to bind to"),
    reload: bool = typer.Option(False, "--reload", help="Enable auto-reload")
):
    """Start the FastAPI server"""
    import uvicorn
    
    typer.echo(f"🚀 Starting Article Classification API on {host}:{port}")
    uvicorn.run("main:app", host=host, port=port, reload=reload)


if __name__ == "__main__":
    app()
