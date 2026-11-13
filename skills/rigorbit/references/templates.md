# Templates

Adapt the wording to the research area, but keep the fields. Agents start with no knowledge of the run, so a brief has to carry everything the agent needs. Thin briefs are the main reason delegated research comes back shallow.

Contents: [Agent brief](#agent-brief) · [Search report](#search-report) · [Proposal report](#proposal-report) · [Novelty breakdown file](#novelty-breakdown-file) · [Novelty audit](#novelty-audit) · [Candidate packet](#candidate-packet) · [Reviewer ballot](#reviewer-ballot) · [Feedback digest](#feedback-digest) · [Analysis plan](#analysis-plan) · [Run manifest](#run-manifest) · [Run record](#run-record)

## Agent brief

Use this frame for every delegated agent.

```text
ROLE: <role description, no credentials>   SEAT: <id>   ROUND: <n>
TASK: <one paragraph: what to produce and why it matters to the run>
SCOPE: <the agreed research scope, venue or audience, and constraints from brief.md>
YOUR REMIT: <the search angle, lens, candidate, or packet assigned to this seat>
INPUTS: <file paths to read. For reviewers, the packet only>
CARRIED FEEDBACK: <digest from earlier rounds, if any>
EVIDENCE RULES: open sources yourself; cite by title, authors, year, DOI or URL, and a
  pinpoint; mark each source full text, abstract only, or not opened; keep published
  findings, reproducibility evidence, and your own inference apart; never cite a source
  you could not find.
OUTPUT: write the full report to <path> in the format below, then reply with a summary
  of at most 150 words and the path.
WORK ALONE: do not look for or use other agents' drafts or votes from this round.
```

For reviewers, add: `A no vote is as useful to this run as a yes. Decide whether this version would hold up at <venue> as it stands.`

## Search report

```markdown
# S<nn> — <search angle>
## Searches run
Index or source, query, date range, number of results examined.
## Key papers
One entry per paper: source ID, what it did, dataset and split, metric, headline result,
access level, pinpoint.
## What existing methods achieve and where comparisons break down
## Gaps
For each: documented gap | open question | gap inferred under this bounded search.
Evidence for the gap, and the closest work that might already fill it.
## Conflicting findings
## What I could not check
```

## Proposal report

```markdown
# M<nn> — <candidate name>
Lens: <assigned lens, or "open seat">. If you left the lens, why.
## What I propose
## How it works
Enough detail that a coding agent could start: components, data flow, training or
inference procedure, key equations or pseudocode.
## Why it is worth testing
Expected benefit, the mechanism behind it, and what would have to be true.
## Closest prior work
The three to five nearest papers and the specific difference from each.
## Novelty table
| Part | Weight | Closest prior work | Novel? | Specific difference | Evidence |
## Novelty score
Output of the script on novelty/M<nn>.json, plus search limits and uncertainty.
## Fallback justification
Only for a score from 40% up to below 50%: designs tried to reach 50%, why each failed
under the constraints, and why this design is still worth testing.
## How to test it
Baselines, datasets, metrics, the minimum experiment that fits the user's compute, and
which outcome would count against the idea.
## Risks and reasons it might fail
## Status
eligible | needs fallback verification | ineligible | could not substantiate a candidate
```

## Novelty breakdown file

Saved as `novelty/M<nn>.json` by the author and `audit/M<nn>.json` by the auditor. Parts and weights follow the rubric fixed before the round. A part marked novel with any of the three text fields empty receives zero credit.

```json
{
  "candidate": "M07",
  "scored_by": "author",
  "fallback_verified": false,
  "parts": [
    {
      "name": "Budget-aware eviction policy",
      "weight": 2,
      "novel": true,
      "closest_prior_work": "S012",
      "difference": "Evicts by predicted reuse, where S012 evicts by recency",
      "evidence": "S012 section 3.2; no reuse-based policy in S012, S031, S044"
    },
    {
      "name": "Standard KV cache layout",
      "weight": 1,
      "novel": false,
      "closest_prior_work": "S003",
      "difference": "",
      "evidence": ""
    }
  ]
}
```

Set `fallback_verified` to true only after the ranking specialists have verified the fallback justification.

## Novelty audit

```markdown
# Audit of M<nn>-v<k>
## Searches run
## Part-by-part findings
| Part | Author's closest work | Closest work I found | Credit: stands / reduced / removed | Why |
## Audited score
Script output on audit/M<nn>.json, next to the author's score.
## Limits of this audit
```

## Candidate packet

The packet is the only thing a reviewer receives, and every reviewer on a panel receives the same one.

```markdown
# <candidate ID>-v<k> — <title>
Gate: problem | methodology | code and design | results
Venue and field: <from brief.md>
## Submission
The proposal, methodology, design, or results, in full.
## Evidence
Sources by ID with access level and pinpoints. For methodology: the author's novelty
table and the audit. For code: repository path, smoke-test record, analysis plan.
For results: provenance check, raw metrics location, analysis plan.
## Change log
Only for v2 onward: each carried issue and how it was fixed or why it was superseded.
## Review criteria
The rubric for this gate from the operating protocol.
```

Leave out the ranking, any other review, earlier vote counts, and any language arguing for approval.

## Reviewer ballot

The fields come first, one per line, exactly as shown. The script reads them.

```markdown
SEAT: 07
ROLE: statistics reviewer
CANDIDATE: P1
VERSION: v1
VOTE: no

## What I checked myself
Sources opened, files read, numbers recomputed.
## Strengths
## Strongest objection
Required even when voting yes.
## Other objections and requested changes
## Blocking conditions
Anything that must change before this could pass. If any are listed, the vote is no.
## Licensing, privacy, and misuse notes
## Confidence
High | medium | low, and what would change my vote.
```

`VOTE` is exactly `yes` or `no`. A conditional approval is a no.

## Feedback digest

```markdown
# Digest — <gate>, round <n>, <candidate IDs and versions>
Panel <size>, tallies per candidate.
## Issues, in priority order (at most ten)
For each: the issue, severity (fatal validity | major | minor), reviews that raised it
(seat IDs), where reviewers disagreed, proposed fix, affected versions, and the check
that will show it is resolved.
## What reviewers valued and should be kept
```

## Analysis plan

Written in Stage 3 and frozen before any results exist.

```markdown
# Analysis plan v<k> — frozen <date>
## Hypotheses
## Primary comparison and metric
## Success criteria
What result supports the idea, what weakens it, and what is inconclusive.
## Baselines, variants, and ablations
## Data, splits, and seeds
## Repeats and uncertainty
Number of runs, how variation is reported, and any statistical test with its threshold.
## Secondary and exploratory analyses
## Stopping and exclusion rules
```

A change after results are seen creates a new version, and everything it adds is exploratory.

## Run manifest

Each experiment run writes this as `manifest.json` in its output folder, and the results bundle includes it.

```json
{
  "code_version": "<git commit or content hash of the approved package>",
  "analysis_plan": "v1",
  "config": {},
  "seeds": [0, 1, 2],
  "environment": {"python": "", "packages": {}},
  "hardware": {"gpu": "", "memory_gb": 0},
  "started": "", "finished": "",
  "runs": [{"name": "", "status": "completed | failed", "metrics_file": "", "log_file": ""}]
}
```

Include failed runs. The results bundle is the manifest, the raw per-run metric files, the logs, and the generated summary tables.

## Run record

Close every user-facing report with this.

```markdown
## Run record
| Role | Planned | Completed | Replaced |
| Gate | Candidate and version | Panel | Yes | No | Needed | Decision |
Sources: <n> opened in full, <n> abstract only, <n> not opened; <n> second-checked.
Not verified: <claims or sources that could not be confirmed>.
Files: <path to reports, ballots, tallies>.
```
