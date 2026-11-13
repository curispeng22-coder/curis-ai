# CURIS DESKTOP SOURCE BASELINE CLOSURE REVIEW

Authority Class: REVIEW
Status: Review
Disposition: DESKTOP SOURCE BASELINE READY — CLEAN PACKAGE AND ISOLATED LAUNCH SMOKE VERIFIED — NOT STAGED OR COMMITTED
Date: 2026-08-20
Owner: Desktop Source Baseline Closure / Business Spine Main Developer
Next Action: merge the exact target objects below into the Business Spine promotion manifest and execute the final packaged Single / Multi / Generic / Parent Resolver / Legacy / restart E2E
Target Authority: `docs/reviews/CURIS_CANONICAL_BUSINESS_SPINE_IMPLEMENTATION_001_REVIEW.md` final acceptance record
Next Gate: final scoped commit only after the main developer's clean packaged E2E and active-database fingerprint pass

## 1. Verdict

**DESKTOP SOURCE BASELINE READY.**

The current Desktop candidate has been reduced to 20 Desktop-owned source files plus the
one accepted frontend packaging prerequisite, `frontend/next.config.js`. A controlled clean
tree installed declared dependencies, rebuilt the frontend and all three Python sidecars,
compiled Tauri from a fresh Cargo target, and produced a new `Curis.app`. That package
launched through macOS Launch Services with an isolated `HOME`, rendered the current CEO
Office, reached the frontend, Workspace Runtime and Gateway, and exited without orphaned
listeners or child processes.

No Product, Runtime, schema, database, high-fidelity UI or domain semantics were changed.
No current untracked Desktop file was deleted or overwritten. Nothing was bulk-added,
staged in the real index, committed or pushed.

## 2. Why `desktop/` was zero tracked

Current `HEAD` is `d3ab0ce46d3a0ebbe13b7748b6722ac0c4bf264a`. The accepted Business
Spine clean source tree `17096f6e9c9319533f8c7d3b1fa07658f122c1ea` contains zero
`desktop/` paths because the Desktop tree existed only in the current untracked working copy
and in an older broad snapshot. The previous frontend closure intentionally did not promote
that mixed tree. This was a source-baseline provenance gap, not evidence that Desktop source
was unnecessary or that the accepted Desktop behavior had been removed.

The current candidate is the preserved untracked `desktop/` working-copy tree. Its trusted
semantic authorities are the accepted Desktop Packaging, Runtime Flow and Single Instance
Issue/Review pairs. Historical snapshot `b7403bed68e44b466be2c7eedea4b5cda6e2db3d`
is a BASE source only; it is not current authority.

## 3. Phase 0 inventory and source boundary

| Path / class | Type | Current state | Historical source | Current-required | Why / semantic owner | Generated | Action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `desktop/Cargo.toml`, `Cargo.lock` | Rust manifest / lock | untracked candidate | `b7403bed6` | yes | exact Tauri/Rust dependency closure / Desktop Packaging | no | KEEP |
| `desktop/package.json`, `pnpm-lock.yaml` | Node package metadata | untracked candidate | manifest in `b7403bed6`; current pnpm lock is newer | yes | declared Tauri CLI install / Desktop Packaging | no | KEEP |
| `desktop/tauri.conf.json`, `build.rs` | Tauri/package build config | untracked candidate | `b7403bed6` | yes | bundle resources, metadata, build hook / Desktop Packaging | no | KEEP |
| `desktop/src/main.rs`, `src/lib.rs` | Rust launch source | untracked candidate | `b7403bed6` | yes | current single-instance, safe app-data paths and sidecar startup / Desktop Runtime Flow | no | KEEP |
| `desktop/runtime/backend_entry.py`, `gateway.py`, `guardian.py` | sidecar source | untracked candidate | `b7403bed6` | yes | Workspace service, local gateway and child supervision / Desktop Runtime Flow | no | KEEP |
| `desktop/scripts/build-runtime.sh`, `build-requirements.txt` | deterministic runtime build source | untracked candidate | `b7403bed6` | yes | fresh standalone frontend and PyInstaller sidecars / Desktop Packaging | no | KEEP |
| `desktop/Info-ATS.plist` | macOS bundle source metadata | untracked candidate | `b7403bed6` | yes | localhost App Transport Security allowance / Desktop Packaging | no | KEEP |
| `desktop/static/index.html` | Tauri build-time placeholder | untracked candidate | `b7403bed6` | yes | declared `frontendDist`; packaged app navigates to built localhost frontend / Desktop Packaging | no | KEEP |
| five configured Desktop icons | required bundle assets | untracked candidate | `b7403bed6` | yes | exact `tauri.conf.json` icon inputs / Desktop Packaging | no | KEEP |
| `frontend/next.config.js` | existing frontend build config | modified tracked candidate | clean BASE plus accepted Packaging delta | yes | `output: "standalone"` is required by `build-runtime.sh` / Frontend Packaging | no | KEEP |
| `desktop/.runtime/` | assembled package input | untracked ignored | also present in historical snapshot | no | rebuilt from source by `build-runtime.sh` | yes | REBUILD, NEVER PROMOTE |
| `desktop/target/` | Cargo/Tauri output | untracked ignored | also present in historical snapshot | no | rebuilt by Cargo/Tauri | yes | REBUILD, NEVER PROMOTE |
| `desktop/node_modules/` | installed dependencies | untracked ignored | also present in historical snapshot | no | restored from `pnpm-lock.yaml` | yes | REBUILD, NEVER PROMOTE |
| `desktop/gen/`, caches, logs, `.DS_Store` | generated metadata / cache | untracked or historical | `b7403bed6` | no | not source input | yes | DROP |
| historical `.app`, DMG/build-release output | packaged output | historical only | `b7403bed6` | no | must be freshly produced | yes | DROP |
| historical `package-lock.json` | redundant npm lock | historical only | `b7403bed6` | no | package declares pnpm and has current pnpm lock | no | DROP |
| historical mobile/store icon variants | unused assets | historical only | `b7403bed6` | no | not referenced by current Tauri config | no | DROP |
| historical secret-broker experiments | unused source | historical only | `b7403bed6` | no | no current importer or accepted authority | no | DROP |
| historical frontend probe/tests and manual release helpers | unused auxiliary source | historical only | `b7403bed6` | no | not required by the verified install/build/package/launch graph | no | DROP |

