
from textblob import TextBlob
from .sentiment_analysis import SentimentAnalysisModel


class TextBlobSentimentAnalysis(SentimentAnalysisModel):
    """Sentiment analysis using TextBlob."""

    def classify(self, text: str) -> float:
        """
        Classify the sentiment of the text using TextBlob.

        :param text: The text to analyze.
        :return: A polarity score between -1.0 (negative) and 1.0 (positive).
        """
        return TextBlob(text).sentiment.polarity
