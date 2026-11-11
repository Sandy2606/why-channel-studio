# QC report: <title> (<date>)

Files, durations, encoding.

## Checks (→ QC-04: never report an unperformed check as passed)
| Check | Rule | Performed? (yes / no / n/a) | Method (script / frame review / listening) | Result |
|---|---|---|---|---|
| Duration under 3:00 | FMT-01 | | | |
| Loudness, true peak | ED-03 | | | |
| Black frames, freezes (HOLDs exempt) | QC-06 | | | |
| Decode errors, loop seam, frame-1 brightness | QC-06 | | | |
| Sharpness and image scale | QC-06, LAY-05 | | | |
| Automated layout (EN and TE) | QC-05 | | | |
| Visual checklist, 12 items | QC-01 | | | |
| Frame-level inspection and phone size | QC-01 | | | |
| Facts, numbers and labels on screen | RS-03, ART-02 | | | |
| Four exports, same body | FMT-09 | | | |
| Post-copy counts and verification date | PUB-02 | | | |
| Story and composition (human) | QC-04 | | | |
| Listening: headphones and phone speaker (human) | QC-04 | | | |
| Telugu naturalness (human) | QC-04 | | | |

## Defect log (→ QC-02)
| # | Found at (brief / script / scene sheet / preview / render) | Severity | Defect | Fix | Status |
|---|---|---|---|---|---|

## Human review
Record human checks in `qc_signoff.md` (same folder) and combine everything with `pipeline/qc/qc_summary.py`. The summary stays INCOMPLETE until every human row is signed with a reviewer and a date.

## Score (→ QC-03; a target, not a substitute for the gate)
