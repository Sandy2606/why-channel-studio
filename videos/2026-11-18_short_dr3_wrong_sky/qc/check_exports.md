## check_exports: DelhiRain3

**Overall: PASS**

Coverage: expected: 4; found: 4

| Check | Rule | Status | Detail |
|---|---|---|---|
| DelhiRain3_EN_YT.mp4 | FMT-09 | PASS | 1080x1920, h264/aac, 130.20 s, 30 fps |
| DelhiRain3_EN_IG.mp4 | FMT-09 | PASS | 1080x1920, h264/aac, 130.20 s, 30 fps |
| DelhiRain3_TE_YT.mp4 | FMT-09 | PASS | 1080x1920, h264/aac, 159.70 s, 30 fps |
| DelhiRain3_TE_IG.mp4 | FMT-09 | PASS | 1080x1920, h264/aac, 159.70 s, 30 fps |
| EN: video body identical at 8 points (ending excluded) | FMT-09 | PASS | max difference 0.00 (limit 2.0); points [7.5, 22.5, 37.6, 52.6, 67.6, 82.6, 97.7, 112.7] |
| EN: audio in sync across platforms (3 windows, ending excluded) | FMT-09 | PASS | 22s lag +0 ms r=1.00; 58s lag +0 ms r=1.00; 94s lag +0 ms r=1.00 (limits: \|lag\| <= 40 ms, r >= 0.9) |
| EN: platform endings | FMT-06 | PASS | durations [130.2, 130.2] s; the last 10.0 s may differ by design (FMT-06) |
| TE: video body identical at 8 points (ending excluded) | FMT-09 | PASS | max difference 0.03 (limit 2.0); points [9.4, 28.1, 46.8, 65.5, 84.2, 102.9, 121.6, 140.3] |
| TE: audio in sync across platforms (3 windows, ending excluded) | FMT-09 | PASS | 27s lag +0 ms r=1.00; 72s lag +0 ms r=1.00; 117s lag +0 ms r=1.00 (limits: \|lag\| <= 40 ms, r >= 0.9) |
| TE: platform endings | FMT-06 | PASS | durations [159.7, 159.7] s; the last 10.0 s may differ by design (FMT-06) |
