# 0.17.0-port.26.3.1

Independent Fabric port of LOD Server Support / Voxy Server Side 0.17.0 to Minecraft 26.3.

- Update Minecraft, Fabric API, Loader, Loom, Sodium and Mod Menu build dependencies.
- Restrict Minecraft metadata to the 26.3 line and update the metadata regression test.
- Build only the Fabric platform and shared library; preserve upstream protocol and mod ID `lss`.
- Use Gradle 9.6.1 and JDK 25 for builds and test execution; shared classes retain Java 21 bytecode.
- Adapt the far-player submission collector to 26.3 model UV mapping, item geometry, text backgrounds, separate crumbling overlays and translucent block-breaking submissions.
- Use the new pose rotation and section fade visibility APIs; preserve armor/glint depth tiers using 26.3 paletted trim textures.
- Adapt region-file access to its new read-only lookup flag; handle absent regions without creating empty files. Add a live regression check for this behavior.
- Preserve raw pre-26.3 region block palettes by translating legacy Name/Properties fields to the current id/properties codec, without modifying caller-owned NBT. Check both object and direct transcode paths with a waterlogged block.
- Move the diagnostic movement rejection hooks to 26.3's shared position-validation method while keeping and expiring the originating packet context.
- Adapt command-test sources and registry fixtures to the 26.3 APIs. Skip symbolic-link checks explicitly when the Windows user cannot create links; retain the checks on capable systems.
- Remove a hardware-dependent concurrency-test expectation that every fast store must drop deposits. Wait for a writer commit receipt before inspecting rows. Retain the no-torn-row, no-error and stored-or-counted-as-dropped invariants.

- Prepare terrain-independent empty-column test fixtures and version-specific native wire fixtures; keep semantic v20 fixtures unchanged.

Experimental release. Consult `verification/TEST-REPORT.md` before advertising tested features.
