import streamlit as st
import pickle
import re


# Load model & vectorizer
model = pickle.load(open('sentiment_model.pkl', 'rb'))
tfidf = pickle.load(open('tfidf_vectorizer.pkl', 'rb'))


# Simple text cleaning (No NLTK needed)
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z ]', '', text)
    words = text.split()
    return ' '.join(words)


# Page Config
st.set_page_config(page_title="Sentiment Analyzer")


# Title
st.title("Flipkart Review Sentiment Analyzer")


# Input
review = st.text_area("Enter Your Review")


# Button
if st.button("Analyze"):

    if review.strip() == "":
        st.warning("Please enter a review")

    else:
        review = clean_text(review)

        vec = tfidf.transform([review])
        result = model.predict(vec)[0]

        if result == 1:
            st.success("Positive Review 😊")

        else:
            st.error("Negative Review 😞")