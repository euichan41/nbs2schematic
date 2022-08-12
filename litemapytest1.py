from stat import SF_APPEND
import sys
import os
from pathlib import Path


from litemapy import Schematic, Region, BlockState

from tkinter import *
from tkinter import filedialog as filedialog
from tkinter import messagebox as msg



##define minecraft blockstate


##build


# Build the planet



##whole tick : smooth_stone


# Shortcut to create a schematic with a single region
reg = Region(0, 0, 0, 21, 21, 21)
schem = reg.as_schematic(name="Planet", author="SmylerMC", description="Made with litemapy")

# Create the block state we are going to use
block = BlockState("minecraft:light_blue_concrete")

# Build the planet
for x, y, z in reg.allblockpos():
    if round(((x-10)**2 + (y-10)**2 + (z-10)**2)**.5) <= 10:
        reg.setblock(x, y, z, block)
        
##reg.setblock(2,0,0,smooth_stone)
##reg.setblock(2,0,1,smooth_stone)
##reg.setblock(2,0,2,smooth_stone)
#3reg.setblock(2,0,3,smooth_stone)
##reg.setblock(3,0,0,smooth_stone)
##reg.setblock(4,0,0,smooth_stone)

# Save the schematic
schem.save("planet.litematic")

# Load the schematic and get its first region
schem = Schematic.load("planet.litematic")
reg = list(schem.regions.values())[0]

# Print out the basic shape
for x in reg.xrange():
    for z in reg.zrange():
        b = reg.getblock(x, 10, z)
        if b.blockid == "minecraft:air":
            print(" ", end="")
        else:
            print("#", end='')
    print()