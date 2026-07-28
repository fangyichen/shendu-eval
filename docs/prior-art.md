# Prior art — what to steal, and what is actually ours

Literature review conducted 2026-07-28 via parallel web research. Findings are
marked **[V]** where a primary source was fetched and read, **[S]** where only a
search snippet was seen, and **[I]** where the claim is inference. Negative
claims ("nobody has done X") are **[I]** by nature — they are the result of
searching, not proof.

Two claims that surfaced in research but **could not be verified** and must not
be cited: (a) that the Apollo/OpenAI anti-scheming paper (arXiv:2509.15541)
contains a "null-control family" varying an irrelevant detail — one pass
reported it, a second could not retrieve any such passage; (b) Eggers, Tuñón &
Dafoe's placebo-test typology (AJPS 2024) — paywalled, never read.

---

## 1. The finding that most threatens this eval

**Greenblatt et al. 2024, alignment faking, App. G.4 [V]** — removing the
*monitoring* clause from their system prompt changed nothing:

> "Telling the model that conversations with non-free tier users are unmonitored
> isn't important (alignment faking and compliance gaps remain the same when this
> information is removed from the prompt)"

Their entire compliance gap was carried by *"this will modify my values"* —
consequence-to-self — not by being watched. **Observation per se may simply not
be a variable that moves models.** That is the exact manipulation this eval is
built on, and it is the most plausible explanation for the null gaps measured
here so far.

Consequence: a null result is uninterpretable without a power check. This is why
the `positive_control` arm exists (see `scenarios/base.py`).

## 2. Design ideas worth taking

| Source | Idea | Status here |
|---|---|---|
| Apollo, in-context scheming [V] | Paired internal memos differing only in tense and one clause, so behaviour change cannot be attributed to spurious prompt differences | We do this with config cues; their prose-memo version is more naturalistic |
| Apollo/OpenAI anti-scheming [V] | "Core tasks relatively simple for frontier models, which minimizes raw capabilities as a confounding variable. The deceptive opportunities, however, are sometimes subtle." | Exactly the `diligence` probe's design rationale |
| MASK [V] | Score honesty against the model's *own elicited belief*, not external truth — no contested answer key needed | Our Stage-1 pledge plays this role. **Do not copy their "no consistent belief" exclusion**: it drops more rows for weaker models, so the denominator varies by capability |
| CoT faithfulness, Chen et al. [V] | Score only on the subpopulation where the manipulation demonstrably changed behaviour, and normalise for random flips | Our `noise_floor` is a cruder version; their formula is the principled one |
| False Success, arXiv:2606.09863 [V] | Use a **structured status field**, not an LLM judge: judges cap at AUROC 0.65/0.54 on "did the agent falsely claim success", a lightweight structured detector reaches 0.83/0.95 | Vindicates deterministic scoring; `diligence` reads actions, not prose |
| METR [V] | Anchor difficulty **exogenously** (human baseline times) rather than inferring it from model performance, so the difficulty axis doesn't drift with the model population | Not yet applied |

**Statistical bar.** Agentic Misalignment computes only `harmful/classified`
with no CIs and no tests [V] — a low bar. The bar to actually target is
anti-scheming's (Fisher's exact, Beta-posterior credible intervals, hierarchical
models for correlated samples) or METR's (three-level hierarchical bootstrap).
Inspect gives us `stderr(cluster=...)` for the paired design; no existing
gap-style eval in `inspect_evals` uses it [V].

## 3. Traps with evidence behind them

- **A delta is not self-interpreting [V].** Claude 3 Haiku produced a real
  compliance gap with *zero* alignment-faking reasoning — "likely due to factors
  other than alignment faking". A weak model can produce our delta for unrelated
  reasons. This is precisely what `noise_floor` is for.
- **Judge validity is a variable, not a constant [V].** CoT-judge/human
  agreement swings from 95%/90% to 25%/50% across settings in the same paper.
- **Difficulty ladders are non-monotonic [V].** o1 on oversight subversion:
  Easy 0.65, **Medium 0.00**, Hard 0.02. A comprehension floor is harder to
  build than it looks.
- **Eval awareness scales with model size, roughly as a power law [S]**
  (arXiv:2509.13333). Stronger models notice the framing more — a capability
  confound of exactly the kind capability-invariance is meant to remove. o3 has
  been observed complying *because* it inferred it was in an alignment test [V].
