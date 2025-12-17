"""
Assessment Generator API
app/routers/assessment.py
"""
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import datetime

from ..database import get_db
from ..dependencies import get_current_user
from .. import crud, schemas, models
from ..services.assessment_service import assessment_service

router = APIRouter(prefix="/assessments", tags=["Assessment Generator"])


# ============ Background Generation ============

async def process_assessment_generation(
    assessment_id: int,
    custom_prompt: str,
    difficulty_level: str,
    question_types: List[str],
    total_questions: int,
    reference_document_ids: List[int],
    db: AsyncSession
):
    """Background task to generate assessment"""
    try:
        # Get reference documents
        reference_materials = []
        if reference_document_ids:
            for doc_id in reference_document_ids:
                doc = await crud.get_document(db, doc_id)
                if doc and doc.file_path:
                    # Read document
                    try:
                        with open(doc.file_path, 'rb') as f:
                            content = f.read()
                            if doc.file_type == 'application/pdf':
                                text = assessment_service.extract_text_from_pdf(content)
                                reference_materials.append(text)
                    except Exception as e:
                        print(f"Error reading document {doc_id}: {e}")

        # Generate questions
        questions, total_marks = await assessment_service.generate_assessment(
            custom_prompt=custom_prompt,
            difficulty_level=difficulty_level,
            question_types=question_types,
            total_questions=total_questions,
            reference_materials=reference_materials
        )

        # Save questions
        for question_data in questions:
            await crud.create_question(
                db=db,
                assessment_id=assessment_id,
                question_data=question_data
            )

        # Update assessment status
        await crud.update_assessment_completion(
            db=db,
            assessment_id=assessment_id,
            total_marks=total_marks,
            status=models.AssessmentStatus.COMPLETED
        )

        print(f"✅ Assessment {assessment_id} generated successfully")

    except Exception as e:
        print(f"❌ Error generating assessment {assessment_id}: {e}")

        # Update status to failed
        await crud.update_assessment_completion(
            db=db,
            assessment_id=assessment_id,
            total_marks=0,
            status=models.AssessmentStatus.FAILED
        )


# ============ Assessment CRUD ============

