from typing import List, Dict
import pandas as pd
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
from llama_index.core import VectorStoreIndex
from src.engine.query_engine import MaterialsRAGQueryEngine
from src.utils.logger import logger

class RagasEvaluator:
    """Evaluates the RAG system performance using Ragas metrics."""

    def __init__(self, query_engine: MaterialsRAGQueryEngine):
        self.query_engine = query_engine
        self.metrics = [
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
        ]

    def run_evaluation(self, test_questions: List[str], ground_truth: List[str]) -> pd.DataFrame:
        """
        Runs Ragas evaluation on a set of test questions.
        
        Args:
            test_questions: List of questions to ask the RAG system.
            ground_truth: List of expected answers.
            
        Returns:
            A pandas DataFrame with the evaluation results.
        """
        logger.info(f"Starting Ragas evaluation for {len(test_questions)} questions")
        
        data = {
            "question": [],
            "answer": [],
            "contexts": [],
            "ground_truth": ground_truth
        }
        
        for q in test_questions:
            result = self.query_engine.query(q)
            data["question"].append(q)
            data["answer"].append(result.response)
            data["contexts"].append([node.text for node in result.source_nodes])
            
        # Convert to dataset format required by Ragas
        from datasets import Dataset
        dataset = Dataset.from_dict(data)
        
        # Run evaluation
        # Note: Ragas evaluation usually requires an OpenAI/Azure API key or another LLM judge.
        # For local setup, this might need custom LLM configuration for Ragas.
        logger.warning("Ragas evaluation typically requires a judge LLM (e.g., OpenAI). Ensure credentials are set.")
        
        results = evaluate(dataset, metrics=self.metrics)
        
        logger.info("Evaluation complete.")
        return results.to_pandas()
