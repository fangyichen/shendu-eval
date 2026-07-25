"""Shèndú (慎独): an integrity-under-no-observation eval for LLMs.

Measures whether a model's *stated* moral commitments hold in its *actions*
when it believes no one is watching — the score is a counterfactual delta
between an observed and an unobserved arm, with delta -> 0 being the good
outcome. See docs/brief.md for the full design.
"""

__version__ = "0.1.0"
