package dev.vox.lss.networking.server;

import com.mojang.datafixers.util.Pair;
import com.mojang.serialization.Codec;
import com.mojang.serialization.DataResult;
import com.mojang.serialization.DynamicOps;
import net.minecraft.world.level.block.state.BlockState;

/** Reads pre-26.3 region palettes as well as 26.3's compact/string and id/properties forms.
 * Raw region reads bypass vanilla DataFixers, so legacy field names must be normalized here.
 * Encoding always uses the current vanilla format; caller-owned tags are never mutated.
 */
final class CompatibleBlockStateCodec implements Codec<BlockState> {
    static final Codec<BlockState> INSTANCE = new CompatibleBlockStateCodec();

    @Override
    public <T> DataResult<Pair<BlockState, T>> decode(DynamicOps<T> ops, T input) {
        var map = ops.getMap(input).result();
        if (map.isPresent() && map.get().get("id") == null && map.get().get("Name") != null) {
            input = ops.createMap(map.get().entries().map(entry -> {
                String key = ops.getStringValue(entry.getFirst()).result().orElse("");
                return switch (key) {
                    case "Name" -> Pair.of(ops.createString("id"), entry.getSecond());
                    case "Properties" -> Pair.of(ops.createString("properties"), entry.getSecond());
                    default -> entry;
                };
            }));
        }
        return BlockState.CODEC.decode(ops, input);
    }

    @Override
    public <T> DataResult<T> encode(BlockState state, DynamicOps<T> ops, T prefix) {
        return BlockState.CODEC.encode(state, ops, prefix);
    }
}
