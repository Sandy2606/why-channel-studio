## check_exports: DelhiRain5

**Overall: PASS**

Coverage: expected: 4; found: 4

| Check | Rule | Status | Detail |
|---|---|---|---|
| DelhiRain5_EN_YT.mp4 | FMT-09 | PASS | 1080x1920, h264/aac, 102.79 s, 30 fps |
| DelhiRain5_EN_IG.mp4 | FMT-09 | PASS | 1080x1920, h264/aac, 102.79 s, 30 fps |
| DelhiRain5_TE_YT.mp4 | FMT-09 | PASS | 1080x1920, h264/aac, 124.46 s, 30 fps |
| DelhiRain5_TE_IG.mp4 | FMT-09 | PASS | 1080x1920, h264/aac, 124.46 s, 30 fps |
| EN: video body identical at 8 points (ending excluded) | FMT-09 | PASS | max difference 0.00 (limit 2.0); points [5.8, 17.4, 29.0, 40.6, 52.2, 63.8, 75.4, 87.0] |
| EN: audio in sync across platforms (3 windows, ending excluded) | FMT-09 | PASS | 16s lag +0 ms r=1.00; 44s lag +0 ms r=1.00; 72s lag +0 ms r=1.00 (limits: \|lag\| <= 40 ms, r >= 0.9) |
| EN: platform endings | FMT-06 | PASS | durations [102.79, 102.79] s; the last 10.0 s may differ by design (FMT-06) |
| TE: video body identical at 8 points (ending excluded) | FMT-09 | PASS | max difference 0.00 (limit 2.0); points [7.2, 21.5, 35.8, 50.1, 64.4, 78.7, 93.0, 107.3] |
| TE: audio in sync across platforms (3 windows, ending excluded) | FMT-09 | PASS | 20s lag +0 ms r=1.00; 55s lag +0 ms r=1.00; 89s lag +0 ms r=1.00 (limits: \|lag\| <= 40 ms, r >= 0.9) |
| TE: platform endings | FMT-06 | PASS | durations [124.46, 124.46] s; the last 10.0 s may differ by design (FMT-06) |
