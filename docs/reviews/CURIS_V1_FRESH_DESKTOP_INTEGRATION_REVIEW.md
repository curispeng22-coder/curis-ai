# Fresh Desktop BUILD_ONLY Review

Status: Review
Authority Class: REVIEW / EVIDENCE
Disposition: REVIEW_REQUIRED
Task ID: CURIS-V1-FRESH-DESKTOP-INTEGRATION-001
Owner / Return Target: Curis V1 交付负责人 /019ff1ba-f696-7002-8a6c-2b357ded819c
Verdict: BUILD_ONLY_READY_FOR_INDEPENDENT_STATIC_QA. NATIVE / FULL APP / PRODUCT NOT_ACCEPTED.

## 已构建与静态证明

新 App：`/private/tmp/curis-fresh-desktop-integration-20261005-01/cargo-target/release/bundle/macos/Curis.app`。真实 offline/frozen Tauri production build02 exit0/125.73s（Rust release1m58s），无 DMG/安装/发布/DeveloperID/notarize。Same Task frontend47/47 BuildID `ITtva07Pq58J1Jdh1HkX5`，1511regular outputSHA0漂移；不是旧Task frontend。Workspace/Gateway/Guardian/Recovery全部新生成（sidecars05 exit0/37.79s），新Node+4program实际MachOarm64/mode755。

PyInstaller actual TOC与workspace包内55DATA sourceSHA逐项一致：Writing、CG0.1/0.2、Music全部18json、四config、33publicAgentassets。不是collect-submodules推断收录或fallback。运行资源22847regular0links；App签名后22851regular0links，全部22847runtime resource原生成SHA在App仍0漂移；55data签名后仍exactsourceSHA。App actualplist com.curis.desktop/0.1.0/minmac12.0。最终Appmain SHA `46f6e78b576815acf5f65e22a0f09559f63ab90857882d477228a563a43f16a4`。

初始 Rust linkeradhoc仅覆盖binary、资源未封，codesign strictdeep失败已保留。依明确BUILD_ONLY许可只对新App执行 `codesign --force --sign - --identifier com.curis.desktop`，无developeridentity/Keychainitems授权；guard保持deny。最终 static codesign display0 / verify--deep--strict0，Signatureadhoc、TeamIdentifiernotset、资源envelope22848。不是Gatekeeper/notarization/native启动验收。before-signseal/原nonruntimeAppbytes在本Taskexternal evidence retained。

## 批准 / 问题 / 场景与依据 / 影响及风险

|批准|具体问题和场景依据|影响/风险/保留边界|
|---|---|---|
|正式BUILD_ONLY489source/七scriptdataargs|普通App需要真正新frontend/四program与CG0.2、配置/33assets，旧资源不可冒充|唯一canonical改动script7adds；配置值/阈值/releasepublished/业务code不改；Product/Frozen/Current不晋升|
|公开Node/Python/PyInstaller/Tauri/Cargo+pnpm/Rust真目标补充|offline构建需要公共工具正向物化，原globalHOME不可整体拷贝|35409publiccontent绑定（35377regular+32filelinks）及3内部directorylinks；exact tools/read-only origins，旧缓存/私有文件不读；资源最终全物化0links|
|六exactpublicnativePython libs|actual03_ssl/sqlite警告+fatalmpdecimal guarddenied；静态otool解析xz/zstd|仅6library load/resolvedliteral和新root副本，非整Homebrew/SQLCLI/DB/Runtime执行；source/cap原值不改|
|同Taskfrontend复用和PyInstallercacheenv|既已fresh47且1511SHA不变；04宿主bincache被guard拒绝|sameTasksealedfrontend复用；PYINSTALLER_CONFIG_DIR新root，拒绝旧缓存保留；没有重复旧Task/old.app|
|Task-onlybeforeBuild静态gateoverlay|strict process-execdeny使test-x为false，即使5files755/已封存；不是missing资源|仅build.beforeBuildCommand一字段overlay，gate真正全部22847runtimeSHA/55DATA+TOCSHA/5MachO+execbit/BuildID1511/links。原config/identifier/window/security/resourcesSHA不改、no execdeny放松；native行为仍未验|
|无身份adhoc资源签名|默认linkersignedApp资源未封装strictcheck失败|仅新Appsignature/resourceenvelope，same22847runtime原SHA保持；未调用developeridentity/真实Keychainitems/外部发布。真实Gatekeeper另验|

具体授权链/问题日志/OriginSHA在 Issue、Task_SCOPE、INPUT/SOURCE/BUILD_SOURCE/OUTPUT seals、evidence与实际logs。CEO普通Ownerdelegation与exactscope并行；本交接不自封Owner acceptance。

## 已记录失败与守卫证据

