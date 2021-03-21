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
            self.blockData: list = ChunkUtils.new3DArray(16, 16, 128)
        else:
            self.blockData: list = blockData
        if len(data) == 0:
            self.data: list = ChunkUtils.new3DArray(16, 16, 128)
        else:
            self.data: list = data
        if len(skyLightData) == 0:
            self.skyLightData: list = ChunkUtils.new3DArray(16, 16, 128)
        else:
            self.skyLightData: list = skyLightData
        if len(blockLightData) == 0:
            self.blockLightData: list = ChunkUtils.new3DArray(16, 16, 128)
        else:
            self.blockLightData: list = blockLightData
        if len(biomeData) == 0:
            self.biomeData: list = ChunkUtils.new2DArray(16, 16)
        else:
            self.biomeData: list = biomeData
                
    def setBlock(self, x: int, y: int, z: int, blockId: int) -> None:
        self.blockData[x + 127][z + 127][y + 64] = blockId
        
    def setData(self, x: int, y: int, z: int, data: int) -> None:
        self.data[x + 127][z + 127][y + 64] = data
        
    def setSkyLight(self, x: int, y: int, z: int, lightLevel: int) -> None:
        self.skyLightData[x + 127][z + 127][y + 64] = lightLevel
        
    def setBlockLight(self, x: int, y: int, z: int, lightLevel: int) -> None:
        self.blockLightData[x + 127][z + 127][y + 64] = lightLevel
