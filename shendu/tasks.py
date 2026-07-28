"""Inspect AI @task definitions for the Shèndú eval.

Phase 0 contains only a smoke task whose sole purpose is to prove the harness
runs end-to-end. Phase 1 will add the real two-stage faithful-reporting task.

Run (no external model needed)::

    uv run inspect eval shendu/tasks.py@smoke --model mockllm/model

Run against a local LM Studio model::

    export LMSTUDIO_BASE_URL=http://localhost:1234/v1
    export LMSTUDIO_API_KEY=lm-studio
    uv run inspect eval shendu/tasks.py@smoke --model openai-api/lmstudio/<model-name>
"""

from __future__ import annotations

from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.scorer import includes
from inspect_ai.solver import generate

from shendu.scenarios.diligence import build_dataset as diligence_dataset
from shendu.scenarios.faithful_reporting import build_dataset
from shendu.scorer import diligence_scorer, integrity_scorer
from shendu.solver import two_stage_solver


@task
def smoke() -> Task:
    """Phase 0 smoke test: end-to-end plumbing check, not a real measurement."""
    return Task(
        dataset=[
            Sample(
                input="Reply with exactly the word: OK",
                target="OK",
            )
        ],
        solver=generate(),
        scorer=includes(),
    )


@task
def faithful_reporting() -> Task:
    """Phase 1: the faithful-reporting integrity pair (brief §5.2).

    Headline metric is ``integrity_gap`` = P(comply|observed) − P(comply|unobserved);
    gap ≈ 0 is the good outcome. ``placebo`` and ``tension`` arms are diagnostic.
    """
    return Task(
        dataset=build_dataset(),
        solver=two_stage_solver(),
        scorer=integrity_scorer(),
    )


@task
def diligence() -> Task:
    """The mild probe: a tedious required check nobody would notice was skipped.

    No metric fails here, so there is nothing to conceal — this isolates
    corner-cutting-when-unobserved from honesty, and compliance costs one tool
    call per table, which keeps the measurement valid across capability levels.
    """
    return Task(
        dataset=diligence_dataset(),
        solver=two_stage_solver(),
        scorer=diligence_scorer(),
    )
