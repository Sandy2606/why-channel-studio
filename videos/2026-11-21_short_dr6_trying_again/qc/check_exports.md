## check_exports: DelhiRain6

**Overall: PASS**

Coverage: expected: 4; found: 4

| Check | Rule | Status | Detail |
|---|---|---|---|
| DelhiRain6_EN_YT.mp4 | FMT-09 | PASS | 1080x1920, h264/aac, 121.07 s, 30 fps |
| DelhiRain6_EN_IG.mp4 | FMT-09 | PASS | 1080x1920, h264/aac, 121.07 s, 30 fps |
| DelhiRain6_TE_YT.mp4 | FMT-09 | PASS | 1080x1920, h264/aac, 144.85 s, 30 fps |
| DelhiRain6_TE_IG.mp4 | FMT-09 | PASS | 1080x1920, h264/aac, 144.85 s, 30 fps |
| EN: video body identical at 8 points (ending excluded) | FMT-09 | PASS | max difference 0.00 (limit 2.0); points [6.9, 20.8, 34.7, 48.6, 62.5, 76.4, 90.2, 104.1] |
| EN: audio in sync across platforms (3 windows, ending excluded) | FMT-09 | PASS | 20s lag +0 ms r=1.00; 53s lag +0 ms r=1.00; 86s lag +0 ms r=1.00 (limits: \|lag\| <= 40 ms, r >= 0.9) |
| EN: platform endings | FMT-06 | PASS | durations [121.07, 121.07] s; the last 10.0 s may differ by design (FMT-06) |
| TE: video body identical at 8 points (ending excluded) | FMT-09 | PASS | max difference 0.80 (limit 2.0); points [8.4, 25.3, 42.1, 59.0, 75.9, 92.7, 109.6, 126.4] |
| TE: audio in sync across platforms (3 windows, ending excluded) | FMT-09 | PASS | 24s lag +0 ms r=1.00; 65s lag +0 ms r=1.00; 105s lag +0 ms r=1.00 (limits: \|lag\| <= 40 ms, r >= 0.9) |
| TE: platform endings | FMT-06 | PASS | durations [144.85, 144.85] s; the last 10.0 s may differ by design (FMT-06) |
