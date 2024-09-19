from abc import ABC, abstractmethod

class SentimentAnalysisModel(ABC):
    """Interface for sentiment analysis models."""

    @abstractmethod
    def classify(self, text: str) -> float:
        """
        Classify the sentiment of the provided text.

        :param text: The text to analyze.
        :return: A polarity score between -1.0 (negative) and 1.0 (positive).
        """
        pass