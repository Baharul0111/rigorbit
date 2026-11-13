#!/usr/bin/env python3
"""Deterministic checks for a Rigorbit run. Standard library only.

  rigorbit_check.py gate <ballots_dir> --panel N
      Tally one candidate's ballots against the 90% gate.

  rigorbit_check.py novelty <breakdown.json>
      Compute a candidate's novelty score and eligibility band.

Exit codes: 0 = pass / eligible, 1 = fail / ineligible,
            2 = pending or needs a verified fallback, 3 = bad input.
"""

import argparse
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

MIN_PANEL = 21
FIELD = re.compile(r"^\s*([A-Za-z_]+)\s*:\s*(.*?)\s*$")


def threshold(panel):
    """Smallest whole number of yes votes that is at least 90% of the panel."""
    return -(-9 * panel // 10)


def read_header(path):
    """Read the KEY: value lines that open a ballot.

    Reading stops at the first heading after the fields, so a line such as
    "VOTE: no" quoted in the written reasoning is never counted.
    """
    fields = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.lstrip().startswith("#"):
            if fields:
                break
            continue
        match = FIELD.match(line)
        if match:
            fields.setdefault(match.group(1).upper(), match.group(2))
    return fields


def cmd_gate(args):
    folder = Path(args.ballots_dir)
    if not folder.is_dir():
        print(json.dumps({"error": "not a folder: %s" % folder}))
        return 3
    if args.panel < 1:
        print(json.dumps({"error": "--panel must be a positive number"}))
        return 3

    yes, no, invalid, seats, versions, candidates = [], [], [], {}, set(), set()
    for path in sorted(folder.glob("*.md")):
        header = read_header(path)
        vote = header.get("VOTE", "").strip().lower()
        seat = header.get("SEAT", "").strip()
        problems = []
        if vote not in ("yes", "no"):
            problems.append("VOTE must be exactly yes or no")
        if not seat:
            problems.append("SEAT is missing")
        elif seat in seats:
            problems.append("SEAT %s already used by %s" % (seat, seats[seat]))
        if problems:
            invalid.append({"file": path.name, "problems": problems})
            continue
        seats[seat] = path.name
        if header.get("VERSION"):
            versions.add(header["VERSION"])
        if header.get("CANDIDATE"):
            candidates.add(header["CANDIDATE"])
        (yes if vote == "yes" else no).append(path.name)

    counted = len(yes) + len(no)
    needed = threshold(args.panel)
    warnings = []
    if args.panel < MIN_PANEL:
        warnings.append("panel of %d is below the Rigorbit minimum of %d" % (args.panel, MIN_PANEL))
    if len(versions) > 1:
        warnings.append("ballots cover more than one version: %s" % sorted(versions))
    if len(candidates) > 1:
        warnings.append("ballots cover more than one candidate: %s" % sorted(candidates))

    if counted > args.panel:
        decision, code = "error", 3
        warnings.append("%d valid ballots for a panel of %d; the panel size is fixed before launch" % (counted, args.panel))
    elif len(versions) > 1 or len(candidates) > 1:
        decision, code = "error", 3
    elif counted < args.panel:
        decision, code = "pending", 2
    elif len(yes) >= needed:
        decision, code = "pass", 0
    else:
        decision, code = "fail", 1

    print(json.dumps({
        "decision": decision,
        "panel": args.panel,
        "yes": len(yes),
        "no": len(no),
        "yes_needed": needed,
        "open_seats": max(args.panel - counted, 0),
        "candidate": sorted(candidates)[0] if len(candidates) == 1 else None,
        "version": sorted(versions)[0] if len(versions) == 1 else None,
        "invalid_ballots": invalid,
        "warnings": warnings,
    }, indent=2))
    return code


def as_fraction(value):
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise ValueError("weight must be a number")
    weight = Fraction(str(value))
    if weight <= 0:
        raise ValueError("weight must be greater than zero")
    return weight


def cmd_novelty(args):
    try:
        data = json.loads(Path(args.breakdown).read_text(encoding="utf-8"))
        parts = data["parts"]
        if not isinstance(parts, list) or not parts:
            raise ValueError("parts must be a non-empty list")
        total = Fraction(0)
        credited = Fraction(0)
        uncredited_claims = []
        for index, part in enumerate(parts, 1):
            name = part.get("name") or "part %d" % index
            weight = as_fraction(part.get("weight", 1))
            total += weight
            if part.get("novel") is True:
                supported = all(str(part.get(key) or "").strip() for key in ("closest_prior_work", "difference", "evidence"))
                if supported:
                    credited += weight
                else:
                    uncredited_claims.append(name)
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        print(json.dumps({"error": "cannot read breakdown: %s" % error}))
        return 3

    score = credited / total * 100
    fallback_verified = data.get("fallback_verified") is True
    if score >= 50:
        status, code = "eligible", 0
    elif score >= 40:
        if fallback_verified:
            status, code = "eligible with verified fallback", 0
        else:
            status, code = "needs verified fallback justification", 2
    else:
        status, code = "ineligible", 1

    print(json.dumps({
        "candidate": data.get("candidate"),
        "scored_by": data.get("scored_by"),
        "score_percent": round(float(score), 4),
        "score_exact": "%d/%d" % (score.numerator, score.denominator),
        "status": status,
        "credited_weight": float(credited),
        "total_weight": float(total),
        "parts": len(parts),
        "claims_given_zero_credit_for_missing_evidence": uncredited_claims,
    }, indent=2))
    return code


def main():
    parser = argparse.ArgumentParser(description="Deterministic checks for a Rigorbit run.")
    commands = parser.add_subparsers(dest="command", required=True)

    gate = commands.add_parser("gate", help="tally one candidate's ballots against the 90%% gate")
    gate.add_argument("ballots_dir", help="folder holding one .md ballot per reviewer seat")
    gate.add_argument("--panel", type=int, required=True, help="panel size fixed before launch")
    gate.set_defaults(run=cmd_gate)

    novelty = commands.add_parser("novelty", help="compute a novelty score from a breakdown file")
    novelty.add_argument("breakdown", help="JSON breakdown file for one candidate")
    novelty.set_defaults(run=cmd_novelty)

    args = parser.parse_args()
    return args.run(args)


if __name__ == "__main__":
    sys.exit(main())
