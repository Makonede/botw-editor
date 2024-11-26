#!/usr/bin/env python3
# -*- coding: utf_8 -*-

from itertools import batched

from game_data import GameData

VERSIONS = {
    0x24e2: '1.0.0',
    0x24ee: '1.1.x',
    0x2588: '1.2.0',
    0x29c0: '1.3.0',
    0x2a46: '1.3.1 - 1.3.2',
    0x3ef8: '1.3.3',
    0x3ef9: '1.3.4',
    0x471a: '1.4.x',
    0x471b: '1.5.0',
    0x471e: '1.6.0',
}


# Load a save file into a GameData object
def load_save() -> GameData:
    with open(input('Path to game_data.sav: '), 'rb') as save:
        # Discard end marker
        save = save.read()[:-0x4]

    # Read version and platform
    version_bytes = save[:0x4]
    version_switch = int.from_bytes(version_bytes, 'little')
    version_wii_u = int.from_bytes(version_bytes, 'big')
    version = min(version_switch, version_wii_u)
    is_switch = version = version_switch

    # Get flags
    save = save[0xc:]
    endianness = 'little' if is_switch else 'big'
    flags: list[tuple[int, bytes]] = [
        (int.from_bytes(flag[0], endianness), flag[1]) for flag in batched(map(
            bytes, batched(save, 0x4, strict=True)
        ), 2, strict=True)
    ]
    return GameData(version, is_switch, flags)


def main() -> None:
    save = load_save()
    print(
        f'{'Switch' if save.is_switch else 'Wii U'} {VERSIONS[save.version]}'
    )

    names = save.get_string(b'PorchItem', 0x40)
    values = save.get_s32(b'PorchItem_Value1')
    print(*(
        f'{name} x{value}' for name, value in zip(names, values)
    ), sep='\n')


if __name__ == '__main__': main()
