## qc_video: DelhiRain5_EN_IG.mp4

**Overall: INCOMPLETE**

Coverage: format: short; duration_s: 102.79; fps: 30.0; scenes_sampled: 21; sheets: contact_sheet, first_3s, corners_captions, phone_size

| Check | Rule | Status | Detail |
|---|---|---|---|
| dimensions | QC-06 | PASS | 1080x1920 (short) |
| duration under 3:00 | FMT-01 | PASS | 102.79 s |
| black frames | QC-06 | PASS | none |
| freezes (holds over 1.5 s) | QC-06 | PASS | 4 freeze(s), all inside marked HOLDs |
| integrated loudness | ED-03 | PASS | -14.0 LUFS (target -14.0 ± 1.0) |
| true peak | ED-03 | PASS | -1.9 dBTP (max -1.0) |
| audio dropouts (silence over 2 s below -50 dB) | ED-03 | PASS | none |
| decode errors | QC-06 | PASS | 0 |
| frame 1 brightness | DIR-08 | PASS | mean 133.5/255 (min 60) |
| loop seam (first vs actual final frame) | FMT-06 | PASS | mean difference 0.77 (max 3.0); final frame = decoded frame 20 of the last 0.5 s |
| loop transition (last 0.5 s, frame to frame) | FMT-06 | PASS | largest frame-to-frame change 0.2 (max 25; a hard cut is typically 40+), about 0.33 s before the end |
| sharpness per scene | QC-06 | REVIEW | low scores {'65s': 113.0} (median 508). Flat vector maps and diagrams score low by nature (known false positive); image scale is verified by check_assets |
| professional visual QC (12-item checklist, frame-level inspection) | QC-01 | NOT PERFORMED | human review required; use the sheets in the output folder |
