package dev.vox.lss.networking.server;

import java.nio.file.Files;
import java.nio.file.Path;
import net.minecraft.SharedConstants;
import net.minecraft.server.Bootstrap;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

class PortNativeCorpusToolTest {
    @Test
    void captureVersionSpecificNativeCorpus() throws Exception {
        assumeTrue("true".equals(System.getenv("LSS_CAPTURE_NATIVE_CORPUS")), "explicit capture tool only");
        SharedConstants.tryDetectVersion();
        Bootstrap.bootStrap();
        var registry = CorpusRegistryAccess.build();
        var root = Path.of("src/test/resources");
        try (var fixtures = Files.list(root.resolve("v20-corpus"))) {
            for (var file : fixtures.filter(p -> p.toString().endsWith(".bin")).toList()) {
                // v20 deduplicates this palette; retain the original air/stone-only native
                // fixture to continue checking the deliberate collapse instead of erasing it.
                if (file.getFileName().toString().equals("duplicate-air.bin")) continue;
                var nativeBody = NbtSectionSerializer.fromV20(Files.readAllBytes(file), registry);
                Files.write(root.resolve("nbt-corpus").resolve(file.getFileName()), nativeBody);
            }
        }
    }
}
