# HTML / Prototype Retention Audit

Status: Review  
Authority Class: REVIEW / AUDIT EVIDENCE

Existing workspace manifest records **985 HTML/HTM files** (Part 1 metric: 985 HTML; delta is extension filter and may include `.htm`; verify metric provenance before treating as contradiction). No new scan performed.

## Manifest classification

| Category | Count | Bytes |
|---|---:|---:|
| Production / Product Docs | 85 | 8,512,785 |
| Exploration | 126 | 7,456,793 |
| Generated | 426 | 11,056,247 |
| Coverage | 25 | 748,304 |
| Dependency | 161 | 5,900,985 |
| Test Fixture | 0 | 0 |
| Captured Page | 1 | 4,366 |
| Legacy Final UI | 0 | 0 |
| Unknown | 161 | 5,773,600 |

## Exploration disposition

Exploration HTML assigned by family: 152; `DELETE_CANDIDATE`: 24; `KEEP_ACTIVE`: 3; `REVIEW_REQUIRED`: 125.

An Exploration Set includes linked HTML/CSS/JS/data/JSON/Markdown/image/evidence files, and the CSV lists every manifest row selected into a family. Generated/dependency/test files outside exploration scopes retain their own categories. Avoid orphaning source dependencies: active HTML dependencies are grouped as a single source set; full replacement candidates apply to the complete obsolete set.

## Gate

Product Freeze §14 explicitly disallows deleting historical Exploration/Candidate. Delete Candidate counts in the CSV are review proposals only and require CEO disposition before any physical cleanup.
