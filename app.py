import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()


def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
    
    text = y[:]
    y.clear()
    
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
            
    text = y[:]
    y.clear()
    
    for i in text:
        y.append(ps.stem(i))
    
    return " ".join(y)

tfidf = pickle.load(open('C:/Users/bhave/OneDrive/Desktop/Github/sms_classifier/vectorizer.pkl', 'rb'))

model = pickle.load(open('C:/Users/bhave/OneDrive/Desktop/Github/sms_classifier/model.pkl','rb'))

st.title("SMS Classifier")
int_sms = st.text_area("Enter the Message")

if st.button("Predict"):
    
    # preprocess
    transformed_sms = transform_text(int_sms)
    # vectorize
    vector_input = tfidf.transform([transformed_sms])
    # predict
    result = model.predict(vector_input)[0]
    # display
    
    if result==1:
        st.header("It is Spam Message!")
        
    else:
        st.header("It is Not A Spam Message!")

