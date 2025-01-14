from fastapi import FastAPI
import pickle
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from pydantic import BaseModel
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Load the trained model and vectorizer
tfidf = pickle.load(open("vectorizer.pkl", "rb"))
model = pickle.load(open("model.pkl", "rb"))

# Initialize Porter Stemmer
ps = PorterStemmer()

# Ensure stopwords are downloaded
nltk.download('stopwords')
nltk.download('punkt')

# Function to preprocess text
def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    
    text = [word for word in text if word.isalnum()]
    text = [word for word in text if word not in stopwords.words('english') and word not in string.punctuation]
    text = [ps.stem(word) for word in text]
    
    return " ".join(text)

# Define request model
class SMSRequest(BaseModel):
    message: str

# Define API route
@app.post("/predict")
def predict_spam(request: SMSRequest):
    transformed_sms = transform_text(request.message)
    vector_input = tfidf.transform([transformed_sms])
    result = model.predict(vector_input)[0]
    
    return {"prediction": "spam" if result == 1 else "not spam"}

