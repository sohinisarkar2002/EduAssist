"""
Assessment Generator Service
app/services/assessment_service.py
"""
from typing import List, Dict, Any
import json
import PyPDF2
import io

from .gemini_client import gemini_client


class AssessmentService:
    """Service for generating assessments using AI"""

    async def generate_assessment(
        self,
        custom_prompt: str,
        difficulty_level: str,
        question_types: List[str],
        total_questions: int,
        reference_materials: List[str]  # List of text content from PDFs
    ) -> List[Dict]:
        """
        Generate complete assessment with questions

        Args:
            custom_prompt: User's instructions
            difficulty_level: EASY, MEDIUM, or HARD
            question_types: List of types to generate
            total_questions: Number of questions
            reference_materials: Text extracted from reference documents

        Returns:
            List of generated questions
        """
        # Combine reference materials
        context = "\n\n".join(reference_materials) if reference_materials else ""

        # Build prompt for Gemini
        system_prompt = self._build_system_prompt(
            custom_prompt,
            difficulty_level,
            question_types,
            total_questions,
            context
        )

        # Generate questions
        try:
            response = await gemini_client.generate_completion(
                prompt=system_prompt,
                temperature=0.8
            )

            # Parse response into structured questions
            questions = self._parse_gemini_response(response, question_types)

            # Ensure we have the right number
            if len(questions) < total_questions:
                # Generate more if needed
                additional = await self._generate_additional_questions(
                    total_questions - len(questions),
                    custom_prompt,
                    difficulty_level,
                    question_types,
                    context
                )
                questions.extend(additional)

            # Truncate if too many
            questions = questions[:total_questions]

            # Assign marks and order
            total_marks = 0
            for i, q in enumerate(questions, 1):
                q['order'] = i
                q['marks'] = self._calculate_marks(q['question_type'], difficulty_level)
                total_marks += q['marks']

            return questions, total_marks

        except Exception as e:
            print(f"Error generating assessment: {e}")
            raise

    def _build_system_prompt(
        self,
        custom_prompt: str,
        difficulty: str,
        question_types: List[str],
        total_questions: int,
        context: str
    ) -> str:
        """Build comprehensive prompt for Gemini"""

        type_instructions = {
            "MCQ": "Multiple Choice Questions with 4 options (only ONE correct answer)",
            "MSQ": "Multiple Select Questions with 4+ options (MULTIPLE correct answers)",
            "NAT": "Numerical Answer Type questions (answer is a number)",
            "SHORT_ANSWER": "Short answer questions (1-2 sentences)",
            "TRUE_FALSE": "True/False questions"
        }

        types_str = "\n".join([f"- {type_instructions.get(t, t)}" for t in question_types])

        prompt = f"""You are an expert educational content creator. Generate {total_questions} assessment questions.

**User Instructions:**
{custom_prompt}

**Difficulty Level:** {difficulty}

**Question Types to Generate:**
{types_str}

**Reference Material:**
{context[:3000] if context else "No specific reference material provided. Use general knowledge."}

**Output Format (STRICT JSON):**
Generate a JSON array of questions. Each question must follow this exact format:

For MCQ:
{{
  "question_type": "MCQ",
  "question_text": "What is...",
  "options": ["A. Option 1", "B. Option 2", "C. Option 3", "D. Option 4"],
  "correct_answer": ["A"],
  "explanation": "Explanation of why A is correct",
  "difficulty": "{difficulty}"
}}

For MSQ:
{{
  "question_type": "MSQ",
  "question_text": "Which of the following...",
  "options": ["A. Option 1", "B. Option 2", "C. Option 3", "D. Option 4"],
  "correct_answer": ["A", "C"],
  "explanation": "Explanation",
  "difficulty": "{difficulty}"
}}

For NAT:
{{
  "question_type": "NAT",
  "question_text": "Calculate...",
  "options": null,
  "correct_answer": "42.5",
  "explanation": "Calculation steps",
  "difficulty": "{difficulty}"
}}

For SHORT_ANSWER:
{{
  "question_type": "SHORT_ANSWER",
  "question_text": "Explain...",
  "options": null,
  "correct_answer": "Brief expected answer",
  "explanation": "Key points to cover",
  "difficulty": "{difficulty}"
}}

For TRUE_FALSE:
{{
  "question_type": "TRUE_FALSE",
  "question_text": "Statement...",
  "options": ["True", "False"],
  "correct_answer": ["True"],
  "explanation": "Why true/false",
  "difficulty": "{difficulty}"
}}

**Important Rules:**
1. Generate EXACTLY {total_questions} questions
2. Mix question types evenly from: {", ".join(question_types)}
3. Base questions on the reference material if provided
4. Ensure questions are {difficulty} difficulty
5. Provide clear, unambiguous questions
6. Include detailed explanations
7. Return ONLY valid JSON array, no other text

Generate the questions now as a JSON array:
"""

        return prompt

    def _parse_gemini_response(self, response: str, expected_types: List[str]) -> List[Dict]:
        """Parse Gemini's JSON response into question objects"""
        try:
            # Extract JSON from response (in case there's extra text)
            json_start = response.find('[')
            json_end = response.rfind(']') + 1

            if json_start == -1 or json_end == 0:
                # Try to find json blocks
                json_start = response.find('```json')
                if json_start != -1:
                    json_start = response.find('[', json_start)
                    json_end = response.rfind(']') + 1

            if json_start != -1 and json_end > json_start:
                json_str = response[json_start:json_end]
                questions = json.loads(json_str)

                # Validate and clean
                validated = []
                for q in questions:
                    if self._validate_question(q):
                        validated.append(q)

                return validated
            else:
                # Fallback: parse manually
                return self._manual_parse(response, expected_types)

        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")
            return self._manual_parse(response, expected_types)

    def _validate_question(self, question: Dict) -> bool:
        """Validate question structure"""
        required = ['question_type', 'question_text', 'correct_answer']
        return all(key in question for key in required)

    def _manual_parse(self, response: str, expected_types: List[str]) -> List[Dict]:
        """Fallback: Create simple questions if parsing fails"""
        print("Using fallback question generation")

        questions = []
        lines = response.split('\n')

        current_q = {}
        for line in lines:
            line = line.strip()
            if line.startswith('Question') or line.startswith('Q'):
                if current_q and 'question_text' in current_q:
                    questions.append(current_q)
                current_q = {
                    'question_type': expected_types[0],
                    'question_text': line,
                    'options': None,
                    'correct_answer': 'Generated answer',
                    'explanation': 'See reference material',
                    'difficulty': 'MEDIUM'
                }

        if current_q and 'question_text' in current_q:
            questions.append(current_q)

        return questions[:5]  # Return max 5 fallback questions

    async def _generate_additional_questions(
        self,
        count: int,
        prompt: str,
        difficulty: str,
        types: List[str],
        context: str
    ) -> List[Dict]:
        """Generate additional questions if needed"""
        # Similar to main generation but for fewer questions
        return []  # Simplified for now

    def _calculate_marks(self, question_type: str, difficulty: str) -> int:
        """Calculate marks based on question type and difficulty"""
        base_marks = {
            'MCQ': 1,
            'MSQ': 2,
            'NAT': 2,
            'SHORT_ANSWER': 3,
            'TRUE_FALSE': 1
        }

        difficulty_multiplier = {
            'EASY': 1,
            'MEDIUM': 1,
            'HARD': 2
        }

        return base_marks.get(question_type, 1) * difficulty_multiplier.get(difficulty, 1)

    def extract_text_from_pdf(self, pdf_bytes: bytes) -> str:
        """Extract text from PDF"""
        try:
            pdf_file = io.BytesIO(pdf_bytes)
            reader = PyPDF2.PdfReader(pdf_file)

            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"

            return text
        except Exception as e:
            print(f"Error extracting PDF text: {e}")
            return ""


# Singleton instance
assessment_service = AssessmentService()
