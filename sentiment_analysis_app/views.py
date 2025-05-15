# from django.shortcuts import render
# from django.http import JsonResponse
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.svm import LinearSVC
# import joblib

# # Load the model and vectorizer from the specified path
# MODEL_PATH = r'C:\Users\ankur\OneDrive\Desktop\Sem 2\adt\project\code_project\sentiment_analysis_app\sentiment_model.pkl'
# VECTORIZER_PATH = r'C:\Users\ankur\OneDrive\Desktop\Sem 2\adt\project\code_project\sentiment_analysis_app\vectorizer.pkl'

# # Load the model and vectorizer only once during the module import
# model = joblib.load(MODEL_PATH)
# vectorizer = joblib.load(VECTORIZER_PATH)

# def index(request):
#     """Render the index.html template."""
#     return render(request, 'index.html')

# def power_bi_visual1(request):
#     """Render the power_bi_visual1.html template."""
#     return render(request, 'power_bi_visual1.html')

# def power_bi_visual2(request):
#     """Render the power_bi_visual2.html template."""
#     return render(request, 'power_bi_visual2.html')

# def analyze_sentiment(request):
#     """Analyze sentiment of the text provided in the POST request."""
#     if request.method == 'POST':
#         text = request.POST.get('text', '')
        
#         # Preprocess the text
#         text_vectorized = vectorizer.transform([text])
        
#         # Predict sentiment
#         sentiment = model.predict(text_vectorized)

#         sentimental_output = sentiment[0]
        
#         # Return a JSON response with the sentiment prediction
#         return JsonResponse({'sentiment': sentimental_output})
#     else:
#         # Return a method not allowed response if the request method is not POST
#         return HttpResponseNotAllowed(['POST'])
# views.py
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
from django.conf import settings
import os
from nltk.tokenize import sent_tokenize
from collections import Counter
import re

# Replace hardcoded paths with relative paths
DOCUMENT_MODEL_PATH = os.path.join(settings.BASE_DIR, 'sentiment_analysis_app', 'document_sentiment_model.pkl')
ASPECT_MODEL_PATH = os.path.join(settings.BASE_DIR, 'sentiment_analysis_app', 'aspect_sentiment_model.pkl')
SENTENCE_MODEL_PATH = os.path.join(settings.BASE_DIR, 'sentiment_analysis_app', 'sentence_sentiment_model.pkl')

DOCUMENT_VECTORIZER_PATH = os.path.join(settings.BASE_DIR, 'sentiment_analysis_app', 'document_vectorizer.pkl')
ASPECT_VECTORIZER_PATH = os.path.join(settings.BASE_DIR, 'sentiment_analysis_app', 'aspect_vectorizer.pkl')
SENTENCE_VECTORIZER_PATH = os.path.join(settings.BASE_DIR, 'sentiment_analysis_app', 'sentence_vectorizer.pkl')

# Load the models and vectorizers only once during the module import
document_model = joblib.load(DOCUMENT_MODEL_PATH)
aspect_model = joblib.load(ASPECT_MODEL_PATH)
sentence_model = joblib.load(SENTENCE_MODEL_PATH)
document_vectorizer = joblib.load(DOCUMENT_VECTORIZER_PATH)
aspect_vectorizer = joblib.load(ASPECT_VECTORIZER_PATH)
sentence_vectorizer = joblib.load(SENTENCE_VECTORIZER_PATH)

def preprocess_text(text):
    """Preprocess the text."""
    processed_text = text.lower()  # Convert text to lowercase
    processed_text = re.sub(r'\W', ' ', processed_text)  # Remove non-word characters
    processed_text = re.sub(r'\s+', ' ', processed_text)  # Remove extra whitespaces
    return processed_text

def index(request):
    """Render the index.html template."""
    return render(request, 'index.html')

def power_bi_visual1(request):
    """Render the power_bi_visual1.html template."""
    return render(request, 'power_bi_visual1.html')

def power_bi_visual2(request):
    """Render the power_bi_visual2.html template."""
    return render(request, 'power_bi_visual2.html')

def analyze_sentiment(request):
    """Analyze sentiment of the text provided in the POST request."""
    if request.method == 'POST':
        text = request.POST.get('text', '')

        # Log the received text
        print("Received text:", text)
        
        # Preprocess the text
        text_preprocessed = preprocess_text(text)
        
        # Vectorize the text for document-level sentiment analysis
        text_vectorized_document = document_vectorizer.transform([text_preprocessed])
        
        # Predict document-level sentiment
        sentiment_document = document_model.predict(text_vectorized_document)
        
        # Vectorize the text for aspect-level sentiment analysis
        text_vectorized_aspect = aspect_vectorizer.transform([text_preprocessed])
        
        # Predict aspect-level sentiment
        sentiment_aspect = aspect_model.predict(text_vectorized_aspect)
        
        # Tokenize the text into sentences
        sentences = sent_tokenize(text_preprocessed)
        
        # Predict sentiment for each sentence and get the most common sentiment
        sentiments_sentence = []
        for sentence in sentences:
            sentence_vectorized = sentence_vectorizer.transform([sentence])
            sentiment_sentence = sentence_model.predict(sentence_vectorized)
            sentiments_sentence.append(sentiment_sentence[0])
        most_common_sentiment_sentence = Counter(sentiments_sentence).most_common(1)[0][0]
        
        # Log the predicted sentiments
        print("Document Sentiment:", sentiment_document[0])
        print("Aspect Sentiment:", sentiment_aspect[0])
        print("Sentence Sentiment:", most_common_sentiment_sentence)
        
        # Return a JSON response with the sentiment predictions
        return JsonResponse({
            'document_sentiment': sentiment_document[0],
            'aspect_sentiment': sentiment_aspect[0],
            'sentence_sentiment': most_common_sentiment_sentence
        })
    else:
        # Return a method not allowed response if the request method is not POST
        return HttpResponseNotAllowed(['POST'])
