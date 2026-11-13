---
name: rigorbit
description: Take a research topic from literature review to a novelty-checked methodology, a reproducible experiment, and a reviewed results report, using large teams of independent research agents and an independent reviewer panel with a 90% approval gate. Use when the user asks for Rigorbit or a research swarm, wants to find a research gap or paper idea grounded in the literature, wants a literature review that leads to a research proposal, wants a novel method or architecture designed and checked against prior work, wants an experiment built to test a research idea, or returns with results or a checkpoint from an earlier Rigorbit run. Not for a quick literature question or a summary of a single paper.
compatibility: Needs a host that can delegate work to independent subagents and can search and open scholarly sources. Stage 3 also needs a coding workspace. The bundled script needs Python 3.8 or later.
---

# Rigorbit

Run four stages in order: choose the problem, design the methodology, build the experiment, review the results. Each stage ends at a gate where an independent reviewer panel votes, and the user decides when to move from problem to methodology and from methodology to code. Honor the user's requested endpoint if they want only part of the workflow.

Rigorbit is worth its cost only if the independence is real and the record is honest. Many agents that share one context, or a tally nobody can trace back to written ballots, give the look of rigor without the substance. The rules below exist to protect those two things.

## Bundled files

- [references/operating-protocol.md](references/operating-protocol.md) covers team rules, evidence checks, novelty scoring, voting, and feedback. Read it before launching the first team of a run.
- [references/workspace.md](references/workspace.md) covers the run folder, the checkpoint, and the ledger. Read it when starting or resuming a run.
- [references/templates.md](references/templates.md) holds the briefs, report formats, ballot, and packet formats. Read the relevant template before writing a brief or a packet.
- `scripts/rigorbit_check.py` tallies a gate from the ballot files and computes a novelty score from a breakdown file. Use it for every tally and every score so the arithmetic is never done by hand.

All paths above are relative to this skill's folder.

## Start or resume

1. Look for an existing run folder or a checkpoint the user supplies. If one exists, read it, tell the user where the run stands (stage, round, open seats, last gate result), and continue from the latest verified point. Otherwise create the run folder described in the workspace reference.
2. Check that the host can do what the run needs: delegate to separate agents, search and open scholarly sources, and for Stage 3 run code. If it cannot delegate, tell the user and stop at what can honestly be done. Writing all the reports or ballots in one context is a single opinion repeated, so it does not count toward any team size or gate.
3. With each stage's intake questions, show the round plan: how many agents in which roles, how many waves the host's concurrency allows, and what that is likely to cost in time or usage if known. Rounds are large, and the user should start them knowingly. Agree a round budget for each gate, three rounds by default.

## Your role as orchestrator

Act as the clerk of the run. Assign work, keep the ledger, combine outputs by the stated rules, run the tallies, and report. Leave the research judgment to the teams: do not write candidates, vote, reword a review, or pick winners yourself, because the orchestrator has seen everything and is the least independent party in the run.

Ask every agent to write its full report to the run folder and return only a short summary with the file path. Work from the summaries and the ledger. This keeps your context free for coordination across dozens of agents and leaves a record the user can open.

Write briefs neutrally. Give agents the task, the evidence, and the criteria. Leave out what the user hopes for, how earlier votes went, and how close a tally is, since reviewers tend to drift toward whatever outcome they sense is wanted.

## 1. Choose the research problem

1. Turn the topic or brief into a focused intake. Ask a few relevant questions together about the intended contribution, target venue or audience, scope, and practical constraints. Use information the user already supplied. Set the search scope from the user's brief and answers.
2. Launch 21 or more independent literature-search agents per round. Assign complementary search angles with enough overlap to verify major claims. Collect one cited report per agent covering relevant papers, existing methods, results and benchmarks, comparison limits, evidence quality, and open gaps. Have three separate specialist agents each synthesize the evidence and shortlist the most promising problem proposals with reasons, closest prior work, feasibility, and likely contribution. Combine their shortlists by the rule in the protocol.
3. Before review, have agents who did not write the cited report open the sources that each shortlisted proposal's gap claim rests on. A gap claim is only as good as the search behind it, and invented or misread references are the most common failure in agent literature work. Drop or relabel anything that cannot be opened and confirmed.
4. Send each shortlisted proposal to the independent reviewer panel. Advance candidates that receive at least 90% yes votes. If none pass, distill the independent feedback through three separate feedback specialists, then search for genuinely different directions within the agreed scope and review a new shortlist.
5. Deliver a plain-language report with diagrams and concrete examples. Explain the problem, what existing work found, what remains open, what might be done, and why this problem earned a place on the shortlist. Include citations, the review outcome, and the run record. Answer follow-up questions. Start Stage 2 only when the user explicitly says to proceed. If multiple proposals pass and the user's choice is unclear, settle the choice before branching into methodology work.

## 2. Design a methodology

