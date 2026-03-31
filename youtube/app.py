import os
from urllib.parse import urlparse, parse_qs

import streamlit as st
from utils.transcript import get_transcript
from utils.pdf_generator import save_to_pdf
from utils.local_summarizer import summarize_text


def extract_video_id(url: str):
    url = url.strip()

    if "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("?")[0]

    if "youtube.com" in url:
        parsed = urlparse(url)

        if parsed.path == "/watch":
            return parse_qs(parsed.query).get("v", [None])[0]

        if "/shorts/" in parsed.path:
            return parsed.path.split("/shorts/")[-1].split("/")[0]

        if "/embed/" in parsed.path:
            return parsed.path.split("/embed/")[-1].split("/")[0]

    return None


st.set_page_config(page_title="YouTube Summarizer", page_icon="🎥", layout="centered")

st.title("🎥 YouTube Video Summarizer")
st.write("Convert YouTube videos into summary and PDF")

url = st.text_input("Enter YouTube URL")

if st.button("Generate"):
    if not url.strip():
        st.warning("Please enter a YouTube URL")
    else:
        video_id = extract_video_id(url)

        if not video_id:
            st.error("Invalid YouTube URL")
        else:
            with st.spinner("Processing..."):
                st.video(url)

                transcript = get_transcript(video_id)

                if transcript.startswith("Error:"):
                    st.error(transcript)
                else:
                    summary = summarize_text(transcript)

                    
                    article = f"""YouTube Video Summary

Summary:
{summary}

Transcript Preview:
{transcript[:2000]}
"""

                    os.makedirs("output", exist_ok=True)
                    pdf_path = os.path.join("output", "summary.pdf")
                    save_to_pdf(article, pdf_path)

                    st.success("Done!")

                    st.subheader("Summary")
                    st.write(summary)

                    st.subheader("Transcript Preview")
                    st.write(transcript[:2000])

                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            label="Download PDF",
                            data=f,
                            file_name="summary.pdf",
                            mime="application/pdf"
                        )