@router.post("/", response_model=schemas.AssessmentResponse, status_code=status.HTTP_201_CREATED)
async def create_assessment(
    assessment: schemas.AssessmentCreate,
    background_tasks: BackgroundTasks,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create AI-generated assessment

    Steps:
    1. Create assessment record (GENERATING status)
    2. Generate questions in background
    3. Return assessment ID immediately

    Client should poll /assessments/{id} to check status
    """
    # Create assessment record
    db_assessment = await crud.create_assessment(
        db=db,
        assessment=assessment,
        user_id=current_user.id
    )

    # Start background generation
    background_tasks.add_task(
        process_assessment_generation,
        assessment_id=db_assessment.id,
        custom_prompt=assessment.custom_prompt,
        difficulty_level=assessment.difficulty_level.value,
        question_types=[qt.value for qt in assessment.question_types],
        total_questions=assessment.total_questions,
        reference_document_ids=assessment.reference_document_ids,
        db=db
    )

    return db_assessment


@router.get("/{assessment_id}", response_model=schemas.AssessmentResponse)
async def get_assessment(
    assessment_id: int,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get assessment by ID (with answers - for instructors)"""
    assessment = await crud.get_assessment(db=db, assessment_id=assessment_id, include_answers=True)

    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    # Check authorization
    if assessment.created_by != current_user.id and current_user.is_student:
        raise HTTPException(status_code=403, detail="Not authorized")

    return assessment


@router.get("/{assessment_id}/preview", response_model=schemas.AssessmentPreview)
async def preview_assessment(
    assessment_id: int,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get assessment preview (no answers - for students)

    Used by students to take the assessment
    """
    assessment = await crud.get_assessment(db=db, assessment_id=assessment_id, include_answers=False)

    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    if assessment.status != models.AssessmentStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Assessment not ready yet")

    return assessment


@router.get("/", response_model=schemas.AssessmentListResponse)
async def list_assessments(
    course_id: int = None,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List assessments"""
    # Instructors see all, students see assessments from their courses
    created_by = None if not current_user.is_student else current_user.id

    assessments = await crud.get_assessments(
        db=db,
        course_id=course_id,
        created_by=created_by
    )

    return {
        "assessments": assessments,
        "total": len(assessments)
    }


@router.delete("/{assessment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_assessment(
    assessment_id: int,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete assessment"""
    assessment = await crud.get_assessment(db=db, assessment_id=assessment_id, include_answers=True)

    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    # Only creator can delete
    if assessment.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    await crud.delete_assessment(db=db, assessment_id=assessment_id)
    return None


# ============ Student Attempts ============

@router.post("/{assessment_id}/attempts", response_model=schemas.AssessmentAttemptResponse)
async def start_attempt(
    assessment_id: int,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Start an assessment attempt"""
    assessment = await crud.get_assessment(db=db, assessment_id=assessment_id, include_answers=False)

    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    if assessment.status != models.AssessmentStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Assessment not ready")

    # Create attempt
    attempt = await crud.create_attempt(
        db=db,
        assessment_id=assessment_id,
        student_id=current_user.id,
        max_score=assessment.total_marks
    )

    return attempt


@router.post("/attempts/{attempt_id}/submit", response_model=schemas.AssessmentAttemptResponse)
async def submit_attempt(
    attempt_id: int,
    submission: schemas.AssessmentSubmit,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Submit assessment answers"""
    # Get attempt
    result = await db.execute(
        select(models.AssessmentAttempt).where(models.AssessmentAttempt.id == attempt_id)
    )
    attempt = result.scalar_one_or_none()

    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")

    if attempt.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if attempt.submitted_at:
        raise HTTPException(status_code=400, detail="Already submitted")

    # Get assessment with answers
    assessment = await crud.get_assessment(
        db=db,
        assessment_id=attempt.assessment_id,
        include_answers=True
    )

    # Grade answers
    answers_dict = {ans.question_id: ans.answer for ans in submission.answers}
    score = self._grade_assessment(assessment.questions, answers_dict)

    # Calculate time taken
    time_taken = int((datetime.now() - attempt.started_at).total_seconds() / 60)

    # Update attempt
    attempt = await crud.submit_attempt(
        db=db,
        attempt_id=attempt_id,
        answers=answers_dict,
        score=score,
        time_taken=time_taken
    )

    return attempt


def _grade_assessment(questions: List[models.Question], answers: dict) -> float:
    """Grade student answers"""
    total_score = 0.0

    for question in questions:
        student_answer = answers.get(question.id)
        correct_answer = question.correct_answer

        if student_answer is None:
            continue

        # Grade based on question type
        if question.question_type in [models.QuestionType.MCQ, models.QuestionType.TRUE_FALSE]:
            # Single correct answer
            if isinstance(student_answer, list):
                student_answer = student_answer[0] if student_answer else None
            if isinstance(correct_answer, list):
                correct_answer = correct_answer[0] if correct_answer else None

            if str(student_answer).strip().upper() == str(correct_answer).strip().upper():
                total_score += question.marks

        elif question.question_type == models.QuestionType.MSQ:
            # Multiple correct answers
            if isinstance(student_answer, list) and isinstance(correct_answer, list):
                student_set = set(str(a).strip().upper() for a in student_answer)
                correct_set = set(str(a).strip().upper() for a in correct_answer)

                if student_set == correct_set:
                    total_score += question.marks
                elif student_set & correct_set:  # Partial credit
                    total_score += question.marks * 0.5

        elif question.question_type == models.QuestionType.NAT:
            # Numerical answer (allow small tolerance)
            try:
                student_num = float(student_answer)
                correct_num = float(correct_answer)
                tolerance = abs(correct_num) * 0.01  # 1% tolerance

                if abs(student_num - correct_num) <= tolerance:
                    total_score += question.marks
            except (ValueError, TypeError):
                pass

        elif question.question_type == models.QuestionType.SHORT_ANSWER:
            # Manual grading required - give half credit for now
            total_score += question.marks * 0.5

    return total_score


@router.get("/my-attempts", response_model=List[schemas.AssessmentAttemptResponse])
async def get_my_attempts(
    assessment_id: int = None,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current user's assessment attempts"""
    attempts = await crud.get_student_attempts(
        db=db,
        student_id=current_user.id,
        assessment_id=assessment_id
    )
    return attempts
