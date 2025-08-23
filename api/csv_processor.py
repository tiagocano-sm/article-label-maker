import pandas as pd
import tempfile
import os
from typing import List, Tuple
from schemas import ArticleRequest, ArticleResponse
from services import ClassificationService


class CSVProcessor:
    """Service for processing CSV files with article classification"""
    
    def __init__(self):
        self.classification_service = ClassificationService()
    
    def process_csv(self, file_path: str) -> Tuple[str, int]:
        """
        Process a CSV file and add classification labels
        
        Args:
            file_path: Path to the input CSV file
            
        Returns:
            Tuple of (output_file_path, number_of_processed_rows)
        """
        try:
            # Read the CSV file
            df = pd.read_csv(file_path)
            
            # Validate required columns
            required_columns = ['title', 'abstract']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            # Convert DataFrame rows to ArticleRequest objects
            articles = []
            for _, row in df.iterrows():
                article = ArticleRequest(
                    title=str(row['title']),
                    abstract=str(row['abstract'])
                )
                articles.append(article)
            
            # Classify all articles
            classifications = self.classification_service.classify_articles_batch(articles)
            
            # Add labels column to DataFrame
            df['labels'] = [self._format_labels(classification.labels) for classification in classifications]
            
            # Create output file
            output_path = self._create_output_file(file_path)
            df.to_csv(output_path, index=False)
            
            return output_path, len(df)
            
        except Exception as e:
            raise Exception(f"Error processing CSV file: {str(e)}")
    
    def _format_labels(self, labels: dict) -> str:
        """
        Format labels dictionary to string representation
        
        Args:
            labels: Dictionary of label:confidence pairs
            
        Returns:
            Formatted string representation of labels
        """
        if not labels:
            return ""
        
        formatted_labels = []
        for label, confidence in labels.items():
            formatted_labels.append(f"{label}:{confidence}")
        
        return ";".join(formatted_labels)
    
    def _create_output_file(self, input_path: str) -> str:
        """
        Create output file path for processed CSV
        
        Args:
            input_path: Original input file path
            
        Returns:
            Output file path
        """
        # Create output directory if it doesn't exist
        output_dir = "processed_csvs"
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate output filename
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_filename = f"{base_name}_classified.csv"
        output_path = os.path.join(output_dir, output_filename)
        
        return output_path
