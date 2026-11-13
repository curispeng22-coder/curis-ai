# Historical Retention Authority Revision Proposal

Status: Review  
Authority Class: REVIEW / PROPOSAL — DOES NOT MODIFY FROZEN AUTHORITY  
Target Authority: `docs/reviews/CURIS_V1_PRODUCT_FREEZE.md` §14  
Owner: CEO / Product  
Next Gate: Explicit CEO decision before Part 4 physical cleanup

## OLD

Product Freeze §14 currently states: “No historical Exploration or Candidate is deleted. None is a default implementation Authority except the explicitly listed visual inputs, and those remain subordinate to the Frozen contract.”

## PROBLEM

This preserves the full physical artifact set even after an accepted successor and the decision record are retained. A large HTML/CSS/JS prototype, repeated screenshot captures, generated packages and old exports can remain forever in the active workspace. Part 2 identified 883 Exploration delete-candidate files totaling 206,110,003 apparent bytes, including 702 image files totaling 169,593,520 bytes. None has been removed. Part 2 also identified 18 small external-archive candidates totaling 293,229 bytes.

## NEW PROPOSED RULE

> Historical decision, closure, accepted finding, rejection rationale, authority provenance and the minimum required Decision Evidence must remain traceable. A historical physical Exploration/Candidate artifact set may be deleted only when a recorded disposition proves its legal successor, replacement scope, current Product/Visual/Interaction status, unique-source and unique-information checks, reference impact, and an owner-approved retention decision. All other historical sets remain `REVIEW_REQUIRED`; filenames, age, `Frozen`, `Accepted`, and mtime do not authorize deletion.

The disposition record must include `Superseded By`, decision date/evidence, FULL/PARTIAL/VISUAL-ONLY/PRODUCT-ONLY/INTERACTION-ONLY replacement scope, `Unique Information Remaining`, decision evidence retained, references updated/obsolete, owner and deletion gate. The file set and its generated evidence are treated atomically.

## WHAT REMAINS PROTECTED

- CEO decisions, Closures, accepted/rejected findings and current Authority provenance.
- Any source still current for a surface, interaction, unique business asset or editable design.
- Non-reproducible external state evidence and the minimum CEO decision screenshots needed to explain a decision.
- Dirty/untracked/unpushed code, business assets, active Figma editable source, required release artifacts and unresolved sets.
- The Part 2 active business visual references explicitly named by Freeze, subordinate to the Product contract.

## WHAT MAY BE DELETED

Only a set marked `DELETE_CANDIDATE` or later `DELETE_APPROVED` by the authorized owner after all proof fields above are complete; no physical deletion follows from `DELETE_CANDIDATE` alone. Reproducible screenshot batches, superseded HTML/CSS/JS, duplicate exports, transport ZIPs and caches may qualify. Full/partial successor scope must be established for each set; partially superseded sources retain unique surfaces or stay archived/review-required.

## MIGRATION IMPACT

- Product Freeze §14 and any files that quote its absolute no-delete rule must be updated through a formally authorized CEO authority revision; this proposal cannot silently reinterpret the current text.
- Update Pointer/authority provenance/Change Log under the project's authority change process, if approved.
- Reconcile Part 2 CSV Delete Candidate sets against final CEO-approved dispositions; retain minimal Decision Evidence.
- Apply retention only through a separate Part 4 exact-path execution manifest, with pre/post fingerprints and no `git clean`, broad directory deletion, or history rewriting.

## RISK

The principal risk is deleting a unique source or an accepted interaction detail whose decision is recorded only in the prototype. Mitigations: atomic sets, source/reference scans, replacement-scope proof, checksum manifest, minimum evidence retention, owner gate, protected dirty worktrees and stop-on-unknown. External archive is optional, not a loophole.

## CEO GATE REQUIRED

Choose: (A) retain the current absolute rule and accept zero historical Exploration deletion; (B) approve the proposed narrow rule and amend §14 through the formal Authority change path; or (C) approve a different precise scope. No Part 4 deletion is allowed until this gate is resolved.
