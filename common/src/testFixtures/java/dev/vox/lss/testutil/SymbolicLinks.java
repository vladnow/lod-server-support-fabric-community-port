package dev.vox.lss.testutil;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.FileSystemException;

/** Probe the OS capability before tests alter their fixture directories. */
public final class SymbolicLinks {
    private SymbolicLinks() {}

    public static boolean supported() throws IOException {
        var directory = Files.createTempDirectory("lss-symlink-probe-");
        var link = directory.resolve("link");
        try {
            Files.createSymbolicLink(link, directory);
            return true;
        } catch (FileSystemException exception) {
            if (System.getProperty("os.name", "").startsWith("Windows")) return false;
            throw exception;
        } catch (UnsupportedOperationException exception) {
            return false;
        } finally {
            Files.deleteIfExists(link);
            Files.delete(directory);
        }
    }
}
