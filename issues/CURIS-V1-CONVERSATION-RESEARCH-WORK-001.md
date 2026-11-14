# CURIS-V1-CONVERSATION-RESEARCH-WORK-001

Status: Review
Authority Class: CURRENT / IMPLEMENTATION ISSUE
Owner: Hao
Updated: 2026-11-15
Baseline: 0deae7ee45ad2372b8c8912f1511f85d25f96ade
Disposition: REVIEW_REQUIRED

Hao approved this first implementation slice on 2026-11-15. The [bounded validation report](../artifacts/tasks/CURIS-VALIDATION-B-EMPLOYEE/REPORT.md) reproduced a business leader reply with no durable Work. The implementation below addresses that gap at the conversation API boundary.

- Allowed Files: `backend/app/api/conversation_router.py`, `backend/app/conversation_service.py`, `backend/tests/test_employee_conversation.py`, `frontend/components/v1/EmployeeConversation.js`, `frontend/lib/v1FrontendApi.js`, and this Issue. Hao approved the scope correction and these two frontend paths following the native entry review.
- Allowed Directories: this chat's isolated worktree, with changes limited to the listed paths. Isolated verification inputs, logs and evidence may be placed under the existing `artifacts/tasks/CURIS-VALIDATION-B-EMPLOYEE/` task directory.
- Input: a saved leader reply explicitly proposing a research problem and expected result, tied to the original user message and current business Assignment. The authorized Company actor explicitly confirms the exact saved proposal version.
- Output: one canonical research Cycle/Work under the same business scope and Assignment, with a persisted receipt on the original conversation. Use the existing published responsibility workflow. Ordinary messages do not create Work. Creation does not execute it.
- Acceptance evidence: the ordinary message path yields a reviewable proposal. The explicit confirmation creates one persistent Work bound to both source messages and the proposal version. Duplicate and concurrent confirmations return the same identifiers. Invalid message, stale Assignment, stale workflow and mismatched proposal version cannot create Work. A new process can retrieve the original receipt and Work and safely repeat confirmation.
- Boundary: proposal and confirmation require canonical `BUSINESS` scope. The employee profile conversation uses the existing confirmation API and shows the persisted receipt. The separate D1 conversation surface, real Provider calls, research execution, cross-employee delivery, Evidence, song planning and release are outside this slice.
- Next Gate: Hao and coordination review the candidate and evidence before authorizing any next slice.
