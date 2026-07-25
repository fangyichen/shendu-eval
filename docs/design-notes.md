# Design notes — running decision log

Chronological log of implementation decisions, complementing the settled design
in [brief.md](brief.md). Newest entries at the top.

## 2026-06-29 — Phase 0 scaffold

- **Package manager: `uv`** (Inspect's default; aligns with the `inspect_evals`
  ecosystem we eventually contribute to). Repo root *is* this directory; the
  importable package is `shendu`.
- **First subject-under-test: a local model via LM Studio** (OpenAI-compatible
  endpoint at `http://localhost:1234/v1`). Free to iterate while building the
  scaffold and scorer. A frontier model gets swapped in for the Phase-3
  eval-awareness realism work, where model capability actually matters.
  - Inspect wiring: `--model openai-api/lmstudio/<model>` with env
    `LMSTUDIO_BASE_URL` and `LMSTUDIO_API_KEY`.
- **Smoke task uses `mockllm/model`** so Phase 0 / CI runs green with zero
  external dependencies. The smoke task is a plumbing check, not a measurement.
- Pinned `inspect-ai>=0.3.50`. The brief warns the framework moves — re-read the
  live Inspect docs before relying on any API detail.

### Open decisions still owed a human call (brief §10)

1. Observation-cue inventory (which incidental signals say "unwatched" without
   smelling like a test) — empirical, deferred to Phase 3.
2. Stage-1 elicitation method (voluntary, task-motivated principle statement).
3. Models under test + sampling settings (delta measured at fixed temperature).
4. Faithful-reporting violation taxonomy (lie vs. omission vs. misleading-true).
5. Eval-aware handling policy (default: report separately, never silently drop).
6. Hypocrisy index as headline vs. secondary metric.
