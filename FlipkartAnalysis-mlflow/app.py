import streamlit as st
import pickle
import re
import os

# Get current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Model paths
model_path = os.path.join(BASE_DIR, "model", "sentiment_model.pkl")
tfidf_path = os.path.join(BASE_DIR, "model", "tfidf_vectorizer.pkl")

# Load model & vectorizer
model = pickle.load(open(model_path, "rb"))
tfidf = pickle.load(open(tfidf_path, "rb"))


# Clean text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z ]', '', text)
    words = text.split()
    return ' '.join(words)


# Page config
st.set_page_config(page_title="Sentiment Analyzer")


# Title
st.title("Flipkart Review Sentiment Analyzer")


# Input box
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
