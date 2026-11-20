## qc_video: DelhiRain6_EN_IG.mp4

**Overall: INCOMPLETE**

Coverage: format: short; duration_s: 121.07; fps: 30.0; scenes_sampled: 25; sheets: contact_sheet, first_3s, corners_captions, phone_size

| Check | Rule | Status | Detail |
|---|---|---|---|
| dimensions | QC-06 | PASS | 1080x1920 (short) |
| duration under 3:00 | FMT-01 | PASS | 121.07 s |
| black frames | QC-06 | PASS | none |
| freezes (holds over 1.5 s) | QC-06 | PASS | 1 freeze(s), all inside marked HOLDs |
| integrated loudness | ED-03 | PASS | -14.5 LUFS (target -14.0 ± 1.0) |
| true peak | ED-03 | PASS | -2.2 dBTP (max -1.0) |
| audio dropouts (silence over 2 s below -50 dB) | ED-03 | PASS | none |
| decode errors | QC-06 | PASS | 0 |
| frame 1 brightness | DIR-08 | PASS | mean 157.5/255 (min 60) |
| sharpness per scene | QC-06 | REVIEW | low scores {'45s': 41.4, '70s': 32.0, '85s': 50.1, '110s': 33.9} (median 298). Flat vector maps and diagrams score low by nature (known false positive); image scale is verified by check_assets |
| professional visual QC (12-item checklist, frame-level inspection) | QC-01 | NOT PERFORMED | human review required; use the sheets in the output folder |
