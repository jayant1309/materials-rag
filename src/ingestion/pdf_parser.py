import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from llama_index.core import Document
from src.utils.logger import logger


class BasePDFParser(ABC):
    """Abstract base class for PDF parsers."""

    @abstractmethod
    def parse(self, file_path: Path) -> List[Document]:
        """Parses a PDF file and returns a list of LlamaIndex Documents."""
        pass


class MarkerParser(BasePDFParser):
    """PDF parser using the Marker library for high-quality markdown extraction."""

    def parse(self, file_path: Path) -> List[Document]:
        """
        Parses a PDF using Marker.
        
        Note: This assumes Marker is installed and configured.
        """
        logger.info(f"Parsing PDF with Marker: {file_path}")
        try:
            from marker.convert import convert_single_pdf
            from marker.models import load_all_models

            # Load models (in production, these should be cached/pre-loaded)
            model_lst = load_all_models()
            full_text, images, out_metadata = convert_single_pdf(str(file_path), model_lst)
            
            return [Document(text=full_text, metadata=out_metadata)]
        except ImportError:
            logger.error("Marker library not found. Please install it with 'pip install marker-pdf'.")
            return []
        except Exception as e:
            logger.exception(f"Error parsing PDF with Marker: {e}")
            return []


class NougatParser(BasePDFParser):
    """PDF parser using Meta's Nougat for scientific document parsing."""

    def parse(self, file_path: Path) -> List[Document]:
        """
        Parses a PDF using Nougat.
        """
        logger.info(f"Parsing PDF with Nougat: {file_path}")
        # Nougat typically runs as a CLI or a separate service for best performance
        # Here we'll provide a placeholder for implementation
        logger.warning("Nougat implementation is a placeholder. Marker is recommended for local use.")
        return []


def get_parser(parser_type: str = "marker") -> BasePDFParser:
    """Factory function to get the appropriate PDF parser."""
    if parser_type.lower() == "marker":
        return MarkerParser()
    elif parser_type.lower() == "nougat":
        return NougatParser()
    else:
        raise ValueError(f"Unknown parser type: {parser_type}")