Repository `.gitignore` already excludes `desktop/.runtime/`, `desktop/target/`,
`desktop/node_modules/` and Runtime Python caches. No new ignore rule was needed.

## 4. BASE → CANDIDATE → TARGET decisions

The TARGET is not assumed from either historical BASE or current candidate. Each target
file was retained only when consumed by the clean graph or an accepted Desktop behavior.
Current candidate deltas from BASE are limited to current dependency versions, package
configuration, safe launch/runtime behavior, pnpm locking and the current local Gateway.

| File | BASE blob | TARGET object | TARGET SHA-256 | Decision |
| --- | --- | --- | --- | --- |
| `desktop/Cargo.toml` | `0a1dae8660814f4ab48c14dc15b00d3377ec14e0` | `29f5410eb82909b595715ce6946a9b71a669446e` | `373b2355346570ad7694514bab6dc6c8807143d94513a989556a25b6de2bb877` | KEEP candidate |
| `desktop/Cargo.lock` | `88398dda39f916257e889022068492949fe91265` | `717f2cb31bca573dccd5b080641e0b42dd3fd3d0` | `a294f30a916d5f07838cfe337869ce3531e033e38e4dba2f35e7b0423ab8c8d2` | KEEP candidate |
| `desktop/package.json` | `1f28a8b028d2e59ee8e0b8503b92dec5068920f5` | `7823cd1f9960685685a290521f7f33271c86ab7b` | `43e708eac0db2a9f06fdff128097dde7f210d9b8dae71a2fb6b9544af29db7a0` | KEEP candidate |
| `desktop/pnpm-lock.yaml` | none | `e16ec78de3594cc46a84a80f46eef4266b1559c1` | `d8f570544d0ce4558ace97e44537796f837ce86b5ae30a5ed694e8ad917db926` | KEEP current lock |
| `desktop/tauri.conf.json` | `6457dec19fa771f47784b952264c7a94d2fa3ab9` | `6611bbda97447b940021ed64e96ddddeb1277f10` | `ec2f3ea29d5b2f564a12699ab8196ad54a8cf3f9645d4a40dff2ebd964045da2` | KEEP candidate |
| `desktop/build.rs` | `988ed7d83545eaa27890f824676aa8d3617b4a35` | `d860e1e6a7cac333c3cc0bc9cb67faf286b07d69` | `487059eaf8a947b80f20a9aacac038a5047b2ad69d2401b827376c67d6fe847f` | KEEP candidate |
| `desktop/src/main.rs` | `c37ddaa807630b21e6b985a4b64ab1fd90c8a615` | `c37ddaa807630b21e6b985a4b64ab1fd90c8a615` | `44af83a699824ce989046dd66c1875081f526058b2cc54fb740c0fdfca6fab06` | KEEP unchanged BASE |
| `desktop/src/lib.rs` | `d3af81eb504d4fa4ce95911fb238bb01b9df963a` | `dd6b79a21f94d23f78bcd4d52ed92ff317d7e6f7` | `d2ada1540eb173f567c9396481ed66424646928a663b96adb7021f8476fcc56d` | KEEP accepted current behavior |
| `desktop/runtime/backend_entry.py` | `d0213e106d9eaa3bf7e20a7940bdec4e5341bb73` | `d0213e106d9eaa3bf7e20a7940bdec4e5341bb73` | `e6d204c904c3e975a7f55defd85a92eb7f30d46068ec582e1cf55471a0695a73` | KEEP unchanged BASE |
| `desktop/runtime/gateway.py` | `9e7695730c1cce282c1e932443c68710a4c8021a` | `5d14ae3fcb604bb353f0b76026623334458e086e` | `b5041bcbc0135f4ae065e0e91e237ff93594541c6f863974f19d3ba4cd06147a` | KEEP accepted current Gateway |
| `desktop/runtime/guardian.py` | `61d57b45f9de281a2171c9c73fc033c53b3f446e` | `61d57b45f9de281a2171c9c73fc033c53b3f446e` | `1ce17d70684f1708a14a9767469e31c1841f8b0955d576ca6c47d131587f2af5` | KEEP unchanged BASE |
| `desktop/scripts/build-runtime.sh` | `dfd93d1064091eee481247e3041c9bfaa25a6053` | `c887f70141ceea17ac7711112c61f2304db745b8` | `0de2f22e65024be2e953d4e38fbda3a304f4acd2e30bc70560399e6790262651` | KEEP accepted clean builder |
| `desktop/scripts/build-requirements.txt` | `6e5af46d720b7aa866d386d7248f30d6d700d6d8` | `6e5af46d720b7aa866d386d7248f30d6d700d6d8` | `ae24814b085416fcc32d82b477c8084eadcc2478f72100b06f386733b0f097b9` | KEEP unchanged BASE |
| `desktop/Info-ATS.plist` | `cc52e29b9f2957d09438057d6b6d3a630b13554e` | `cc52e29b9f2957d09438057d6b6d3a630b13554e` | `fdd066e2cf3997a6275e23bedc88bc6488b537e7f0a90e67dc5098da6637870d` | KEEP unchanged BASE |
| `desktop/static/index.html` | `856a8f52e6f30f167ed499c866dd053cbe5ded31` | `d9568306dc63e2564943a6cf7ffb923588109446` | `f1dba4c3b1ec0a93f7de83780e3458a8900b6894ca159267f67a31c4a355addc` | KEEP current placeholder |
| `desktop/icons/32x32.png` | `421665d68cb0a348d719d82e001e419263bf7f17` | same | `e5384104eca90ef4df92c453123a538b69e57175d14d2f02cb19d150b2f9b878` | KEEP referenced asset |
| `desktop/icons/128x128.png` | `0ad9e5c4ff6586cd0b96fa0f6f6ed366a23c94e1` | same | `941370c87412181584ee6a7c1ce3e593e00e442969675ac94cf206e08031a4f2` | KEEP referenced asset |
| `desktop/icons/128x128@2x.png` | `31f97f4e7f35526e53ec5aca886beca5247970a9` | same | `f569f64a95ababefaa2b0fa2206a9421433d6eed63c46e34f1ca52bc2ffd3d6f` | KEEP referenced asset |
| `desktop/icons/icon.icns` | `35e0bc52bc1f59c62e962ad498104a2062ee3678` | same | `e5fc5ba88ba9bf8856dd0f82d8a4c51224a5362f8a10fd4087d31d2e58ccc3ab` | KEEP referenced asset |
| `desktop/icons/icon.ico` | `1fe498101da65b08878cb35fe6767fde0e696124` | same | `0dfad4d64cbe4878304d271a584226868262f4bb4b4194ac164d57634788d545` | KEEP referenced asset |
| `frontend/next.config.js` | `a54f7cc14d86785ea8feffb5d3350cfa111c228f` | `196deea3eff292957406141229453f90a7db0c3e` | `635c187eb4eb51894353971b83c5d7f0e7fa6951e13ce00417d9c7faec714a74` | KEEP accepted standalone-output delta |

