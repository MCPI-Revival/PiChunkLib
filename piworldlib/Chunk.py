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

from piworldlib.ChunkUtils import ChunkUtils

class Chunk:
    def __init__(self, x: int, z: int, blockData: list = [], data: list = [], skyLightData: list = [], blockLightData: list = [], biomeData: list = []) -> None:
        self.x: int = x
        self.y: int = y
        if len(blockData) == 0:
            self.resetBlockData()
        else:
            self.blockData: list = blockData
        if len(data) == 0:
            self.resetData()
        else:
            self.data: list = data
        if len(skyLightData) == 0:
            self.resetSkyLightData()
        else:
            self.skyLightData: list = skyLightData
        if len(blockLightData) == 0:
            self.resetBlockLightData()
        else:
            self.blockLightData: list = blockLightData
        if len(biomeData) == 0:
            self.resetBiomeData()
        else:
            self.biomeData: list = biomeData
                
    def resetBlockData(self) -> None:
        self.blockData: list = ChunkUtils.new3DArray(16, 16, 128)
            
    def resetData(self) -> None:
        self.data: list = ChunkUtils.new3DArray(16, 16, 128)
            
    def resetSkyLightData(self) -> None:
        self.skyLightData: list = ChunkUtils.new3DArray(16, 16, 128)
            
    def resetBlockLightData(self) -> None:
        self.blockLightData: list = ChunkUtils.new3DArray(16, 16, 128)
            
    def resetBiomeData(self) -> None:
        self.biomeData: list = ChunkUtils.new2DArray(16, 16)
            
    def resetAllData(self) -> None:
        self.resetBlockData()
        self.resetData()
        self.resetSkyLightData()
        self.resetBlockLightData()
        self.resetBiomeData()
                
    def setBlock(self, x: int, y: int, z: int, blockId: int) -> None:
        self.blockData[x + 127][z + 127][y + 64] = blockId
        
    def setData(self, x: int, y: int, z: int, data: int) -> None:
        self.data[x + 127][z + 127][y + 64] = data
        
    def setSkyLight(self, x: int, y: int, z: int, lightLevel: int) -> None:
        self.skyLightData[x + 127][z + 127][y + 64] = lightLevel
        
    def setBlockLight(self, x: int, y: int, z: int, lightLevel: int) -> None:
        self.blockLightData[x + 127][z + 127][y + 64] = lightLevel
        
    def setBiome(self, x: int, z: int, biome: int) -> None:
        self.biomeData[x + 127][z + 127] = biome
        
    def readBlockData(self, buffer: bytes):
        self.resetBlockData()
        offset = 0
        x = 0
        z = 0
        y = 0
        while not len(buffer) <= offset:
            self.blockData[x][z][y] = buffer[offset]
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
        
