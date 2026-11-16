## check_exports: DelhiRain2

**Overall: PASS**

Coverage: expected: 4; found: 4

| Check | Rule | Status | Detail |
|---|---|---|---|
| DelhiRain2_EN_YT.mp4 | FMT-09 | PASS | 1080x1920, h264/aac, 119.77 s, 30 fps |
| DelhiRain2_EN_IG.mp4 | FMT-09 | PASS | 1080x1920, h264/aac, 119.77 s, 30 fps |
| DelhiRain2_TE_YT.mp4 | FMT-09 | PASS | 1080x1920, h264/aac, 140.70 s, 30 fps |
| DelhiRain2_TE_IG.mp4 | FMT-09 | PASS | 1080x1920, h264/aac, 140.70 s, 30 fps |
| EN: video body identical at 8 points (ending excluded) | FMT-09 | PASS | max difference 0.00 (limit 2.0); points [6.9, 20.6, 34.3, 48.0, 61.7, 75.5, 89.2, 102.9] |
| EN: audio in sync across platforms (3 windows, ending excluded) | FMT-09 | PASS | 19s lag +0 ms r=1.00; 52s lag +0 ms r=1.00; 85s lag +0 ms r=1.00 (limits: \|lag\| <= 40 ms, r >= 0.9) |
| EN: platform endings | FMT-06 | PASS | durations [119.77, 119.77] s; the last 10.0 s may differ by design (FMT-06) |
| TE: video body identical at 8 points (ending excluded) | FMT-09 | PASS | max difference 0.00 (limit 2.0); points [8.2, 24.5, 40.8, 57.2, 73.5, 89.9, 106.2, 122.5] |
| TE: audio in sync across platforms (3 windows, ending excluded) | FMT-09 | PASS | 24s lag +0 ms r=1.00; 63s lag +0 ms r=1.00; 102s lag +0 ms r=1.00 (limits: \|lag\| <= 40 ms, r >= 0.9) |
| TE: platform endings | FMT-06 | PASS | durations [140.7, 140.7] s; the last 10.0 s may differ by design (FMT-06) |
