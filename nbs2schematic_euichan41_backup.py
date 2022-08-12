from stat import SF_APPEND
import sys
import os
import math
from pathlib import Path


import pynbs41
from litemapy import Schematic, Region, BlockState

from tkinter import *
from tkinter import filedialog as filedialog
from tkinter import messagebox as msg

#open file

root = Tk()
root.filename =  filedialog.askopenfilename(initialdir = r"C:\Users",title = "choose your file",filetypes = (("nbs files","*.nbs"),("all files","*.*")))
print (root.filename)

demo = pynbs41.read(root.filename)

header=demo.header
print (header.tempo)

file_path = root.filename
file_name = Path(file_path).stem
print(file_name)


new_file = pynbs41.new_file(song_name=file_name + '_20tickconverted')


#convert nbs file into 20t/s

layer_respective = [0]

for tick, chord in pynbs41.read(root.filename):
    note_tick = [note.tick for note in chord]
    note_layer = [note.layer for note in chord]
    note_instrument = [note.instrument for note in chord]
    note_key = [note.key for note in chord]
    note_velocity = [note.velocity for note in chord]
    note_panning = [note.panning for note in chord] 
    note_pitch = [note.pitch for note in chord]
    
    new_file.notes.extend([
        pynbs41.Note(round(note_tick[i]*(20/header.tempo)), note_layer[i], note_instrument[i], note_key[i], note_velocity[i], note_panning[i], note_pitch[i]) for i in range(len(note_key))
    ])

new_file.header.tempo = 20

new_file.save(file_name + '_20tickconverted' + '.nbs')


#open 20t/s converted nbs file

nbs2schematic_nbsfile = pynbs41.read(file_name + '_20tickconverted' + '.nbs')

for tick, chord in nbs2schematic_nbsfile:
    note_tick = [note.tick for note in chord]
    note_layer = [note.layer for note in chord]
    note_instrument = [note.instrument for note in chord]
    note_key = [note.key for note in chord]
    note_velocity = [note.velocity for note in chord]
    note_panning = [note.panning for note in chord] 
    note_pitch = [note.pitch for note in chord]
    
    layer_diff = [i for i in note_layer if i not in layer_respective]
    layer_respective = layer_diff + layer_respective
    
    print(note_tick, note_layer, note_instrument, note_key)

layer_respective_sorted = sorted(layer_respective)
print(layer_respective_sorted)
layer_number = len(layer_respective_sorted)
songlength = nbs2schematic_nbsfile.header.song_length
print("number of layers = ", layer_number)
print("length of the song = ", songlength)


#define minecraft blockstate

diamond_block = BlockState('minecraft:diamond_block')
cyan_concrete = BlockState('minecraft:cyan_concrete')
sea_lantern = BlockState('minecraft:sea_lantern')

prismarine_slab = BlockState('minecraft:prismarine_brick_slab', {'type' : 'top'})
prismarine_bricks = BlockState('minecraft:prismarine_bricks')
dark_prismarine_slab = BlockState('minecraft:dark_prismarine_slab', {'type' : 'top'})
repeater = BlockState('minecraft:repeater')
redstone = BlockState('minecraft:redstone_wire', {'east' : 'side', 'west' : 'side', 'north' : 'side', 'south' : 'side'})

#create the schematic

reg = Region(0, 0, 0, 27, 15, songlength*2 + 5) 
schem = reg.as_schematic(name=file_name, author="euichan41", description="Made with nbs2schematic")


#load the starting platform schematic

schem1 = Schematic.load("nbs2schematic_startingplatform.litematic")
reg1 = list(schem1.regions.values())[0]

for x in reg1.xrange():
    for y in reg1.yrange():
        for z in reg1.zrange():
            reg.setblock(x,y,z,reg1.getblock(x,y,z))
            

#calculate and create needed noteblock rows

if layer_number>48:
    print("error! layer number over 48 is not compatible!")
    msg.showwarning("error","the layer number should be under 48!")
    sys.exit(0)

