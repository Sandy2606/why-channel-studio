## check_exports: DelhiRain4

**Overall: PASS**

Coverage: expected: 4; found: 4

| Check | Rule | Status | Detail |
|---|---|---|---|
| DelhiRain4_EN_YT.mp4 | FMT-09 | PASS | 1080x1920, h264/aac, 114.97 s, 30 fps |
| DelhiRain4_EN_IG.mp4 | FMT-09 | PASS | 1080x1920, h264/aac, 114.97 s, 30 fps |
| DelhiRain4_TE_YT.mp4 | FMT-09 | PASS | 1080x1920, h264/aac, 134.60 s, 30 fps |
| DelhiRain4_TE_IG.mp4 | FMT-09 | PASS | 1080x1920, h264/aac, 134.60 s, 30 fps |
| EN: video body identical at 8 points (ending excluded) | FMT-09 | PASS | max difference 0.61 (limit 2.0); points [6.6, 19.7, 32.8, 45.9, 59.0, 72.2, 85.3, 98.4] |
| EN: audio in sync across platforms (3 windows, ending excluded) | FMT-09 | PASS | 18s lag +0 ms r=1.00; 50s lag +0 ms r=1.00; 81s lag +0 ms r=1.00 (limits: \|lag\| <= 40 ms, r >= 0.9) |
| EN: platform endings | FMT-06 | PASS | durations [114.97, 114.97] s; the last 10.0 s may differ by design (FMT-06) |
| TE: video body identical at 8 points (ending excluded) | FMT-09 | PASS | max difference 0.45 (limit 2.0); points [7.8, 23.4, 38.9, 54.5, 70.1, 85.7, 101.2, 116.8] |
| TE: audio in sync across platforms (3 windows, ending excluded) | FMT-09 | PASS | 22s lag +0 ms r=1.00; 60s lag +0 ms r=1.00; 97s lag +0 ms r=1.00 (limits: \|lag\| <= 40 ms, r >= 0.9) |
| TE: platform endings | FMT-06 | PASS | durations [134.6, 134.6] s; the last 10.0 s may differ by design (FMT-06) |
