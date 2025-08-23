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
            
            # Convert DataFrame rows to ArticleRequest objects, filtering out empty titles/abstracts
            articles = []
            valid_indices = []
            
            for index, row in df.iterrows():
                title = str(row['title']).strip()
                abstract = str(row['abstract']).strip()
                
                # Skip rows with empty title or abstract
                if not title or not abstract or title.lower() in ['nan', 'none', ''] or abstract.lower() in ['nan', 'none', '']:
                    continue
                
                article = ArticleRequest(
                    title=title,
                    abstract=abstract
                )
                articles.append(article)
                valid_indices.append(index)
            
            # Classify all articles
            classifications = self.classification_service.classify_articles_batch(articles)
            
            # Create a new DataFrame with only the required columns plus labels, using only valid rows
            result_df = pd.DataFrame({
                'title': df.loc[valid_indices, 'title'],
                'abstract': df.loc[valid_indices, 'abstract'],
                'labels': [self._format_labels(classification.labels) for classification in classifications]
            })
            
            # Create output file
            output_path = self._create_output_file(file_path)
            result_df.to_csv(output_path, index=False)
            
            return output_path, len(articles)
            
        except Exception as e:
            raise Exception(f"Error processing CSV file: {str(e)}")
    
    def _format_labels(self, labels: list) -> str:
        """
        Format labels list to string representation
        
        Args:
            labels: List of label names
            
        Returns:
            Formatted string representation of labels
        """
        if not labels:
            return ""
        
        return "|".join(labels)
    
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
