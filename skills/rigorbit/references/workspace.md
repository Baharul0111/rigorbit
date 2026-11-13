# Run Workspace

Every run lives in one folder. Reports, ballots, and the checkpoint are files, so a run can pause, resume in a new session, and be inspected by the user. Create the folder in the user's project or working directory and tell them where it is.

## Layout

```text
rigorbit-runs/<run-slug>/
├── checkpoint.json          current state of the run
├── ledger.jsonl             one line per agent seat
├── sources.jsonl            one line per source
├── brief.md                 agreed scope, constraints, venue, round budgets
├── stage1/
│   └── round-1/
│       ├── assignments.md   search angles per seat
│       ├── reports/         S01.md ... one per search agent
│       ├── synthesis/       Y1.md Y2.md Y3.md
│       ├── shortlist.md     combined shortlist and the rule applied
│       ├── packets/         P1-v1.md ... what reviewers receive
│       ├── reviews/P1-v1/   seat-01.md ... one ballot per seat
│       ├── tally/           P1-v1.json  script output
│       └── feedback/        F1.md F2.md F3.md digest.md
├── stage2/
│   └── round-1/
│       ├── rubric.md        novelty rubric, fixed before launch
│       ├── assignments.md   lens per seat
│       ├── reports/         M01.md ... one per proposal agent
│       ├── novelty/         M01.json ... author breakdowns
│       ├── ranking/         R1.md ... R7.md and combined.md
│       ├── audit/           M07.md and M07.json per shortlisted candidate
│       ├── packets/  reviews/  tally/  feedback/
├── stage3/
│   ├── constraints.md
│   ├── analysis-plan-v1.md  frozen before any results exist
│   ├── design/              experiment design reports
│   ├── code/                the experiment package
│   ├── smoke-tests.md       exactly what ran locally and what it showed
│   └── round-1/             packets/ reviews/ tally/ feedback/
├── stage4/
│   ├── uploads/run-1/       the user's results bundle, untouched
│   ├── provenance-run-1.md  manifest check and recomputed headline numbers
│   └── round-1/             packets/ reviews/ tally/ feedback/
└── deliverables/            the reports given to the user
```

Start a new `round-N` folder for each failed gate round and never overwrite an earlier one. Earlier rounds are the evidence that feedback was addressed.

## Naming

- Seats: `S01` search, `Y1` synthesis, `M01` proposal, `R1` ranking, `A-M07` novelty audit, `seat-01` reviewer, `F1` feedback.
- Candidates keep their ID for the whole run. Add a version suffix whenever content changes: `P1-v1`, `P1-v2`.
- A packet is immutable once any reviewer has received it. A change means a new version and a new panel.

## checkpoint.json

Update it after every wave and every gate decision.

```json
{
  "run": "long-context-memory",
  "updated": "2026-11-13T07:30:00+05:30",
  "stage": 2,
  "round": 1,
  "status": "pending",
  "waiting_on": "18 of 51 proposal seats still open",
  "user_gates": {"stage2_go_ahead": true, "stage3_go_ahead": false},
  "round_budget": {"problem": 3, "methodology": 3, "code": 3, "results": 3},
  "rounds_used": {"problem": 1, "methodology": 0, "code": 0, "results": 0},
  "selected": {"problem": "P2-v1", "methodology": null},
  "gates": [
    {"gate": "problem", "round": 1, "candidate": "P2-v1", "panel": 21, "yes": 20, "no": 1, "decision": "pass"}
  ],
  "teams": {
    "stage2_proposal": {"planned": 51, "complete": 33, "open": 18}
  },
  "next_action": "launch wave 4 with seats M34 to M51"
}
```

`status` is one of `in_progress`, `pending` (work remains that the host can do), `waiting_for_user`, or `closed`.

## ledger.jsonl

One line per seat, appended when the seat is assigned and updated when it finishes. This is what the run record at the end of each report is built from.

```json
{"seat": "M07", "role": "proposal", "stage": 2, "round": 1, "lens": "drop the full-attention assumption", "input_version": "brief-v2", "status": "complete", "output": "stage2/round-1/reports/M07.md", "replaced_by": null}
```

`status` is `assigned`, `complete`, `incomplete`, or `replaced`. Only `complete` seats count toward a team size.

## sources.jsonl

One line per source, shared by all stages.

```json
{"id": "S012", "title": "…", "authors": "…", "year": 2025, "venue": "…", "doi_or_url": "…", "published": true, "access": "full_text", "first_cited_by": "S04", "checked_by": ["S04", "Y2"]}
```

`access` is `full_text`, `abstract_only`, or `not_opened`. A source counts as second-checked when `checked_by` includes an agent other than `first_cited_by`.
