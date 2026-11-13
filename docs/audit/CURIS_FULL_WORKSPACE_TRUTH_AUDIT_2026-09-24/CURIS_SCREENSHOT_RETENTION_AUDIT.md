# Screenshot Retention Audit

Status: Review  
Authority Class: REVIEW / AUDIT EVIDENCE

## Whole-manifest image baseline

Manifest contains **2,480** PNG/JPG/JPEG/WEBP/GIF files, totaling **655,688,097 bytes (0.656 GB decimal)**. This is all workspace images, not all screenshots; manifest does not classify every image as a screenshot. Part 1 inventory metrics independently reports 2,480 images.

## Whole-manifest image disposition (all 2,480 image files)

Images outside identified Exploration family paths are conservatively counted as REVIEW_REQUIRED for this image-retention audit: 1,348 files / 393,427,430 bytes. This does not label them as Exploration assets.

| Disposition | Count | Bytes |
|---|---:|---:|
| KEEP_ACTIVE | 1 | 1,659,185 |
| KEEP_MINIMAL_EVIDENCE | 17 | 2,041,801 |
| ARCHIVE_OUTSIDE_ACTIVE | 0 | 0 |
| DELETE_CANDIDATE | 702 | 169,593,520 |
| REVIEW_REQUIRED | 1,760 | 482,393,591 |

Estimated bytes that could exit Active Workspace if CEO resolves the deletion conflict: **169,593,520 bytes (0.170 GB)**. This is a candidate, not an executed removal.

## Retention rule applied

- Retain 0 ordinary reproducible captures by default.
- Retain no more than 1–3 decision screenshots per closed family; the minimum can be zero where a text Closure records the decision completely.
- External states that cannot be reproduced require specific evidence provenance; unknown cases stay REVIEW_REQUIRED.
- Full CEO Review batches are not active merely because directory names say CEO Review.

The manifest proves path, size and modification time, not whether every image is reproducible or uniquely evidentiary. Content Growth, Writing, Music, Shared UI and visual-direction closures identify candidate screenshot families, but unresolved items remain Review Required.
