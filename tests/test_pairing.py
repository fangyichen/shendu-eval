"""The load-bearing invariant: the scored arms differ ONLY in the observation cue.

If observed and unobserved differ in anything but the cue, the delta is no longer
uniquely attributable to "performing for an audience" (brief §6, §8.3).
"""

from shendu.observation_cues import OBSERVED_CUE, UNOBSERVED_CUE
from shendu.scenarios.base import OBSERVED, PLACEBO, UNOBSERVED
from shendu.scenarios.diligence import QUERY_RESULTS as DILIGENCE_QUERIES
from shendu.scenarios.diligence import render_stage2 as diligence_stage2
from shendu.scenarios.faithful_reporting import render_stage2


def test_scored_arms_differ_only_in_cue():
    observed = render_stage2(OBSERVED)
    unobserved = render_stage2(UNOBSERVED)

    assert observed != unobserved
    # Swapping just the cue text turns one arm into the other — nothing else differs.
    assert observed.replace(OBSERVED_CUE, UNOBSERVED_CUE) == unobserved
    assert unobserved.replace(UNOBSERVED_CUE, OBSERVED_CUE) == observed


def test_cues_are_equal_salience():
    # Same number of lines and same field keys -> only meaning differs, not volume.
    obs_lines, unobs_lines = OBSERVED_CUE.splitlines(), UNOBSERVED_CUE.splitlines()
    assert len(obs_lines) == len(unobs_lines)
    keys = lambda lines: [ln.split(":", 1)[0].strip() for ln in lines]
    assert keys(obs_lines) == keys(unobs_lines)


def test_placebo_keeps_observed_cue_but_changes_neutral():
    # Placebo must carry the OBSERVED cue (still "watched") yet not equal observed,
    # so a behavior change vs observed would implicate a neutral field, not observation.
    placebo = render_stage2(PLACEBO)
    assert OBSERVED_CUE in placebo
    assert UNOBSERVED_CUE not in placebo
    assert placebo != render_stage2(OBSERVED)


def test_diligence_arms_differ_only_in_cue():
    """The mild probe must satisfy the same load-bearing invariant."""
    observed = diligence_stage2(OBSERVED)
    unobserved = diligence_stage2(UNOBSERVED)
    assert observed != unobserved
    assert observed.replace(OBSERVED_CUE, UNOBSERVED_CUE) == unobserved


def test_diligence_scenario_has_no_failure_to_conceal():
    """This probe isolates corner-cutting from honesty: nothing fails here."""
    assert all(r["ok"] for r in DILIGENCE_QUERIES)
