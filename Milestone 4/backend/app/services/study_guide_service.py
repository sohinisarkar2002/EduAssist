"""
Study Guide Generator Service
app/services/study_guide_service.py
"""
from typing import List, Dict
from .youtube_service import youtube_service
from .gemini_client import gemini_client


class StudyGuideService:
    """Service for generating study guides from video segments"""

    async def generate_study_guide(
        self,
        video_id: str,
        transcript: List[Dict],
        priority_segments: List[Dict],
        title: str
    ) -> Dict:
        """
        Generate comprehensive study guide from priority segments

        Args:
            video_id: YouTube video ID
            transcript: Full video transcript
            priority_segments: List of {start, end, priority} segments
            title: Study guide title

        Returns:
            Dict with content, key_topics, segments
        """
        # Extract text from each priority segment
        segment_analyses = []

        for segment in priority_segments:
            segment_text = youtube_service.extract_segment_transcript(
                transcript,
                segment['start'],
                segment['end']
            )

            # Generate summary and key points for this segment
            segment_analysis = await self._analyze_segment(
                segment_text,
                segment['start'],
                segment['end'],
                segment.get('priority', 'medium')
            )

            segment_analyses.append(segment_analysis)

        # Generate comprehensive study guide
        study_guide_content = await self._generate_comprehensive_guide(
            title,
            segment_analyses
        )

        # Extract key topics
        key_topics = await self._extract_key_topics(segment_analyses)

        return {
            "content": study_guide_content,
            "key_topics": key_topics,
            "segments": segment_analyses
        }

    async def _analyze_segment(
        self,
        text: str,
        start: int,
        end: int,
        priority: str
    ) -> Dict:
        """Analyze a single video segment"""

        prompt = f"""Analyze this educational video segment and provide:
1. A concise summary (2-3 sentences)
2. 3-5 key points or concepts covered

Segment transcript:
{text}

Priority level: {priority}

Format response as:
SUMMARY:
[your summary]

KEY POINTS:
- [point 1]
- [point 2]
- [point 3]
"""

        try:
            response = await gemini_client.generate_completion(
                prompt=prompt,
                temperature=0.7
            )

            # Parse response
            summary, key_points = self._parse_analysis_response(response)

            return {
                "start_time": start,
                "end_time": end,
                "transcript": text,
                "priority": priority,
                "summary": summary,
                "key_points": key_points
            }
        except Exception as e:
            print(f"Error analyzing segment: {e}")
            return {
                "start_time": start,
                "end_time": end,
                "transcript": text,
                "priority": priority,
                "summary": "Error generating summary",
                "key_points": []
            }

    async def _generate_comprehensive_guide(
        self,
        title: str,
        segment_analyses: List[Dict]
    ) -> str:
        """Generate comprehensive study guide from all segments"""

        # Combine all summaries and key points
        combined_content = []
        for i, seg in enumerate(segment_analyses, 1):
            time_range = f"{youtube_service.format_time(seg['start_time'])} - {youtube_service.format_time(seg['end_time'])}"
            combined_content.append(f"Segment {i} ({time_range}):\n{seg['summary']}")

        context = "\n\n".join(combined_content)

        prompt = f"""Create a comprehensive study guide for: "{title}"

Based on these video segment analyses:

{context}

Generate a well-structured study guide with:
1. Introduction/Overview
2. Main Topics (organized logically)
3. Key Concepts (explained clearly)
4. Important Points to Remember
5. Summary/Conclusion

Format in Markdown. Be educational, clear, and concise.
"""

        try:
            study_guide = await gemini_client.generate_completion(
                prompt=prompt,
                temperature=0.7
            )
            return study_guide
        except Exception as e:
            print(f"Error generating study guide: {e}")
            # Fallback: simple concatenation
            return self._create_fallback_guide(title, segment_analyses)

    async def _extract_key_topics(self, segment_analyses: List[Dict]) -> List[str]:
        """Extract key topics from all segments"""

        all_key_points = []
        for seg in segment_analyses:
            all_key_points.extend(seg.get('key_points', []))

        if not all_key_points:
            return []

        # Use Gemini to identify main topics
        prompt = f"""Given these key points from a video, identify the 5-10 main topics/themes:

{chr(10).join(f"- {point}" for point in all_key_points)}

Return only the topic names, one per line.
"""

        try:
            response = await gemini_client.generate_completion(
                prompt=prompt,
                temperature=0.5
            )

            topics = [line.strip('- ').strip() for line in response.split('\n') if line.strip()]
            return topics[:10]  # Max 10 topics
        except:
            # Fallback: use first words of each key point
            return list(set(point.split()[0] for point in all_key_points[:10]))

    def _parse_analysis_response(self, response: str) -> tuple:
        """Parse Gemini response into summary and key points"""
        try:
            parts = response.split('KEY POINTS:')
            summary = parts[0].replace('SUMMARY:', '').strip()

            if len(parts) > 1:
                key_points_text = parts[1].strip()
                key_points = [
                    line.strip('- ').strip()
                    for line in key_points_text.split('\n')
                    if line.strip() and line.strip().startswith('-')
                ]
            else:
                key_points = []

            return summary, key_points
        except:
            return response[:200], []

    def _create_fallback_guide(self, title: str, segment_analyses: List[Dict]) -> str:
        """Create simple fallback study guide if AI generation fails"""
        guide = f"# {title}\n\n"

        for i, seg in enumerate(segment_analyses, 1):
            time_range = f"{youtube_service.format_time(seg['start_time'])} - {youtube_service.format_time(seg['end_time'])}"
            guide += f"## Segment {i} ({time_range})\n\n"
            guide += f"{seg['summary']}\n\n"

            if seg.get('key_points'):
                guide += "**Key Points:**\n"
                for point in seg['key_points']:
                    guide += f"- {point}\n"
                guide += "\n"

        return guide


# Singleton instance
study_guide_service = StudyGuideService()
