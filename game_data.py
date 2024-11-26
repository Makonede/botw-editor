# -*- coding: utf_8 -*-

from dataclasses import dataclass
from itertools import batched, takewhile
from struct import unpack
from zlib import crc32


@dataclass
class GameData:
    version: int
    is_switch: bool
    flags: list[tuple[int, bytes]]

    # Get a flag
    def get_bytes(self, name: bytes) -> bytes: return b''.join(
        flag[1] for flag in self.flags if flag[0] == crc32(name)
    )
    def get_data(self, name: bytes, format: str) -> tuple:
        data = self.get_bytes(name)
        return unpack(
            f'{'<' if self.is_switch else '>'}{len(data) // 0x4}{format}', data
        )

    def get_bool(self, name: bytes) -> tuple[bool]:
        return self.get_data(name, '?')
    def get_s32(self, name: bytes) -> tuple[int]:
        return self.get_data(name, 'i')
    def get_f32(self, name: bytes) -> tuple[float]:
        return self.get_data(name, 'f')
    def get_string(self, name: bytes, length: int) -> tuple[str]:
        return [bytes(s).decode().rstrip('\0') for s in takewhile(
            any, batched(self.get_bytes(name), length, strict=True)
        )]
