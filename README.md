# Article Label Maker

A multi-label classification system for scientific articles built with modern web technologies and AI-powered development tools.

## 🏗️ Backend Architecture

```mermaid
graph TB
    subgraph "FastAPI Application"
        A[main.py] --> B[FastAPI App]
        B --> C[API Endpoints]
        B --> D[Middleware]
    end

    subgraph "API Endpoints"
        C --> E["/classify_article<br/>POST"]
        C --> F["/classify_articles_in_csv<br/>POST"]
        C --> G["/download/{filename}<br/>GET"]
        C --> H["/health<br/>GET"]
        C --> I["/warmup<br/>POST"]
    end

    subgraph "Services Layer"
        J[ClassificationService] --> K[Classifier Factory]
        L[CSVProcessor] --> M[Pandas Processing]
        N[MetricsService] --> O[Analytics & Reporting]
    end

    subgraph "Classifier System"
        K --> P[ClassifierBase]
        P --> Q[ZeroShotClassifier]
        P --> R[FewShotClassifier]
        
        Q --> S[GLiClass Model]
        Q --> T[Transformers Pipeline]
        
        R --> U[Ollama Integration]
        R --> V[Few-Shot Prompts]
    end

    subgraph "Configuration"
        W[Settings] --> X[Environment Config]
        Y[Schemas] --> Z[Data Validation]
    end

    subgraph "External Dependencies"
        AA[Ollama Server] --> U
        BB[HuggingFace Models] --> S
        CC[CSV Files] --> M
    end

    %% Connections
    E --> J
    F --> L
    G --> L
    H --> J
    I --> J
    
    J --> W
    L --> Y
    N --> Y
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style J fill:#e8f5e8
    style P fill:#fff3e0
    style W fill:#fce4ec
```

## 📁 Backend File Structure

```mermaid
graph TD
    subgraph "API Root"
        A[main.py] --> B[FastAPI Entry Point]
        C[pyproject.toml] --> D[Dependencies]
        E[Dockerfile] --> F[Container Config]
    end

    subgraph "App Package"
        G[app/__init__.py] --> H[Package Root]
        
        subgraph "Classifiers"
            I[classifiers/__init__.py] --> J[Classifier Factory]
            K[classifier_base.py] --> L[Abstract Base Class]
            M[zero_shot.py] --> N[GLiClass Implementation]
            O[few_shot_prompting.py] --> P[Ollama Integration]
            Q[few_shot_prompts.py] --> R[Prompt Templates]
        end
        
        subgraph "Services"
            S[services/__init__.py] --> T[Services Package]
            U[classification.py] --> V[Classification Logic]
            W[csv_processor.py] --> X[CSV Handling]
            Y[metrics_service.py] --> Z[Analytics]
        end
        
        subgraph "Configuration"
            AA[config/__init__.py] --> BB[Config Package]
            CC[settings.py] --> DD[App Settings]
            EE[schemas.py] --> FF[Data Models]
        end
    end

    subgraph "Data & Output"
        GG[processed_csvs/] --> HH[Output Directory]
        II[sample_articles.csv] --> JJ[Test Data]
    end

    %% Relationships
    A --> G
    G --> I
    G --> S
    G --> AA
    
    I --> K
    I --> M
    I --> O
    I --> Q
    
    S --> U
    S --> W
    S --> Y
    
    AA --> CC
    AA --> EE
    
    style A fill:#e1f5fe
    style G fill:#f3e5f5
    style I fill:#e8f5e8
    style S fill:#fff3e0
    style AA fill:#fce4ec
```

## 🔄 Classification Flow

