# LOD Server Support Community Port

An unofficial Minecraft 26.3 Fabric port of [LOD Server Support](https://github.com/VoX/lod-server-support), also distributed upstream as Voxy Server Side.

The server provides distant terrain to participating clients. Clients use Voxy to render that terrain beyond the normal server view distance. Install this mod and Fabric API on both sides; install a compatible Voxy renderer on the client separately. Voxy is not required on a dedicated server.

This port targets Minecraft 26.3, Fabric Loader 0.19.5 and Fabric API 0.160.5+26.3, using Java 25. It preserves the upstream `lss` mod ID, networking and configuration system. Do not install it alongside another LSS or VSS JAR.

Changes from upstream: Minecraft 26.3 dependencies, a bounded version requirement, Fabric-only build configuration and the API adaptations listed in the changelog. The upstream Paper and NeoForge platforms are not part of this release.

Treat this version as experimental. The release's test report describes completed automated checks and any unverified client integrations; a successful build alone does not establish full multiplayer or rendering compatibility.

Original project and copyright: VoX. Voxy Server Side branding: Xantha and VoX. This community port is not endorsed by those authors or the Voxy renderer author. Code is MIT-licensed; bundled libraries retain their notices. The Voxy renderer is a separate download and is not bundled.

AI assistance was used for the port and publication text. For Modrinth, apply the appropriate AI-content disclosure when using this page text.
