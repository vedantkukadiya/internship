from youtube_transcript_api import YouTubeTranscriptApi


def get_transcript(video_id: str) -> str:
    try:
        api = YouTubeTranscriptApi()
        fetched_transcript = api.fetch(video_id, languages=["en", "hi"])

        text = " ".join(
            snippet.text.strip()
            for snippet in fetched_transcript
            if getattr(snippet, "text", "").strip()
        )

        if not text:
            return "Error: Transcript is empty."

        return text

    except Exception as e:
        return f"Error: Could not fetch transcript. {e}"