## 5. Exact source Allowed Files

```text
desktop/Cargo.toml
desktop/Cargo.lock
desktop/package.json
desktop/pnpm-lock.yaml
desktop/tauri.conf.json
desktop/build.rs
desktop/src/main.rs
desktop/src/lib.rs
desktop/runtime/backend_entry.py
desktop/runtime/gateway.py
desktop/runtime/guardian.py
desktop/scripts/build-runtime.sh
desktop/scripts/build-requirements.txt
desktop/Info-ATS.plist
desktop/static/index.html
desktop/icons/32x32.png
desktop/icons/128x128.png
desktop/icons/128x128@2x.png
desktop/icons/icon.icns
desktop/icons/icon.ico
frontend/next.config.js
```

This Review is the only additional evidence file:
`docs/reviews/CURIS_DESKTOP_SOURCE_BASELINE_CLOSURE_REVIEW.md`.

The source-only controlled tree before this Review is
`7666051f86d125f98c1c6888f00d844cd488be69`. Its diff from the accepted
frontend tree is exactly the 20 Desktop paths above and `frontend/next.config.js`.

## 6. Clean source dependency graph

```text
clean controlled source tree
├── frontend/package.json + pnpm-lock.yaml
│   └── pnpm install --frozen-lockfile
│       └── pnpm build → frontend/.next/standalone + static assets
├── backend/requirements.txt
│   └── isolated Python venv
├── desktop/scripts/build-requirements.txt
│   └── PyInstaller in the same isolated venv
└── desktop/package.json + pnpm-lock.yaml + Cargo.toml + Cargo.lock
    └── pnpm install --frozen-lockfile
        └── tauri build
            ├── build-runtime.sh
            │   ├── packaged Node + standalone frontend
            │   ├── curis-workspace
            │   ├── curis-gateway
            │   └── curis-guardian
            └── fresh Cargo release → Curis.app
```

