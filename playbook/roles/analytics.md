# Role: Analytics

**Inputs:** platform analytics once access is verified; the delivered videos and their scene sheets.
**Responsibilities:** the weekly performance review; tracing each lesson to the stage that caused it.
**Outputs:** `templates/performance_review.md` filled in each week; TEST entries in `history.md`.

## Rules
- **[AN-01]** (P, user Nov 10) Don't treat performance as diagnosed until the actual retention and viewed-versus-swiped-away figures are in. Make no performance claims without data. Analytics access (vidIQ, Metricool) is not yet verified.
- **[AN-02]** (P, Phase 2A approval) The weekly review records KEEP, DROP or TEST, with each lesson traced to a stage. A TEST becomes a rule only with the user's approval (→ WF-05).
- **[AN-03]** (C, user Nov 1) After posting, watch the replay rate on loops and any dips at correction or legal-flash beats.

## Checklist
1. Data source and date recorded.
2. Each lesson is linked to a stage and a video.
3. No conclusions from fewer than a few videos or from data that isn't available.
4. Proposed rule changes are sent to the user, not applied.
5. Lessons are recorded as TEST in `history.md`, never written straight into a rule file.
6. Platform facts quoted in a review carry their source and date (→ `platform_rules.md`).

**Failure conditions:** claims without data; a rule changed without approval.
**Handoff:** proposals go to the user; approved changes go to the owner file via the replace procedure.
