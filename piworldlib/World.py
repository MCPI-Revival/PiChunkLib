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

from piworldlib.Chunk import Chunk
from piworldlib.ChunkUtils import ChunkUtils

class World:
    def __init__(self, worldDir: str) -> None:
        self.chunksData = open(worldDir + "/chunks.dat", "rb").read()
        self.levelData = open(worldDir + "/level.dat", "rb").read()
        self.entitiesData = open(worldDir + "/entities.dat", "rb").read()
        self.read_chunks()

    def to_4KB_sectors(self, buffer: bytes) -> list:
        offset: int = 0
        sectors: list = []
        while not len(buffer) <= offset:
            sectors.append(buffer[offset:offset + 4096])
            offset += 4096
        return sectors
    
    def readChunksIndex(self, buffer: bytes) -> list:
        if len(buffer) != 4096:
            return
        index: list = []
        for offset in range(0, 4096, 4):
            chunkSize: int = buffer[offset]
            sectorIndex: int = int.from_bytes(buffer[offset + 1:offset + 4], "little")
            if chunkSize > 0 and sectorIndex > 0:
                index.append([chunkSize, sectorIndex])
        return index
    
    def read_chunks(self) -> None:
        sectors: list = self.to_4KB_sectors(self.chunksData)
        index: list = self.readChunksIndex(sectors[0])
        sqrtChunksCount: int = int(len(index) ** .5)
        self.chunks: list = ChunkUtils.new2DArray(32, 32)
        chunkX: int = 0
        chunkZ: int = 0
        for i in index:
            buffer: bytes = b"".join(sectors[i[1]:i[1] + i[0]])
            chunk: object = Chunk(chunkX, chunkZ)
            chunk.read(buffer)
            self.chunks[chunkX][chunkZ]: object = chunk
            if chunkZ == (sqrtChunksCount - 1):
                chunkX += 1
                chunkZ: int = 0
            if chunkX == (sqrtChunksCount - 1):
                break
            chunkZ += 1