Declared external toolchain used: Node `v24.16.0`, pnpm `10.34.5`, Python
`3.14.5`, PyInstaller `6.15.0`, Cargo `1.97.1`, Rust `1.97.1`. No old `.app`,
old target output, working-copy-only file, undeclared source path or signing secret was used.

## 7. Clean build proof

Build root:
`/tmp/curis-desktop-source-closure.9J7Y0w/export-v2`

Commands:

```bash
cd frontend
pnpm install --frozen-lockfile

python3 -m venv /tmp/curis-desktop-source-closure.9J7Y0w/export/.build-venv
/tmp/curis-desktop-source-closure.9J7Y0w/export/.build-venv/bin/python -m pip install \
  -r backend/requirements.txt \
  -r desktop/scripts/build-requirements.txt

cd desktop
pnpm install --frozen-lockfile
CURIS_BUILD_PYTHON=/tmp/curis-desktop-source-closure.9J7Y0w/export/.build-venv/bin/python pnpm build
```

Result: **PASS**.

- frontend production build: PASS, 42 routes;
- fresh standalone frontend assembly: PASS;
- fresh Workspace, Gateway and Guardian PyInstaller sidecars: PASS;
- fresh Cargo release build: PASS;
- fresh macOS application bundle: PASS.

New package:
`/tmp/curis-desktop-source-closure.9J7Y0w/export-v2/desktop/target/release/bundle/macos/Curis.app`

- size: `442M`;
- main executable SHA-256:
  `193445e462ef3dc03068906c1e9f8c35de0c1810da3588003478168c17dddd86`;
- bundle identifier: `com.curis.desktop`;
- runtime manifest ports: frontend `3010`, Workspace `8002`, Gateway `8080`;
- packaged data path: `data/curis.sqlite` beneath the app-data directory;
- packaged runtime contains the standalone frontend, Node, Workspace, Gateway and Guardian;
- no database, environment file, private key or application log is packaged. The only `.pem`
  is Certifi's public CA trust bundle.

## 8. Packaged Desktop launch smoke

The new `.app` was launched through macOS Launch Services with:

```text
HOME=/tmp/curis-desktop-smoke.20260820/home
TMPDIR=/tmp/curis-desktop-smoke.20260820/tmp
```

Result: **PASS**.

- native window title: `Curis — CEO Office`;
- focused WebView: `127.0.0.1:3010/ceo-office`;
- visual result: current CEO Office rendered, with no immediate package/bridge failure;
- `GET http://127.0.0.1:3010/ceo-office`: `200`, title `Curis CEO Office`;
- `GET http://127.0.0.1:8002/health`: `200`, `{"status":"ok"}`;
- `GET http://127.0.0.1:8080/health`: `200`, `{"status":"ok"}`;
- authenticated Gateway request for current companies: `200`, tenant `selfuse`;
- isolated SQLite created only under the isolated app-data directory;
- after native quit, ports `3010`, `8002`, `8080` had no listeners and no packaged child
  process remained.

