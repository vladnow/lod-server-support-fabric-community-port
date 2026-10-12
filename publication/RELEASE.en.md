Unofficial experimental Fabric port of LOD Server Support / Voxy Server Side 0.17.0 to Minecraft 26.3.

Requirements: Java 25, Fabric Loader 0.19.5, Fabric API 0.160.5+26.3. Install one port JAR on the server and participating clients. A compatible Voxy renderer is required on clients for Voxy terrain rendering and is obtained separately.

Do not combine this JAR with another LSS/VSS build; both use mod ID `lss`. This release contains no Paper or NeoForge build.

Validation: 2,869 JUnit cases passed, 12 explicitly skipped; all 80 required server GameTests passed. Dedicated-server startup/diagnostics/SQLite/shutdown and client GameTests passed, including a separate local Voxy 26.3 + Sodium profile. See the included test report for the exact profile and remaining limitations. Keep this release marked as experimental/pre-release until your multiplayer and rendering acceptance checks pass.

Credits: VoX (upstream), Xantha (VSS branding). MIT license and third-party notices are included. AI assistance was used in preparing the port and release text.
