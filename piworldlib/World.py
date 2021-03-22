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
        self.chunks: list = []
        x: int = -127
        z: int = -127
        for i in index:
            buffer: bytes = b"".join(sectors[i[1]:i[1] + i[0]])
            chunk: object = Chunk(x, z)
            if z == 127:
                x += 16
                z: int = -127
            if x == 127:
                break
            z += 16
            chunk.read(buffer)
            self.chunks.append(chunk)
            
    def getBlock(self, x: int, y: int, z: int) -> int:
        for chunk in self.chunks:
            if chunk.x <= x <= chunk.z and chunk.x <= z <= chunk.z:
                return chunk.getBlock(x, y, z)
        
    def getData(self, x: int, y: int, z: int) -> int:
        for chunk in self.chunks:
            if chunk.x <= x <= chunk.z and chunk.x <= z <= chunk.z:
                return chunk.getData(x, y, z)
        
    def getSkyLight(self, x: int, y: int, z: int) -> int:
        for chunk in self.chunks:
            if chunk.x <= x <= chunk.z and chunk.x <= z <= chunk.z:
                return chunk.getSkyLight(x, y, z)
        
    def getBlockLight(self, x: int, y: int, z: int) -> int:
        for chunk in self.chunks:
            if chunk.x <= x <= chunk.z and chunk.x <= z <= chunk.z:
                return chunk.getBlockLight(x, y, z)
        
    def getBiome(self, x: int, z: int) -> int:
        for chunk in self.chunks:
            if chunk.x <= x <= chunk.z and chunk.x <= z <= chunk.z:
                return chunk.getBiome(x, y, z)
                
    def setBlock(self, x: int, y: int, z: int, blockId: int) -> None:
        for chunk in self.chunks:
            if chunk.x <= x <= chunk.z and chunk.x <= z <= chunk.z:
                chunk.setBlock(x, y, z, blockId)
        
    def setData(self, x: int, y: int, z: int, data: int) -> None:
        for chunk in self.chunks:
            if chunk.x <= x <= chunk.z and chunk.x <= z <= chunk.z:
                chunk.setData(x, y, z, data)
        
    def setSkyLight(self, x: int, y: int, z: int, lightLevel: int) -> None:
        for chunk in self.chunks:
            if chunk.x <= x <= chunk.z and chunk.x <= z <= chunk.z:
                chunk.setSkyLight(x, y, z, lightLevel)
        
    def setBlockLight(self, x: int, y: int, z: int, lightLevel: int) -> None:
        for chunk in self.chunks:
            if chunk.x <= x <= chunk.z and chunk.x <= z <= chunk.z:
                chunk.setBlockLight(x, y, z, lightLevel)
        
    def setBiome(self, x: int, z: int, biome: int) -> None:
        for chunk in self.chunks:
            if chunk.x <= x <= chunk.z and chunk.x <= z <= chunk.z:
               chunk.setBiome(x, z, biome)
