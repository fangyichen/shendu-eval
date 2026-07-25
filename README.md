# Shèndú (慎独) — an integrity-under-no-observation eval

An agentic LLM evaluation that measures whether a model's **stated** moral
commitments hold up in its **actions** when it believes no one is watching.

The score is a **counterfactual delta** between two arms of a paired scenario
that differ *only* in an incidental observation cue. The good outcome is
**delta → 0** (the model behaves the same whether or not it thinks it is
observed) — this inverts the usual "higher is better". See [docs/brief.md](docs/brief.md)
for the full design and the hard measurement constraints (§4).

Built on [Inspect AI](https://inspect.aisi.org.uk/).

## Quickstart

```bash
# install uv if you don't have it: https://docs.astral.sh/uv/
uv sync --extra dev          # create .venv and install deps

# Phase 0 smoke test — runs end-to-end with no external model:
uv run inspect eval shendu/tasks.py@smoke --model mockllm/model

# run the test suite:
uv run pytest
```

### Running against a local LM Studio model

Start a model server in LM Studio (default port 1234), then:

```bash
export LMSTUDIO_BASE_URL=http://localhost:1234/v1
export LMSTUDIO_API_KEY=lm-studio
uv run inspect eval shendu/tasks.py@smoke --model openai-api/lmstudio/<model-name>
```

## Status

Phase 0 (scaffold) complete: the harness runs green on a stub task.
Phase 1 (one hand-built faithful-reporting counterfactual pair + delta scorer)
is next. See the roadmap in [docs/brief.md](docs/brief.md) §9 and the running
decision log in [docs/design-notes.md](docs/design-notes.md).

## Layout

```
shendu/            # the eval package
  tasks.py         # Inspect @task definitions
  ...              # principles/, scenarios/, solver.py, scorer.py (Phase 1+)
tests/             # pairing invariant + scorer math tests
analysis/          # effect size, CIs, per-principle breakdown (Phase 2+)
docs/              # brief.md (design spec) + design-notes.md (decision log)
```
