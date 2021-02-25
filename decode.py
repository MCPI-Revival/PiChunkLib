################################################################################
#                                                                              #
#  __  __ _____ ____   ____                 _                                  #
# |  \/  |  ___|  _ \ / ___| __ _ _ __ ___ (_)_ __   __ _                      #
# | |\/| | |_  | | | | |  _ / _` | '_ ` _ \| | '_ \ / _` |                     #
# | |  | |  _| | |_| | |_| | (_| | | | | | | | | | | (_| |                     #
# |_|  |_|_|   |____/ \____|\__,_|_| |_| |_|_|_| |_|\__, |                     #
#                                                    |___/                     #
# Copyright 2021 MFDGaming                                                     #
#                                                                              #
# Permission is hereby granted, free of charge, to any person                  #
# obtaining a copy of this software and associated documentation               #
# files (the "Software"), to deal in the Software without restriction,         #
# including without limitation the rights to use, copy, modify, merge,         #
# publish, distribute, sublicense, and/or sell copies of the Software,         #
# and to permit persons to whom the Software is furnished to do so,            #
# subject to the following conditions:                                         #
#                                                                              #
# The above copyright notice and this permission notice shall be included      #
# in all copies or substantial portions of the Software.                       #
#                                                                              #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR   #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,     #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER       #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING      #
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS #
# IN THE SOFTWARE.                                                             #
#                                                                              #
################################################################################

import struct

def split_to_sectors(data):
    offset = 0
    sectors = []
    while not len(data) <= offset:
        sectors.append(data[offset:offset + 4096])
        offset += 4096
    return sectors

def decode_index(data):
    if len(data) != 4096:
        return
    chunks_info = []
    for offset in range(0, 4096, 4):
        sc = data[offset] # The sector count of the chunk
        scfs = int.from_bytes(data[offset + 1:offset + 4], "little") # The count of sectors from the start
        chunks_info.append({"sc": sc, "scfs": scfs})
    return chunks_info

def decode_bpb(data): # Block per byte
    block_map = [[[0] * 128] * 16] * 16
    offset = 0
    x = 0
    z = 0
    y = 0
    while not len(data) <= offset:
        block_map[x][z][y] = data[offset]
        offset += 1
        if y == 127:
            z += 1
            y = 0
        if z == 15:
            x += 1
            z = 0
        if x == 15:
            break
        y += 1
    return block_map

def decode_bphb(data): # Block per half byte
    block_map = [[[0] * 128] * 16] * 16
    offset = 0
    x = 0
    z = 0
    y = 0
    while not len(data) <= offset:
        y1 = data[offset] & 0x0f
        y2 = data[offset] >> 4
        offset += 1
        for cy in [y1, y2]:
            block_map[x][z][y] = cy 
            if y == 127:
                z += 1
                y = 0
            if z == 15:
                x += 1
                z = 0
            if x == 15:
                break
            y += 1
    return block_map

def decode_cpb(data): # Chunk per byte
    chunk_map = [[0] * 16] * 16
    offset = 0
    x = 0
    z = 0
    while not len(data) <= offset:
        chunk_map[x][z] = data[offset]
        offset += 1
        if x == 15:
            z += 1
            x = 0
        if z == 15:
            break
        x += 1
    return chunk_map

def decode_chunks(data):
    sectors = split_to_sectors(data)
    index = decode_index(sectors[0])
    chunks = []
    for i in index:
        chunk_data = b"".join(sectors[i["scfs"]:i["scfs"] + i["sc"]])
        if chunk_data[:4] == b"\x04\x41\x01\x00": # Is a valid chunk?
            chunks.append({
                "blocks": decode_bpb(chunk_data[4:4 + 32768]),
                "data": decode_bphb(chunk_data[32772:32772 + 16384]),
                "skylight": decode_bphb(chunk_data[49156:49156 + 16384]),
                "blocklight": decode_bphb(chunk_data[65540:65540 + 16384]),
                "biomes": decode_cpb(chunk_data[81924:81924 + 256])
            })
    return chunks