The repository active databases were unchanged before and after launch:

| Path | Size | mtime | SHA-256 |
| --- | ---: | ---: | --- |
| `data/curis.sqlite` | `1232896` | `1786873339` | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` |
| `backend/data/curis.sqlite` | `1277952` | `1786783659` | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` |

This smoke proves package startup and current frontend/runtime reachability only. It does not
claim the main developer's final packaged Single / Multi / Generic / Parent Resolver /
Legacy / restart Business Spine E2E.

## 9. Known warnings and release boundary

- The local development bundle has only a linker-generated ad-hoc executable signature;
  `codesign --verify --deep --strict` does not accept the bundle because resources are not
  sealed. No Developer ID, notarization or distribution credential was requested or used.
  This does not block the authorized local development-package launch proof; it remains a
  release/distribution gate.
- `BUILD-MANIFEST.json` records `gitSha: "unknown"` because the controlled export intentionally
  has no `.git` directory. Source provenance is instead fixed by the Git objects and tree IDs
  in this Review.
- Next standalone output embeds its clean temporary `outputFileTracingRoot`; PyInstaller bytecode
  embeds clean-export compile filenames. These are build provenance strings, not runtime file
  dependencies. Launch succeeded after the source build without access to the working copy.
- Workspace logs `D1 toolchain unavailable; service continues without it`; all three package
  services and the current application still passed this bounded launch smoke. D1 is not part
  of this Desktop source-baseline gate.

## 10. Required fourteen answers

1. **Why was `desktop/` zero tracked?** It was omitted from the prior controlled frontend tree
   because current Desktop source was untracked and historical `b7403bed6` was mixed with
   generated and stale content; whole-tree promotion was forbidden.
2. **Where is historical Desktop source?** In tracked snapshot
   `b7403bed68e44b466be2c7eedea4b5cda6e2db3d`, used only as BASE/provenance.
3. **Where did the current candidate come from?** The preserved untracked current working-copy
   `desktop/` tree, reconciled against accepted Desktop Issue/Review authority.
4. **Which paths are source?** The exact 21-file source Allowed Files manifest in section 5.
5. **Which paths are generated?** `.runtime/`, `target/`, `node_modules/`, `gen/`, `.next/`,
   caches, logs, temporary files, `.app`, DMG and other package outputs.
6. **Which historical source was dropped?** Redundant npm lock, secret-broker experiments,
   unused mobile/store icons, old frontend probe/tests, manual release helpers, obsolete
   package output and every generated subtree.
7. **Which candidate was kept or rebuilt?** All 21 source inputs were kept after semantic and
   dependency audit; frontend standalone output, sidecars, dependencies, Cargo target and
   `.app` were rebuilt from clean source.
8. **What are the exact TARGET files?** Section 5 is the complete source manifest; section 4
   records each target object and SHA-256.
9. **Can a clean checkout restore it?** Yes. Controlled source tree
   `7666051f86d125f98c1c6888f00d844cd488be69` exported all required source without the
   working copy and completed the graph.
10. **Did clean Desktop build pass?** Yes; frontend, three sidecars, Cargo release and Tauri
    macOS bundle all passed from fresh output.
11. **Did the newly built package launch?** Yes; the native window rendered current CEO Office
    and frontend/Workspace/Gateway health and request evidence passed.
12. **Any working-copy-only dependency?** No. The build and launch consumed only the controlled
    source export, declared dependency locks/toolchain and newly generated outputs.
13. **Were Product or Runtime semantics modified?** No. No source was edited in this closure;
    it reconstructed provenance for already accepted Desktop behavior.
14. **Can this return to Business Spine final acceptance?** Yes. The main developer can merge
    the exact objects and proceed directly to the final packaged Business Spine E2E and scoped
    commit gate.

## 11. Git preservation evidence

The real index was not used for controlled-tree construction. Its staged-diff SHA-256 before
and after build and launch remained:
`9c651783ea44f83e4267655e7182cb9602e3eac4df21474cebbf07b3b30e9b32`.

No `git add desktop/`, `git add .`, `git add -A`, reset, clean, checkout overwrite, deletion,
commit or push occurred. The current Desktop candidate remains in place.

## 12. Handoff

**DESKTOP SOURCE BASELINE READY**

The Business Spine main developer should consume the exact objects and Allowed Files in this
Review, regenerate the combined clean tree, rebuild the package, execute final packaged
Single / Multi / Generic / Parent Resolver / Legacy / restart evidence, reconfirm the active
database fingerprints, and only then create the final scoped commit. **NOT PUSHED.**
