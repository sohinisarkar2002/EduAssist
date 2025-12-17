"""
YouTube Service - Extract captions and metadata
app/services/youtube_service.py
"""
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
from typing import List, Dict, Optional
import re


class YouTubeService:
    """Service for extracting YouTube video captions and metadata"""

    @staticmethod
    def extract_video_id(url: str) -> str:
        """
        Extract video ID from various YouTube URL formats

        Supports:
        - https://www.youtube.com/watch?v=VIDEO_ID
        - https://youtu.be/VIDEO_ID
        - https://www.youtube.com/embed/VIDEO_ID
        """
        patterns = [
            r'(?:youtube\.com\/watch\?v=)([\w-]+)',
            r'(?:youtu\.be\/)([\w-]+)',
            r'(?:youtube\.com\/embed\/)([\w-]+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        raise ValueError(f"Could not extract video ID from URL: {url}")

    @staticmethod
    def get_video_metadata(url: str) -> Dict:
        """
        Get video metadata using pytube

        Returns:
            dict with title, duration, thumbnail_url
        """
        try:
            yt = YouTube(url)

            return {
                "title": yt.title,
                "duration": yt.length,  # in seconds
                "thumbnail_url": yt.thumbnail_url,
                "author": yt.author,
                "views": yt.views,
                "description": yt.description[:500] if yt.description else ""
            }
        except Exception as e:
            print(f"Error getting video metadata: {e}")
            return {
                "title": "Unknown",
                "duration": 0,
                "thumbnail_url": "",
                "author": "",
                "views": 0,
                "description": ""
            }

    @staticmethod
    def get_transcript(video_id: str, languages: List[str] = ['en']) -> List[Dict]:
        """
        Get video transcript/captions

        Args:
            video_id: YouTube video ID
            languages: List of language codes to try (default: ['en'])

        Returns:
            List of transcript segments with 'text', 'start', 'duration'
        """
        try:
            transcript = YouTubeTranscriptApi.get_transcript(
                video_id,
                languages=languages
            )
            return transcript
        except Exception as e:
            print(f"Error getting transcript: {e}")
            raise ValueError(f"Could not get captions for video. Error: {str(e)}")

    @staticmethod
    def check_captions_available(video_id: str) -> bool:
        """Check if video has captions available"""
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            return len(list(transcript_list)) > 0
        except:
            return False

    @staticmethod
    def extract_segment_transcript(
        transcript: List[Dict],
        start_time: int,
        end_time: int
    ) -> str:
        """
        Extract transcript text for a specific time segment

        Args:
            transcript: Full video transcript
            start_time: Start time in seconds
            end_time: End time in seconds

        Returns:
            Concatenated transcript text for the segment
        """
        segment_text = []

        for entry in transcript:
            entry_start = entry['start']
            entry_end = entry_start + entry['duration']

            # Check if this entry overlaps with our segment
            if entry_end >= start_time and entry_start <= end_time:
                segment_text.append(entry['text'])

        return ' '.join(segment_text)

    @staticmethod
    def format_time(seconds: int) -> str:
        """Convert seconds to HH:MM:SS format"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60

        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"


# Singleton instance
youtube_service = YouTubeService()