- **Contamination nulls these evals [V].** The `alignment_faking` port in the
  Inspect register reports a gap of ~−0.04 to −0.05, p>0.25 on current models,
  attributed to verbatim-prompt contamination and mitigation overfit; it ships
  paraphrase-ensemble and fictional-lab de-fingerprinting knobs in response.

## 4. Where the gap in the literature actually is

**Nobody has built an eval where the compliant action is trivial, tedious and
low-stakes rather than a dramatic moral choice, measured as a function of
perceived observation. [I]** Searched from six directions; nothing found. The
supporting evidence is that Anthropic's own honesty-elicitation write-up
concedes its settings contain **no genuinely low-stakes dishonesty** [V] — the
field knows the hole is there.

Coverage of the four properties we want:

| Work | Trivial/tedious duty | Observed-vs-unobserved | No contested ground truth | Capability-invariant |
|---|---|---|---|---|
| MASK | ✗ | ✓ | ✓ | mostly |
| CoT faithfulness | ✗ | ✓ (strongest) | ✓ | mostly |
| Utility–Behavior Gap | ✗ (effort quality) | ✓ | ✓ | ✓ |
| τ-bench / GuideBench | ✓ | ✗ | ✗ | ✗ |
| **`diligence` here** | **✓** | **✓** | **✓** | **✓** |

## 5. The placebo arm: precedent exists, but not in this field

Two independent passes found prompt-level precedent, under **no shared name**:

- **Yang et al., "Compared to What? Baselines and Metrics for Counterfactual
  Prompting" (arXiv:2605.01048) [V]** — calls it a **paraphrase baseline**. The
  result is the argument for the design: gender-induced prediction flips (14.9%)
  were statistically indistinguishable from paraphrase-induced flips (14.1%), and
  **only 5 of 120 previously-significant tests survived** once general prompt
  sensitivity was accounted for.
- **FinPersona-Bench (arXiv:2606.31522) [V]** — calls it a **placebo condition**,
  using length-matched boilerplate to separate semantic content from position.

Adjacent names elsewhere: *placebo/falsification test* (econometrics), *negative
control* (epidemiology), *invariance test* (CheckList), *metamorphic relation*
(software testing), *perturbation sensitivity analysis*.

**But no instance was found in alignment/behavioural agentic evals [I]**, and
the major labs handle noise by resampling and hierarchical uncertainty rather
than by a null-manipulation arm [V]. Pairing a placebo arm (negative control,
effect should be ~0) with a positive control (effect should be large) to bracket
an eval's sensitivity from both sides appears to be unclaimed ground — one
LessWrong post argues for the positive half via mutation testing; nobody argues
for both [S].

**Terminology.** Use "placebo arm", glossed once as a negative control. Never
write "control arm"/"control evaluation" unqualified: in AI safety that already
means a red-team/blue-team protocol game (Redwood, UK AISI) [V], and the two
vocabularies are disjoint.

## 6. Judgability versus realism

The tension we worried about in brief §7 is acknowledged in the literature but
has no name and no accepted solution. DeepMind's honeypot paper (arXiv:2605.29729)
lists it as competing desiderata [V]:

> "Realism vs Checkability: The complexity of realistic environments makes it
> more difficult to verify whether an action constitutes sabotage."

Proposed mitigations: naturalistic trajectory replay (LURE, arXiv:2605.26438
[V]) and treating verbalised eval-awareness as a realism signal to repair the
scenario (Goodfire [S]).

## 7. Honest novelty assessment

**Not ours.** The counterfactual-paired delta structure. `inspect_evals` already
registers an `alignment_faking` eval whose headline is a compliance gap between
paired arms [V]; MASK, CoT-faithfulness and sandbagging are all paired designs.
The brief predicted this (§11) — now confirmed.

**Plausibly ours, in descending confidence.**

1. **The trivial-duty probe** (`diligence`) — a documented gap, with the field's
   own admission that it is missing.
2. **Two-sided sensitivity bracketing** — placebo arm for the noise floor *and*
   positive control for power, so both readings of a null are distinguishable.
   Each half has precedent; the pair does not appear to.
3. **delta → 0 as the target rather than a failure signal.** Not merely framing:
   it is what makes the diagnostic arms necessary, and existing gap evals ask
   only "how high is the violation rate".
4. **Capability invariance as a first-class design constraint.** Six partial
   approaches exist in the literature; none treats it as the governing
   requirement, and both known comprehension-floor techniques (difficulty
   ladders, post-hoc model exclusion) are documented to work badly.