- 初guard `/bin/true` / `/usr/local/bin/python3`路径不存在，以及default-deny连echo/Python134（具体原因UNKNOWN）保留；改标准进程操作但保留精确file/network/private/DB/targetdenial。
- 旧probeprofile未独立预捕获，后来逆向重建SHA与当时record一致，明确不是independentpre-capture。最终guard `9413282ba2b321ac92eb1f163690a2fbec89012220adcfb6d232191261ba21e2` 同SHA新probe实际exit0：21929loopbackconnect errno1、futureexactDBwrite拒绝、syntheticunlistedreporead拒绝；没有读取保护DB作测试。currentguard/profile及03probe独立封存。
- runtime01 `.bin`物化丢相对解析，runtime02目录namespace丢Nextselfresolution，32内部filelinks+3dirlinks与新node_modulesnamespace修复，sourcebytes未改；oldmanifests/logs与repair records保留。
- runtime03publiclibrary denial、sidecars04私有宿主PyInstallercachedenial、Tauri01skiptest-x与execdeny冲突、初签名资源envelope失败均actualstderr/exit保留；不把warnings/fallback当PASS。失败workspace03/04work/dist/spec及相关beforebytes保留。
- Cargo actual mac metadata --offline--frozen exit0/246packages；初418lock168platformarchive缺失presence不能推断hostoffline无法build。完整Tauri02后来exit0。cargo.global-cache始终不存在，未授权SQLite init。仅未来唯一qa-root/data/curis.sqlite的拒写探针，文件不存在。

## 真实边界与下一 Gate

没有 App、Workspace、Gateway、Frontend server、Guardian target或Recovery执行；没有 UI/Browser/新fixture/当前DB fingerprint/Provider/费用/用户media/Keychain授权动作。NoGit mutation/Current/Pointer/Index/ChangeLog；no canonicalBlueprint/UI/layout/Settings变更。保护3DB/defaultApp目录不读写，未获取当前fingerprint，不能声称当前DBhash没变。守卫与有限probe是本轮隔离证据，不冒充全系统调用审计。

CG/Music ordinarypublishedactivation仍真实GAP，包内代码/候选测试不等于普通启用。SettingsprototypeWIP排除，现239formalfront是cutoff但不是全部FinalUI accepted；后续formalSettings接线另freshrebuild。实际Provider/权限/媒体导入/权益/经营结果未验证。ceo_evidence_api派生b_layer_pending_decisionsSQLite path未修/未创建，nextRuntime隔离scope决定。Writing persisted model-selection cold metadata误失效仅Ownerqueuedreadonlyaudit授权，不把推测作为已复现bug，也不修生产/重跑旧QA DB。

Owner独立 static inputs/outputs/config/签名验证 → 有限 BUILD_ONLY disposition → **单独 exact NATIVE_LAUNCH grant**，包括新guard/根/同DB/fixture/普通启用/Keychain边界、正常entry→Company/sevenareas/3domains/Sharedselection/candidate/confirmation/return→alltargets exit→same-root restart。已派发不是验收。本Taskseal后可按已授权开始新的Writing只读4files audit计划，仍不能改生产或执行repro。

## Task Output Manifest / Disposition

正式Issue：`/Users/yy/Documents/Curis AI Workspace/issues/CURIS-V1-FRESH-DESKTOP-INTEGRATION-001.md`；Review：`/Users/yy/Documents/Curis AI Workspace/docs/reviews/CURIS_V1_FRESH_DESKTOP_INTEGRATION_REVIEW.md`，StatusReview、REVIEW/EVIDENCE、REVIEW_REQUIRED。唯一code changed：`/Users/yy/Documents/Curis AI Workspace/desktop/scripts/build-runtime.sh`（fullpreimage+exact7inversecheck）。Task根 TASK_SCOPE/PLAN/INPUT_SEAL/SOURCE_SEAL/BUILD_SOURCE_SEAL/BUILD_OUTPUT_SEAL/HANDOFF/output-manifest 与evidence/logs/tests/guards各路径均retain REVIEW_REQUIRED；外部新App/source/publicdeps/cache/generated/failedretained输出逐regular及link清单SHA在output-manifest，未PROMOTE/ARCHIVE/DELETE。manifest自身hash外部回Owner避免自引用。canonical/旧Taskseals全部保留原bytes，Pointer/Index不更新。NextGate如上。

Final closure: source489andpublic35409content0drift; publicRustsysroot/compiler/systemtool93readonlyfileSHAsrecorded (not fullSystem/SDKtreefingerprint). ExactknownownTauri/runnerPIDs no longer present; newTask/externalphysicalfiles SQLiteheaderscan0, solefutureDB/.globalcacheabsent; protectedcurrentDBnotread. Finalphysicaloutputmanifestregularfiles/links+hashes includesallgeneratedfailedoutputs andsignaturebeforebytes; selfSHA omittedandreturnedoutside.
