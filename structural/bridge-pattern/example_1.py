"""
Example 1 — Remote control + device.

The remote-control abstraction and device implementation vary independently.
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class Device(ABC):
    """Implementation: any controllable device."""

    @abstractmethod
    def is_enabled(self) -> bool: ...

    @abstractmethod
    def enable(self) -> None: ...

    @abstractmethod
    def disable(self) -> None: ...

    @abstractmethod
    def get_volume(self) -> int: ...

    @abstractmethod
    def set_volume(self, volume: int) -> None: ...

    @abstractmethod
    def get_channel(self) -> int: ...

    @abstractmethod
    def set_channel(self, channel: int) -> None: ...

    @abstractmethod
    def name(self) -> str: ...


class TV(Device):
    def __init__(self) -> None:
        self._on = False
        self._volume = 30
        self._channel = 1

    def is_enabled(self) -> bool:
        return self._on

    def enable(self) -> None:
        self._on = True

    def disable(self) -> None:
        self._on = False

    def get_volume(self) -> int:
        return self._volume

    def set_volume(self, volume: int) -> None:
        self._volume = max(0, min(100, volume))

    def get_channel(self) -> int:
        return self._channel

    def set_channel(self, channel: int) -> None:
        self._channel = channel

    def name(self) -> str:
        return "Samsung TV"


class Radio(Device):
    def __init__(self) -> None:
        self._on = False
        self._volume = 50
        self._channel = 87

    def is_enabled(self) -> bool:
        return self._on

    def enable(self) -> None:
        self._on = True

    def disable(self) -> None:
        self._on = False

    def get_volume(self) -> int:
        return self._volume

    def set_volume(self, volume: int) -> None:
        self._volume = max(0, min(100, volume))

    def get_channel(self) -> int:
        return self._channel

    def set_channel(self, channel: int) -> None:
        self._channel = channel

    def name(self) -> str:
        return "Sony Radio"


class RemoteControl:
    """Basic abstraction."""

    def __init__(self, device: Device) -> None:
        self.device = device

    def toggle_power(self) -> None:
        if self.device.is_enabled():
            self.device.disable()
        else:
            self.device.enable()

    def volume_up(self) -> None:
        self.device.set_volume(self.device.get_volume() + 10)

    def volume_down(self) -> None:
        self.device.set_volume(self.device.get_volume() - 10)

    def channel_up(self) -> None:
        self.device.set_channel(self.device.get_channel() + 1)


class AdvancedRemote(RemoteControl):
    """Refined abstraction with extra features."""

    def mute(self) -> None:
        self.device.set_volume(0)


def main() -> None:
    for device in (TV(), Radio()):
        remote = AdvancedRemote(device)
        remote.toggle_power()
        print(f"{device.name()} on: {device.is_enabled()}")
        remote.volume_up()
        print(f"{device.name()} volume: {device.get_volume()}")
        remote.mute()
        print(f"{device.name()} after mute: {device.get_volume()}")


if __name__ == "__main__":
    main()
