# Wave 3 CEO Decision — Remaining Historical/UI Consolidation

Status: Review  
Authority Class: REVIEW / Audit Evidence  
Decision boundary: Recommendations only. No delete, move, archive, rename, authority change, or worktree action occurred.

## Family decisions

| Family | Recommendation | Archive set | Delete set | Keep minimal / active | CEO decision |
|---|---|---|---|---|---|
| CEO Workspace | HOLD | NONE | NONE | 48 rows / 3,165,440 B | PENDING |
| Conversation | DELETE_APPROVABLE | NONE | 4 screenshot paths / 870,012 B | 0 | PENDING |
| curis operational visual exploration | ARCHIVE_OUTSIDE_ACTIVE | All 8 rows / 2,838,390 B | NONE | 0 | PENDING |
| CURIS OPERATIONAL VISUAL EXPLORATION | ARCHIVE_OUTSIDE_ACTIVE | All 14 rows / 3,033,661 B | NONE | 0 | PENDING |
| curis project workspace visual exploration | ARCHIVE_OUTSIDE_ACTIVE | All 7 rows / 3,423,811 B | NONE | 0 | PENDING |
| CURIS PROJECT WORKSPACE VISUAL EXPLORATION | ARCHIVE_OUTSIDE_ACTIVE | All 6 rows / 3,419,821 B | NONE | 0 | PENDING |
| curis ui prototype | ARCHIVE_OUTSIDE_ACTIVE | All 227 rows / 23,957,223 B | NONE | 0 | PENDING |
| curis ui prototype.bak | HOLD_WITH_SPECIFIC_REASON | 18 non-identical rows / 1,354,059 B | 33 hash-identical rows / 5,072,731 B | 18 rows / 1,354,059 B | PENDING |
| Employee | ARCHIVE_OUTSIDE_ACTIVE | All 11 rows / 2,289,772 B | NONE | 0 | PENDING |
| Figma | HOLD_WITH_SPECIFIC_REASON | 16 PNGs / 4,100,074 B already reside under docs/99_Archive; 5 decision/context records remain minimal | NONE | 9 rows / 132,822 B | PENDING |
| Four-Pane | ARCHIVE_OUTSIDE_ACTIVE | 1 row / 57,299 B | NONE | 0 | PENDING |
| Knowledge | HOLD_WITH_SPECIFIC_REASON | NONE | NONE | 14 rows / 1,207,834 B | PENDING |
| Meeting | ARCHIVE_OUTSIDE_ACTIVE | All 18 rows / 1,641,895 B | NONE | 0 | PENDING |
| multi surface workspace screenshots | HOLD_WITH_SPECIFIC_REASON | NONE | NONE | 23 rows / 3,947,704 B | PENDING |
| Operating Intelligence | HOLD_WITH_SPECIFIC_REASON | NONE | NONE | 2 rows / 119,258 B | PENDING |
| Professional Workspace | KEEP_MINIMAL_EVIDENCE | 3 research notes / 27,053 B | NONE | 0 | PENDING |
| prototypes | HOLD_WITH_SPECIFIC_REASON | NONE | NONE | 108 rows / 12,257,726 B | PENDING |
| RD WORKSPACE HTML EXPLORATION | ARCHIVE_OUTSIDE_ACTIVE | All 21 rows / 4,501,742 B | NONE | 0 | PENDING |
| screenshots | HOLD_WITH_SPECIFIC_REASON | NONE | NONE | 51 rows / 5,904,815 B | PENDING |
| Shared Employee Interaction | KEEP_MINIMAL_EVIDENCE | 2 distinct captures / 508,803 B | 6 HTML/CSS/JS/check/metadata files / 53,782 B | 0 | PENDING |
| Talent | ARCHIVE_OUTSIDE_ACTIVE | All 8 rows / 1,259,421 B | NONE | 0 | PENDING |
| Unresolved Exploration | HOLD_WITH_SPECIFIC_REASON | NONE | NONE | 105 rows / 1,487,781 B | PENDING |

## Separate exact sets

| Set | Recommendation | Files | Bytes | CEO decision |
|---|---|---:|---:|---|
| `BAK-DUP-01` — same-relative `.bak` copies with exact SHA-256 match | APPROVE DELETE? | 33 | 5,072,731 | PENDING |
| `SHARED-OLD-HTML-01` — superseded runnable validation package | APPROVE DELETE? | 6 | 53,782 | PENDING |
| `CONV-SCREEN-01` — superseded persistent-Conversation screenshots | APPROVE DELETE? | 4 | 870,012 | PENDING |
| Content Growth/Theme minimal-evidence compression subset | APPROVE DELETE? | 8 | 3,206,614 | PENDING |
| Archive outside Active exact sets listed in resolution | APPROVE ARCHIVE? | 321 | 46,423,035 | PENDING |
| Root review dispositions | APPROVE / MODIFY / HOLD by row | 28 | 21,276,438 | PENDING |

The four rows above proposing delete total **51 unique paths / 9,203,139 B**. The minimal-evidence row is a subset of that total and is intentionally not added twice. `HOLD_WITH_SPECIFIC_REASON` means only the named missing fact remains; no blanket delete is proposed.

## CEO response

For each family/set, write one of: `APPROVE DELETE`, `APPROVE ARCHIVE`, `KEEP`, or `HOLD`. The `.bak` recommendation applies only to the 33 hash-identical paths; the 18 different files remain HOLD. Shared Employee approval applies only to the six listed validation files; preserve the two state captures and Frozen Shell authority. Root decisions apply only to the exact 28 rows in `CURIS_ROOT_REVIEW_RESOLUTION.csv`.
