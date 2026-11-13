# Operating Protocol

Contents: [Run independent teams](#run-independent-teams) · [Combine specialist outputs](#combine-specialist-outputs) · [Verify evidence](#verify-evidence) · [Score novelty per candidate](#score-novelty-per-candidate) · [Audit novelty](#audit-novelty) · [Review and vote](#review-and-vote) · [Hand off after a failed gate](#hand-off-after-a-failed-gate) · [Repeat experiments](#repeat-experiments)

## Run independent teams

**Team sizes.** Use actual delegated agents. Set the round's team sizes and assignments before launching.

| Role | Size |
| --- | --- |
| Stage 1 literature-search agents | at least 21 per round |
| Stage 1 synthesis specialists | exactly 3 |
| Source checkers | as many as the shortlist needs, none of them the first citer |
| Stage 2 proposal agents | at least 51 per round |
| Stage 2 ranking specialists | exactly 7 |
| Stage 2 novelty auditors | 1 fresh agent per shortlisted candidate |
| Reviewers | at least 21 for every gate |
| Feedback specialists | exactly 3 for each failed gate round |
| Research-design and coding specialists | as the experiment needs |

**Waves and seats.** Run in waves up to the available concurrency. Release completed agents and create separate fresh agent instances for outstanding assignments. Keep the role, agent identity, round, input version, and output status in the ledger. Count each real, complete contribution once.

**Separation.** Use fresh review sessions, and keep reviewers separate from the agents who generated, selected, audited, designed, coded, or summarized feedback for the submission they review. An agent that has argued for a piece of work cannot judge it fairly.

**What each agent sees.** Give each search or proposal agent the common brief, its remit or lens, relevant constraints, and any distilled feedback from prior rounds. Withhold current-round peer drafts and votes, since agents that read each other's drafts converge and the team stops being independent. Give selectors the original reports and their citations. Give every reviewer the same versioned candidate packet and review criteria. Withhold the selectors' ranking, other reviewers' opinions, earlier vote counts, and the live tally until votes are submitted.

**Lenses.** Before a Stage 2 round, write the list of starting lenses and assign one per seat, leaving roughly one seat in five open. Draw the lenses from the Stage 1 evidence: different approach families, different bottlenecks to attack, different assumptions to drop. In a later round, add lenses that respond to the distilled feedback and retire lenses that produced only ineligible candidates.

**Incomplete work.** If an agent returns incomplete work or fails to respond, retry the assignment or replace it with a fresh agent before counting that seat. If tooling, time, or the available execution window prevents the required panel or workforce from finishing, report actual counts and save the checkpoint as pending. Resume remaining seats when possible. Advance only after the required work and gate are complete.

**Roles, not credentials.** Use role descriptions such as senior methods reviewer or venue-style reviewer without claiming real affiliations, credentials, or years of experience.

**Checkpoint.** Keep a checkpoint with the agreed scope, user gates, round budget, current stage and round, evidence and source identifiers, candidate and code versions, report locations, panel assignments, vote counts, and feedback handoff. Reuse this record across waves and resumptions. See [workspace.md](workspace.md) for the layout.

**Round budget.** Keep a failed gate open for another round while work is executable within the user's constraints and the agreed round budget. When the budget is spent, or progress requires new user input, resources, access, or a material scope change, show the pending state and the decision needed.

## Combine specialist outputs

Specialists work separately and the orchestrator combines their outputs by fixed rules, so the result does not depend on the orchestrator's own taste.

- **Stage 1 synthesis.** Each of the three specialists produces its own shortlist. A proposal named by at least two of them goes on the shortlist. List proposals named by only one as also considered, with the reason given.
- **Stage 2 duplicates.** Each ranking specialist flags pairs of candidates whose core mechanism is the same under different names. Merge a pair when at least four of the seven flag it. Keep the better-evidenced candidate as the representative and list the other as a supporting report. A merged group takes one place in the top ten.
- **Stage 2 ranking.** Each ranking specialist ranks the eligible candidates independently with written reasons. Order candidates by mean rank and break ties by evidence quality. Record where the specialists disagreed strongly, since reviewers and the user should know which picks were contested.
- **Feedback.** Each feedback specialist drafts its own list of issues from the reviews. Merge the lists, put issues raised by two or more specialists first, and order the rest by how many reviews raised them.

## Verify evidence

- **Search.** Search relevant scholarly indexes and primary sources. Start with published papers and use accessible author manuscripts or preprints when relevant, clearly marking publication and verification status. Record search terms, sources searched, relevant dates, and the closest competing work.
- **Read the paper.** Check actual paper content for claims where accessible. Label abstract-only or unavailable evidence and limit claims accordingly.
- **Cite precisely.** For consequential claims, preserve paper title, author, year, stable DOI or URL, and a pinpoint such as a page, table, figure, or section when available. Confirm that the citation supports the exact claim. Record dataset, split, metric, baseline, and compute or evaluation setting when they affect a result. Separate published findings, reproducibility evidence, and your inference.
- **Keep a source ledger.** Give every source an ID and record whether it was opened in full, seen as an abstract only, or not opened, and which agent checked it. Reports cite sources by ID so one paper is not counted as several.
- **Second check.** Before a proposal or candidate advances, have an agent other than the one that first cited them open the sources its central claims rest on. Treat a reference that cannot be found or opened as if it does not exist: remove the claim, or keep it clearly marked as unverified and outside the argument. Agents sometimes produce references that look real and are not, and one of these in a gap claim invalidates the stage.
- **Classify gaps.** In each report, distinguish a documented gap from an open question or a gap inferred under a bounded search. Retain credible competing work and conflicting findings.
- **Stay traceable.** Provide plain-language explanations while preserving traceability to source reports, reviewer votes, and primary evidence.

## Score novelty per candidate

1. **Fix the rubric first.** Before the Stage 2 generation round, define what counts as a substantive part of a candidate in this research area, with consistent weights or equal weights. Choose meaningful technical units such as an architecture mechanism, an integration mechanism, an optimization strategy, or a materially new experiment design. Score the technical proposal, including essential reused parts at the same granularity. Omit boilerplate and incidental details. Keep the rubric and normalization consistent across comparable candidates and rounds. Record any necessary rubric change and rescore affected candidates before comparison.
2. **Map every part to prior work.** Ask each agent to map every scored part to the closest verified prior work. Record its weight, whether it earns novelty credit, the specific difference, and the evidence. Credit a combination when the interaction mechanism or capability is itself substantively new and the evidence supports the distinction. Count it once. Give zero credit to reused, cosmetic, or unverified elements. Favor substantive differences over splitting a small change into several entries.
3. **Compute the score.** The percentage is the total weight of evidence-supported novel parts divided by the total weight of substantive parts, multiplied by 100. Save the breakdown in the format given in [templates.md](templates.md) and compute it with the script, which uses the unrounded value for eligibility:

   ```sh
   python scripts/rigorbit_check.py novelty path/to/M07.json
   ```

   Treat the percentage as an estimate under the documented search and rubric. Publish the breakdown, search limits, and meaningful uncertainty.
4. **Apply the thresholds.** Assess each candidate individually at the same threshold.

   | Score | Status |
   | --- | --- |
   | 50% or higher | Eligible on novelty. |
   | 40% up to but below 50% | Eligible only with a verified fallback justification. |
   | Below 40%, missing justification, or inadequate evidence | Ineligible. |

   For the fallback, require the candidate's author to document why a reasonable search for a 50% design failed under the agreed constraints, the nearest alternatives examined, and why the lower-scoring design remains worthwhile. Have the ranking specialists verify the fallback before shortlisting and the reviewer panel verify it at the gate. Record the individual report even if its candidate is ineligible. Keep new rounds focused on defensible directions when the pool is thin.

## Audit novelty

The author's score is a claim. The audit tests it.

- Give each shortlisted candidate to a fresh agent that did not propose, rank, or review it. Its task is to search for prior work that already contains each credited part or the credited combination, concentrating on the parts carrying the most weight.
- The auditor records the searches it ran, the closest work it found for each part, and whether the credit stands, is reduced, or is removed. It produces a revised breakdown file, and the script computes the audited score.
- The audited score decides eligibility and is the score shown to reviewers and the user. Show the author's score alongside it and explain any difference.
- If the audit moves a candidate below its threshold, remove it from the shortlist, promote the next-ranked eligible candidate, and audit that one as well.
- An audit that finds nothing is still a bounded search. Report it as "no closer prior work found under these searches".

## Review and vote

**Panel makeup.** Review with the declared venue and field in mind. Set the seats before launch with complementary specialties such as domain knowledge, methods, statistics, reproducibility, compute or systems, and practical value. At the methodology gate, give at least three seats to prior-art checking.

**Gate rubrics.** Keep the panel rubric specific to the gate.

| Gate | What reviewers check |
| --- | --- |
| Problem | The evidence for the gap and the value of studying it. |
| Methodology | Novelty including the audit, feasibility, and testability. |
| Code and design | Implementation correctness, reproducibility, evaluation validity, and whether the analysis plan is fixed and sufficient. |
| Results | The evidence, robustness, agreement with the analysis plan, and whether the conclusions follow. |

At every gate, reviewers also note data licensing or access problems, privacy or human-subjects issues, and clear misuse risk. These block approval when they would prevent publication or responsible use at the declared venue.

**Each reviewer checks for itself.** Ask each reviewer to open the sources or files its judgment rests on instead of trusting the packet's summary, and to list what it checked. A panel that only reads the packet can only measure how persuasive the packet is.

**The ballot.** Require a yes or no vote with written reasoning from each reviewer for each candidate or submission, using the ballot format in [templates.md](templates.md). Ask for evidence, strengths, the strongest objection even from a reviewer voting yes, requested changes, and any conditions that block approval. A yes means the current version meets that gate. Count an approval that depends on a future fix as a no for the current version.

**Incomplete ballots.** A ballot with no clear vote, or with reasoning that never refers to specifics of the packet, is incomplete. Give that seat to a fresh agent. Do not send a ballot back to the same reviewer for a different answer, and do not edit ballots.

**The tally.** Complete the panel before tallying. A gate passes only when yes votes are greater than or equal to the ceiling of 0.90 times the panel size, applied separately to each candidate.

| Panel size | Yes votes needed |
| --- | --- |
| 21 | 19 |
| 25 | 23 |
| 30 | 27 |

Run the tally with the script, which reads the ballot files, reports missing or invalid seats, and returns pass, fail, or pending:

```sh
python scripts/rigorbit_check.py gate path/to/ballots --panel 21
```

Report the panel size, vote count, decision, and version.

## Hand off after a failed gate

- Retain each reviewer's written report.
- Have three distinct feedback specialists read the reports, merge duplicate findings, and select up to ten high-impact actionable comments. If fewer than ten distinct actionable issues exist, report those.
- Preserve links to originating reviews, note disagreement, and surface fatal validity issues ahead of cosmetic requests.
- Carry the ordered list, proposed fixes, affected versions, and success checks to the next team.
- Give the next version's packet a change log that answers each carried issue: fixed and how, or superseded by a different direction and why. Reviewers of the new version see the change log, not the earlier vote counts.

## Repeat experiments

For repeat experiments, keep original results and preregistered or agreed metrics visible. Mark post-result changes as exploratory and use fresh held-out evidence or an appropriate independent repeat when making new confirmatory claims. Evaluate outcome quality by the strength of the evidence and the accuracy of the claims.
