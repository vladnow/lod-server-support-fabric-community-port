# LOD Server Support Community Port

Unofficial Fabric port of [VoX's LOD Server Support](https://github.com/VoX/lod-server-support) / Voxy Server Side 0.17.0 to Minecraft **26.3**.

The server streams distant terrain to participating clients. Clients use a separately installed Voxy renderer to display it beyond the normal server view distance. This project preserves upstream networking and mod ID `lss`.

## Install

Requirements: Minecraft 26.3, Java 25, Fabric Loader 0.19.5+, Fabric API 0.160.5+26.3.

Put **one** main JAR from `dist` in `mods` on the Fabric server and participating clients. Choose the VSS or LSS variant; do not install both or combine with upstream LSS/VSS. Obtain a compatible Voxy renderer separately for clients. The dedicated server does not need Voxy. Sodium 0.9.2 and Mod Menu 21.0.0-beta.1 are the client APIs used to compile this port.

- VSS commands: `/vsslod diag` on server, `/vss diag` on client.
- LSS commands: `/lsslod diag` on server, `/lss diag` on client.
- Edit the generated `config/vss-server-config.yaml` or `config/lss-server-config.yaml` and run the corresponding server `reload` command. Existing upstream configuration migration is preserved.

## Status

Experimental port. See [validation report](verification/TEST-REPORT.md) for completed checks and limitations. Compilation and automated tests do not by themselves prove every renderer, shader, anti-xray or chunk-system integration works.

## Build

Run `build.ps1 -JavaHome '<JDK 25 directory>'`. It stages the source under the Windows temporary directory to avoid Gradle worker failures on Cyrillic paths. The first build requires access to public dependency repositories. Outputs and SHA-256 hashes are copied to `dist`.

Linux/macOS or a Latin-only checkout: `./gradlew :fabric:build :common:test`. This fork builds Fabric only; the retained Paper/NeoForge sources are reference material.

## Credits and license

Original code: VoX. VSS branding: Xantha and VoX. MIT; retain [LICENSE](LICENSE) and [third-party notices](THIRD-PARTY-NOTICES). See [provenance](UPSTREAM.md) and [changes](CHANGELOG.md). This is an independent port without an endorsement by the original authors. The separate Voxy renderer is not included and has its own distribution terms.

[Пошаговая инструкция по публикации на русском](PUBLISHING.ru.md). Nothing has been uploaded by this preparation. AI assistance was used for the port and accompanying publication text.
