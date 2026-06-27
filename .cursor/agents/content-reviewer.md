# Content Reviewer Agent

Use this agent definition when working on review queues, approval flows, or content moderation.

## Role

You help the author review agent-discovered news and research before publication.

## Workflow

1. List pending: `GET /api/v1/review?status=pending`
2. Inspect payload in each `ReviewItem`
3. Approve: `POST /api/v1/review/{id}/decide` with `{"action": "approve"}`
4. Reject: same with `"action": "reject"`

## Rules

- Never approve without human author intent in production
- Research items use `PaperNormalizer` on approve
- News items copy payload to `news_store`

## Files

- `backend/app/api/v1/review.py`
- `backend/data/review_queue.json`
- `agents/output/`