if layer_number==0:
    print("error! there must be at least 1 layer!")
    msg.showwarning("error","there must be at least 1 layer!")
    sys.exit(0)

if layer_number>0 and layer_number<=48:
    layer_case=math.ceil(layer_number/4)
    print("needed noteblock row number = ",layer_case) ## e.g. there will be 2 noteblock rows for 5 layers in nbs file (one row can cover 4 layers) => layer_case = 2


#create blocks for each notes in layers (if a layer contains snare drum(sand), it will be placed in middle_row1 and upholded by sea lantern)

for tick, chord in nbs2schematic_nbsfile:
    
    
    
    note_tick = [note.tick for note in chord]
    note_layer = [note.layer for note in chord]
    note_instrument = [note.instrument for note in chord]
    note_key = [note.key for note in chord]
    note_velocity = [note.velocity for note in chord]
    note_panning = [note.panning for note in chord] 
    note_pitch = [note.pitch for note in chord]
    

for i in range(0,layer_case-1):
    for j in range(0,songlength):
        if i == 0: ## middle_row1
            reg.setblock(10,0,j*2+4,prismarine_slab)
            reg.setblock(10,1,j*2+4,repeater)
            reg.setblock(10,0,j*2+5,dark_prismarine_slab)
            reg.setblock(10,1,j*2+5,prismarine_bricks)
            reg.setblock(10,2,j*2+5,redstone)
            reg.setblock(9,1,j*2+5,cyan_concrete)
            reg.setblock(11,1,j*2+5,cyan_concrete)
            reg.setblock(9,2,j*2+5,diamond_block)
            reg.setblock(11,2,j*2+5,diamond_block)
            
            reg.setblock(16,0,j*2+5,prismarine_slab)
            reg.setblock(16,1,j*2+5,repeater)
            reg.setblock(16,0,j*2+6,dark_prismarine_slab)
            reg.setblock(16,1,j*2+6,prismarine_bricks)
            reg.setblock(16,2,j*2+6,redstone)
            reg.setblock(15,1,j*2+6,cyan_concrete)
            reg.setblock(17,1,j*2+6,cyan_concrete)
            reg.setblock(15,2,j*2+6,diamond_block)
            reg.setblock(17,2,j*2+6,diamond_block)

        if i == 1: ##middle_row2
            reg.setblock(10,3,j*2+4,prismarine_slab)
            reg.setblock(10,4,j*2+4,repeater)
            reg.setblock(10,3,j*2+5,dark_prismarine_slab)
            reg.setblock(10,4,j*2+5,prismarine_bricks)
            reg.setblock(10,5,j*2+5,redstone)
            reg.setblock(9,4,j*2+5,cyan_concrete)
            reg.setblock(11,4,j*2+5,cyan_concrete)
            reg.setblock(9,5,j*2+5,diamond_block)
            reg.setblock(11,5,j*2+5,diamond_block)
            
            reg.setblock(16,3,j*2+5,prismarine_slab)
            reg.setblock(16,4,j*2+5,repeater)
            reg.setblock(16,3,j*2+6,dark_prismarine_slab)
            reg.setblock(16,4,j*2+6,prismarine_bricks)
            reg.setblock(16,5,j*2+6,redstone)
            reg.setblock(15,4,j*2+6,cyan_concrete)
            reg.setblock(17,4,j*2+6,cyan_concrete)
            reg.setblock(15,5,j*2+6,diamond_block)
            reg.setblock(17,5,j*2+6,diamond_block)
            
        if i == 2: ##right_row1
            reg.setblock(2,0,j*2+4,prismarine_slab)
            reg.setblock(2,1,j*2+4,repeater)
            reg.setblock(2,0,j*2+5,dark_prismarine_slab)
            reg.setblock(2,1,j*2+5,prismarine_bricks)
            reg.setblock(2,2,j*2+5,redstone)
            reg.setblock(1,1,j*2+5,cyan_concrete)
            reg.setblock(3,1,j*2+5,cyan_concrete)
            reg.setblock(1,2,j*2+5,diamond_block)
            reg.setblock(3,2,j*2+5,diamond_block)
            
            reg.setblock(6,0,j*2+5,prismarine_slab)
            reg.setblock(6,1,j*2+5,repeater)
            reg.setblock(6,0,j*2+6,dark_prismarine_slab)
            reg.setblock(6,1,j*2+6,prismarine_bricks)
            reg.setblock(6,2,j*2+6,redstone)
            reg.setblock(5,1,j*2+6,cyan_concrete)
            reg.setblock(7,1,j*2+6,cyan_concrete)
            reg.setblock(5,2,j*2+6,diamond_block)
            reg.setblock(7,2,j*2+6,diamond_block)
        
        if i == 3: ##left_row1
            reg.setblock(20,0,j*2+4,prismarine_slab)
            reg.setblock(20,1,j*2+4,repeater)
            reg.setblock(20,0,j*2+5,dark_prismarine_slab)
            reg.setblock(20,1,j*2+5,prismarine_bricks)
            reg.setblock(20,2,j*2+5,redstone)
            reg.setblock(19,1,j*2+5,cyan_concrete)
            reg.setblock(21,1,j*2+5,cyan_concrete)
            reg.setblock(19,2,j*2+5,diamond_block)
            reg.setblock(21,2,j*2+5,diamond_block)
            
            
            reg.setblock(24,0,j*2+5,prismarine_slab)
            reg.setblock(24,1,j*2+5,repeater)
            reg.setblock(24,0,j*2+6,dark_prismarine_slab)
            reg.setblock(24,1,j*2+6,prismarine_bricks)
            reg.setblock(24,2,j*2+6,redstone)
            reg.setblock(23,1,j*2+6,cyan_concrete)
            reg.setblock(25,1,j*2+6,cyan_concrete)
            reg.setblock(23,2,j*2+6,diamond_block)
            reg.setblock(25,2,j*2+6,diamond_block)
            
        if i == 4: ##right_row2
            reg.setblock(2,3,j*2+4,prismarine_slab)
            reg.setblock(2,4,j*2+4,repeater)
            reg.setblock(2,3,j*2+5,dark_prismarine_slab)
            reg.setblock(2,4,j*2+5,prismarine_bricks)
            reg.setblock(2,5,j*2+5,redstone)
            reg.setblock(1,4,j*2+5,cyan_concrete)
            reg.setblock(3,4,j*2+5,cyan_concrete)
            reg.setblock(1,5,j*2+5,diamond_block)
            reg.setblock(3,5,j*2+5,diamond_block)
            
            reg.setblock(6,3,j*2+5,prismarine_slab)
            reg.setblock(6,4,j*2+5,repeater)
            reg.setblock(6,3,j*2+6,dark_prismarine_slab)
            reg.setblock(6,4,j*2+6,prismarine_bricks)
            reg.setblock(6,5,j*2+6,redstone)
            reg.setblock(5,4,j*2+6,cyan_concrete)
            reg.setblock(7,4,j*2+6,cyan_concrete)
            reg.setblock(5,5,j*2+6,diamond_block)
            reg.setblock(7,5,j*2+6,diamond_block)
        
        if i == 5: ##left_row2
            reg.setblock(20,3,j*2+4,prismarine_slab)
            reg.setblock(20,4,j*2+4,repeater)
            reg.setblock(20,3,j*2+5,dark_prismarine_slab)
            reg.setblock(20,4,j*2+5,prismarine_bricks)
            reg.setblock(20,5,j*2+5,redstone)
            reg.setblock(19,4,j*2+5,cyan_concrete)
            reg.setblock(21,4,j*2+5,cyan_concrete)
            reg.setblock(19,5,j*2+5,diamond_block)
            reg.setblock(21,5,j*2+5,diamond_block)
            
            reg.setblock(24,3,j*2+5,prismarine_slab)
            reg.setblock(24,4,j*2+5,repeater)
            reg.setblock(24,3,j*2+6,dark_prismarine_slab)
            reg.setblock(24,4,j*2+6,prismarine_bricks)
            reg.setblock(24,5,j*2+6,redstone)
            reg.setblock(23,4,j*2+6,cyan_concrete)
            reg.setblock(25,4,j*2+6,cyan_concrete)
            reg.setblock(23,5,j*2+6,diamond_block)
            reg.setblock(25,5,j*2+6,diamond_block)
            
        if i == 6: ##right_row3
            reg.setblock(2,6,j*2+4,prismarine_slab)
            reg.setblock(2,7,j*2+4,repeater)
            reg.setblock(2,6,j*2+5,dark_prismarine_slab)
            reg.setblock(2,7,j*2+5,prismarine_bricks)
            reg.setblock(2,8,j*2+5,redstone)
            reg.setblock(1,7,j*2+5,cyan_concrete)
            reg.setblock(3,7,j*2+5,cyan_concrete)
            reg.setblock(1,8,j*2+5,diamond_block)
            reg.setblock(3,8,j*2+5,diamond_block)
            
            reg.setblock(6,6,j*2+5,prismarine_slab)
            reg.setblock(6,7,j*2+5,repeater)
            reg.setblock(6,6,j*2+6,dark_prismarine_slab)
            reg.setblock(6,7,j*2+6,prismarine_bricks)
            reg.setblock(6,8,j*2+6,redstone)
            reg.setblock(5,7,j*2+6,cyan_concrete)
            reg.setblock(7,7,j*2+6,cyan_concrete)
            reg.setblock(5,8,j*2+6,diamond_block)
            reg.setblock(7,8,j*2+6,diamond_block)
        
        if i == 7: ##left_row3
            reg.setblock(20,6,j*2+4,prismarine_slab)
            reg.setblock(20,7,j*2+4,repeater)
            reg.setblock(20,6,j*2+5,dark_prismarine_slab)
            reg.setblock(20,7,j*2+5,prismarine_bricks)
            reg.setblock(20,8,j*2+5,redstone)
            reg.setblock(19,7,j*2+5,cyan_concrete)
            reg.setblock(21,7,j*2+5,cyan_concrete)
            reg.setblock(19,8,j*2+5,diamond_block)
            reg.setblock(21,8,j*2+5,diamond_block)
            
            reg.setblock(24,6,j*2+5,prismarine_slab)
            reg.setblock(24,7,j*2+5,repeater)
            reg.setblock(24,6,j*2+6,dark_prismarine_slab)
            reg.setblock(24,7,j*2+6,prismarine_bricks)
            reg.setblock(24,8,j*2+6,redstone)
            reg.setblock(23,7,j*2+6,cyan_concrete)
            reg.setblock(25,7,j*2+6,cyan_concrete)
            reg.setblock(23,8,j*2+6,diamond_block)
            reg.setblock(25,8,j*2+6,diamond_block)
            
        if i == 8: ##right_row4
            reg.setblock(2,9,j*2+4,prismarine_slab)
            reg.setblock(2,10,j*2+4,repeater)
            reg.setblock(2,9,j*2+5,dark_prismarine_slab)
            reg.setblock(2,10,j*2+5,prismarine_bricks)
            reg.setblock(2,11,j*2+5,redstone)
            reg.setblock(1,10,j*2+5,cyan_concrete)
            reg.setblock(3,10,j*2+5,cyan_concrete)
            reg.setblock(1,11,j*2+5,diamond_block)
            reg.setblock(3,11,j*2+5,diamond_block)
            
            reg.setblock(6,9,j*2+5,prismarine_slab)
            reg.setblock(6,10,j*2+5,repeater)
            reg.setblock(6,9,j*2+6,dark_prismarine_slab)
            reg.setblock(6,10,j*2+6,prismarine_bricks)
            reg.setblock(6,11,j*2+6,redstone)
            reg.setblock(5,10,j*2+6,cyan_concrete)
            reg.setblock(7,10,j*2+6,cyan_concrete)
            reg.setblock(5,11,j*2+6,diamond_block)
            reg.setblock(7,11,j*2+6,diamond_block)
        
        if i == 9: ##left_row4
            reg.setblock(20,9,j*2+4,prismarine_slab)
            reg.setblock(20,10,j*2+4,repeater)
            reg.setblock(20,9,j*2+5,dark_prismarine_slab)
            reg.setblock(20,10,j*2+5,prismarine_bricks)
            reg.setblock(20,11,j*2+5,redstone)
            reg.setblock(19,10,j*2+5,cyan_concrete)
            reg.setblock(21,10,j*2+5,cyan_concrete)
            reg.setblock(19,11,j*2+5,diamond_block)
            reg.setblock(21,11,j*2+5,diamond_block)
            
            reg.setblock(24,9,j*2+5,prismarine_slab)
            reg.setblock(24,10,j*2+5,repeater)
            reg.setblock(24,9,j*2+6,dark_prismarine_slab)
            reg.setblock(24,10,j*2+6,prismarine_bricks)
            reg.setblock(24,11,j*2+6,redstone)
            reg.setblock(23,10,j*2+6,cyan_concrete)
            reg.setblock(25,10,j*2+6,cyan_concrete)
            reg.setblock(23,11,j*2+6,diamond_block)
            reg.setblock(25,11,j*2+6,diamond_block)
            
        if i == 10: ##right_row4
            reg.setblock(2,12,j*2+4,prismarine_slab)
            reg.setblock(2,13,j*2+4,repeater)
            reg.setblock(2,12,j*2+5,dark_prismarine_slab)
            reg.setblock(2,13,j*2+5,prismarine_bricks)
            reg.setblock(2,14,j*2+5,redstone)
            reg.setblock(1,13,j*2+5,cyan_concrete)
            reg.setblock(3,13,j*2+5,cyan_concrete)
            reg.setblock(1,14,j*2+5,diamond_block)
            reg.setblock(3,14,j*2+5,diamond_block)
            
            reg.setblock(6,12,j*2+5,prismarine_slab)
            reg.setblock(6,13,j*2+5,repeater)
            reg.setblock(6,12,j*2+6,dark_prismarine_slab)
            reg.setblock(6,13,j*2+6,prismarine_bricks)
            reg.setblock(6,14,j*2+6,redstone)
            reg.setblock(5,13,j*2+6,cyan_concrete)
            reg.setblock(7,13,j*2+6,cyan_concrete)
            reg.setblock(5,14,j*2+6,diamond_block)
            reg.setblock(7,14,j*2+6,diamond_block)
        
        if i == 11: ##left_row4
            reg.setblock(20,12,j*2+4,prismarine_slab)
            reg.setblock(20,13,j*2+4,repeater)
            reg.setblock(20,12,j*2+5,dark_prismarine_slab)
            reg.setblock(20,13,j*2+5,prismarine_bricks)
            reg.setblock(20,14,j*2+5,redstone)
            reg.setblock(19,13,j*2+5,cyan_concrete)
            reg.setblock(21,13,j*2+5,cyan_concrete)
            reg.setblock(19,14,j*2+5,diamond_block)
            reg.setblock(21,14,j*2+5,diamond_block)
            
            reg.setblock(24,12,j*2+5,prismarine_slab)
            reg.setblock(24,13,j*2+5,repeater)
            reg.setblock(24,12,j*2+6,dark_prismarine_slab)
            reg.setblock(24,13,j*2+6,prismarine_bricks)
            reg.setblock(24,14,j*2+6,redstone)
            reg.setblock(23,13,j*2+6,cyan_concrete)
            reg.setblock(25,13,j*2+6,cyan_concrete)
            reg.setblock(23,14,j*2+6,diamond_block)
            reg.setblock(25,14,j*2+6,diamond_block)
            




schem.save(file_name + ".litematic")



# Load the schematic and get its first region

# Print out the basic shapes
for x in reg.xrange():
    for z in reg.zrange():
        b = reg.getblock(x, 0, z)
        if b.blockid == "minecraft:air":
            print(" ", end="")
        else:
            print("#", end='')
    print()
    
    