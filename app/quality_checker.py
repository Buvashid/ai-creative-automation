"""Provide quality-assurance status values for generated creatives."""

from dataclasses import dataclass

QA_PENDING_REVIEW = "PENDING_REVIEW"
QA_PASSED = "PASSED"
QA_REJECTED = "REJECTED"
QA_FIX_REQUIRED = "FIX_REQUIRED"


def initial_qa_status(generation_succeeded: bool) -> str:
    """Return the default QA status without approving generated artwork."""
    return QA_PENDING_REVIEW if generation_succeeded else QA_FIX_REQUIRED

@dataclass(frozen=True)
class QualityCheck:
    """Minimal result for a future creative quality check."""

    creative_id: str
    passed: bool
    issues: tuple[str, ...] = ()
