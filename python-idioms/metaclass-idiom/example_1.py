"""
Example 1 — Plugin registration via RegistryMeta.
"""
from __future__ import annotations

from metaclass import Plugin, PluginA, PluginB


def load_plugin(name: str) -> Plugin:
    cls = Plugin.registry[name]
    return cls()


def main() -> None:
    print("Registered plugins:", list(Plugin.registry.keys()))

    for name in Plugin.registry:
        plugin = load_plugin(name)
        print(f"  {name}: {plugin.run()}")

    # Dynamically add a third plugin
    class PluginC(Plugin):
        def run(self) -> str:
            return "PluginC dynamically added"

    print("\nAfter adding PluginC:", list(Plugin.registry.keys()))
    print(load_plugin("PluginC").run())


if __name__ == "__main__":
    main()