```mermaid
flowchart TD
    A[Client Request] --> B{Request Type}
    
    B -->|Single Article| C[POST /classify_article]
    B -->|CSV File| D[POST /classify_articles_in_csv]
    B -->|Health Check| E[GET /health]
    B -->|Model Warmup| F[POST /warmup]
    
    C --> G[ClassificationService]
    D --> H[CSVProcessor]
    E --> I[Health Check]
    F --> J[Model Warmup]
    
    G --> K{Classifier Type}
    K -->|zero_shot| L[ZeroShotClassifier]
    K -->|few_shot| M[FewShotClassifier]
    
    L --> N[GLiClass Model]
    M --> O[Ollama API]
    
    N --> P[Transformers Pipeline]
    O --> Q[LLM Generation]
    
    P --> R[Process Results]
    Q --> R
    
    R --> S[Format Response]
    S --> T[Return Labels]
    
    H --> U[Read CSV]
    U --> V[Process Each Article]
    V --> G
    G --> W[Write Results]
    W --> X[Return File]
    
    I --> Y[Check Services]
    J --> Z[Load Model]
    
    style A fill:#e1f5fe
    style G fill:#e8f5e8
    style L fill:#fff3e0
    style M fill:#fff3e0
    style N fill:#fce4ec
    style O fill:#fce4ec
```

## 🚀 Overview

Article Label Maker is a full-stack application that classifies scientific articles into multiple categories using machine learning. The system provides both a web interface for manual article classification and batch processing capabilities for CSV files.

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework for building APIs
- **Python 3.11** - Latest stable Python version
- **uv** - Fast Python package manager and installer
- **Pandas** - Data manipulation and analysis
- **Pydantic** - Data validation using Python type annotations
- **Uvicorn** - ASGI server for running FastAPI applications

### Frontend
- **Next.js 15** - React framework for production
- **React 19** - Latest React version
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **Radix UI** - Accessible component primitives
- **Lucide React** - Beautiful icons

### Development Tools
- **Docker & Docker Compose** - Containerization and orchestration
- **v0** - AI-powered UI development platform
- **Cursor** - AI-enhanced code editor
- **Git** - Version control

## 📋 Prerequisites

Before running the application, ensure you have the following installed:

- **Docker Engine** (version 20.10 or later)
- **Docker Compose** (version 2.0 or later)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd article-label-maker
```

### 2. Build and Start Services
```bash
docker-compose up --build
```

### 3. Access the Application
- **Frontend**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000/health

## 📁 Project Structure

```
article-label-maker/
├── api/                    # FastAPI backend
│   ├── main.py            # FastAPI application entry point
│   ├── schemas.py         # Pydantic data models
│   ├── services.py        # Business logic services
│   ├── csv_processor.py   # CSV file processing
│   ├── metrics_service.py # Model performance metrics
│   ├── pyproject.toml     # Python dependencies
│   ├── Dockerfile         # Backend container configuration
│   └── .dockerignore      # Docker ignore rules
├── frontend/              # Next.js frontend
│   ├── app/               # Next.js app directory
│   ├── components/        # React components
│   ├── services/          # API service layer
│   ├── package.json       # Node.js dependencies
│   ├── Dockerfile         # Frontend container configuration
│   └── .dockerignore      # Docker ignore rules
├── docker-compose.yml     # Service orchestration
└── README.md             # This file
```

## 📊 Features

### Article Classification
- **Single Article**: Manual input of title and abstract
- **Batch Processing**: Upload CSV files with multiple articles
- **Multi-label Support**: Articles can belong to multiple categories

### Supported Categories
- Cardiovascular
- Neurological
- Hepatorenal
- Oncological

## 🔌 API Endpoints

### Core Endpoints

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `GET` | `/` | Health check | - | Status message |
| `GET` | `/health` | Service health | - | Health status |
| `POST` | `/classify_article` | Classify single article | `ArticleRequest` | `ArticleResponse` |
| `POST` | `/classify_articles_in_csv` | Process CSV file | `multipart/form-data` | `CSVResponse` |
| `GET` | `/download/{filename}` | Download processed CSV | - | File download |

## 👥 Authors

- **Cesar Alfredo Uribe Leon**
- **David Giraldo Villa** 
- **Santiago Cano Duque**

---