1. Ask a fresh set of relevant questions about the intended solution and constraints. Cover whether the user wants a new architecture, an add-on, an optimization, or another method, and which trade-offs or constraints matter most.
2. Set a shared novelty rubric before generation. Also set a spread of starting lenses, such as different approach families or different parts of the problem to attack, and give each agent one, keeping some seats open with no lens. Agents working from the same brief converge on the same few ideas, and the lenses are what make 51 seats produce more than a handful of distinct candidates. A lens is a starting point: an agent may leave it when the evidence leads elsewhere and should say why.
3. Launch 51 or more independent research agents per round. Each agent researches prior work, develops its own candidate, and writes a report covering what it proposes, how it works, why it is worth testing, what is new, and how to test it. Apply novelty to each individual candidate across its substantive technical contributions. Require at least 50% verified novelty where achievable. Allow a candidate with at least 40% and below 50% only when its agent documents credible attempts to reach 50% and why those attempts failed under the agreed constraints. The absolute minimum is 40%. See the protocol for the score, evidence, and eligibility rules.
4. Make the individual reports available to the user, including reports that could not substantiate an eligible candidate, marked with their status. Have seven separate specialist agents review eligible candidates, flag near-duplicates, and rank them on novelty, evidence quality, expected value, feasibility, and how decisively each idea can be tested. Combine their rankings by the rule in the protocol to select the top ten, or all eligible candidates when fewer qualify, and explain the ranking. If no candidates qualify, have the ranking specialists identify recurring deficiencies and carry those findings into a fresh generation round before convening reviewers.
5. Audit the novelty of each shortlisted candidate. An author scoring its own idea has every reason to miss the paper that already did it, so give each shortlisted candidate to a fresh agent whose only job is to find prior work that removes a credited part, then rescore. The audited score decides eligibility. If a candidate drops out, move the next-ranked eligible candidate up and audit it too.
6. Send each shortlisted methodology to the independent reviewer panel with the author's novelty table and the audit. Apply the 90% gate separately. If none pass, carry the distilled reviewer feedback into a fresh generation round. Present the approved methodologies in clear language with diagrams and examples. Explain what to build, the precise contribution and its evidence, what the experiment would test, and which outcomes would support or weaken the idea. Start Stage 3 only when the user explicitly says to proceed, with the selected methodology clear.

## 3. Build and review the experiment

1. Ask about available hardware and memory, wall-clock limits, budget, desired experimental depth, data or dependencies, and output format such as a Python project or Jupyter notebook. Record the constraints and match the design to them.
2. For rigorous experiments, have a separate research team design variants, appropriate baselines, ablations, metrics, and the evaluation protocol. Cover data splits, seeds, repeat runs, uncertainty, and reproducibility as appropriate. Write the primary comparisons, metrics, and success criteria into an analysis plan file and freeze it before any results exist. Stage 4 judges the results against this file, which is what separates a confirmed prediction from a story fitted afterwards.
3. Have specialist coding agents implement the complete experiment. Have each run write a manifest recording the code version, configuration, seeds, environment, and hardware, and include a step that gathers the manifest, raw metrics, and logs into one results bundle. Run feasible local smoke tests and record exactly what ran. Send the implementation, the experiment design, and the analysis plan to the independent panel. Apply the 90% gate to the combined submission. If it fails, revise the code or design using the distilled reviewer feedback and repeat review.
4. Deliver code with setup and run steps, expected outputs, relevant resource estimates, and the results bundle the user should return. Wait for the user to run the experiment and upload the results, unless they separately ask for execution and authorize the resources needed.

## 4. Review results and iterate

1. Check where the results came from before judging them. Confirm from the manifest that the uploaded run used the approved code version and configuration, and recompute the headline numbers from the raw metrics. Report any mismatch to the user and the panel. Ask for any missing evidence that materially affects review, such as raw metrics, run logs, settings, data splits, hardware, seeds, failed runs, and code or experiment version.
2. Have the independent panel assess the evidence, evaluation quality, and conclusions against the approved experiment and the frozen analysis plan. Apply the 90% gate.
3. If it fails, use the distilled feedback to request any missing evidence and route experimental or implementation issues to the research and coding teams. Trace changes to the reported deficiencies. Preserve prior runs and distinguish changes made after seeing results from the original confirmatory plan. Send revised code and design through Stage 3 review before delivering a new version for the user to rerun. Repeat results review when the new evidence arrives.
4. On approval, deliver a cited or artifact-linked account of the results, supported claims, uncertainties, and limitations. Accept well-supported negative or inconclusive conclusions when warranted by the evidence.

## When a gate keeps failing

A failed gate stays open for another round while the round budget allows. When the budget is used up without a pass, stop and show the user the closest candidates, the objections that kept recurring, and the choices: fund another round, narrow or change the scope, relax a constraint, or close the stage with a documented no-go. A no-go backed by 21 written reviews is a useful result, and it is better than spending without limit or lowering the bar to get a pass.

## What every user-facing report carries

End each stage report with the run record: actual agent counts by role, panel size, vote count and decision for each candidate with its version, how many sources were opened in full versus abstract only, anything that could not be verified, and where the individual reports and ballots are stored. The user is trusting the process, so show them the process that actually ran.
