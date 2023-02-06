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

temp_value = 0;

layer_maximum = 0;

note_temp = 0;
sequence_temp = 0;




for tick, chord in pynbs41.read(root.filename):
    note_tick = [note.tick for note in chord]
    note_layer = [note.layer for note in chord]
    note_instrument = [note.instrument for note in chord]
    note_key = [note.key for note in chord]
    note_velocity = [note.velocity for note in chord]
    note_panning = [note.panning for note in chord] 
    note_pitch = [note.pitch for note in chord]
    
    if layer_maximum <= len(note_layer):      ##count the maximum chord length for every tick
        layer_maximum = len(note_layer)
    
    new_file.notes.extend([
        pynbs41.Note(round(note_tick[i]*(20/header.tempo)), note_layer[i], note_instrument[i], note_key[i], note_velocity[i], note_panning[i], note_pitch[i]) for i in range(len(note_key))
    ])

new_file.header.tempo = 20

new_file.save(file_name + '_20tickconverted' + '.nbs')




#open 20t/s converted nbs file

nbs2schematic_nbsfile = pynbs41.read(file_name + '_20tickconverted' + '.nbs')


"""
for tick, chord in nbs2schematic_nbsfile:
    note_tick = [note.tick for note in chord]
    note_layer = [note.layer for note in chord]
    note_instrument = [note.instrument for note in chord]
    note_key = [note.key for note in chord]
    
    layer_diff = [i for i in note_layer if i not in layer_respective]
    layer_respective = layer_diff + layer_respective

"""

#layer_respective_sorted = sorted(layer_respective) ##sort the layers in ascending order
#print("sorted layer numbers = ", layer_respective_sorted)

print("layer_maximum = ",layer_maximum)


"""
for x in sand_layers:
    if x in layer_respective_sorted:
        layer_respective_sorted.remove(x)

print("number of layers without sand = ", len(layer_respective_sorted))
""" ##sand layer sorting already done in line 72



"""
layers_rearranged = sand_layers + layer_respective_sorted ##rearrange the layer, put sand layers in front of the array
print("rearranged layer = ", layers_rearranged)
""" ##sand layer sorting already done in line 72

#layers_rearranged = layer_respective_sorted

songlength = nbs2schematic_nbsfile.header.song_length
print("length of the song = ", songlength)




#define minecraft blockstate

diamond_block = BlockState('minecraft:diamond_block')
cyan_concrete = BlockState('minecraft:cyan_concrete')
white_concrete = BlockState('minecraft:white_concrete')

prismarine_slab = BlockState('minecraft:prismarine_brick_slab', {'type' : 'top'})
prismarine_bricks = BlockState('minecraft:prismarine_bricks')
dark_prismarine_slab = BlockState('minecraft:dark_prismarine_slab', {'type' : 'top'})
repeater = BlockState('minecraft:repeater')
repeater_delay2 = BlockState('minecraft:repeater', {'delay' : '2'})
repeater_sideFacing = BlockState('minecraft:repeater', {'facing' : 'east'})
redstone = BlockState('minecraft:redstone_wire', {'east' : 'side', 'west' : 'side', 'north' : 'side', 'south' : 'side'})

#create the schematic

reg = Region(-4, -1, 0, 48, 19, songlength//2 + 11) 
schem = reg.as_schematic(name=file_name, author="euichan41", description="Made with nbs2schematic")


#load the starting platform schematic

schem1 = Schematic.load("startplatform_imp2_final.litematic")
reg1 = list(schem1.regions.values())[0]

for x in reg1.xrange():
    for y in reg1.yrange():
        for z in reg1.zrange():
            reg.setblock(x,y,z,reg1.getblock(x,y,z))
            

if layer_maximum>36:
    print("error! layer number over 36 is not compatible!")
    msg.showwarning("error","the layer number should be under 36!")
    sys.exit(0)

if layer_maximum==0:
    print("error! there must be at least 1 layer!")
    msg.showwarning("error","there must be at least 1 layer!")
    sys.exit(0)

if layer_maximum>0 and layer_maximum<=36:
    layer_case=math.ceil(layer_maximum/3)
    print("needed noteblock row number = ",layer_case) ## e.g. there will be 2 noteblock rows for 5 layers in nbs file (one row can cover 3 layers) => layer_case = 1


for i in range(0,layer_case):
    for j in range(0,(songlength//4)+1):
        if i == 0: ## middle_row1
            reg.setblock(16,0,j*2+4,prismarine_slab)
            reg.setblock(16,1,j*2+4,repeater_delay2)
            reg.setblock(16,0,j*2+5,dark_prismarine_slab)
            reg.setblock(16,1,j*2+5,prismarine_bricks)
            reg.setblock(15,0,j*2+5,prismarine_slab)
            reg.setblock(14,0,j*2+5,prismarine_slab)
            reg.setblock(14,1,j*2+5,prismarine_bricks)
            reg.setblock(15,1,j*2+5,repeater_sideFacing)
            
            reg.setblock(22,0,j*2+5,prismarine_slab)
            reg.setblock(22,1,j*2+5,repeater_delay2)
            reg.setblock(22,0,j*2+6,dark_prismarine_slab)
            reg.setblock(22,1,j*2+6,prismarine_bricks)
            reg.setblock(21,0,j*2+6,prismarine_slab)
            reg.setblock(20,0,j*2+6,prismarine_slab)
            reg.setblock(20,1,j*2+6,prismarine_bricks)
            reg.setblock(21,1,j*2+6,repeater_sideFacing)
            
            #reg.setblock(8,0,j*2+5,white_concrete)
            #reg.setblock(9,0,j*2+5,white_concrete)
            #reg.setblock(11,0,j*2+5,white_concrete)
            #reg.setblock(12,0,j*2+5,white_concrete)
            
            #reg.setblock(14,0,j*2+6,white_concrete)
            #reg.setblock(15,0,j*2+6,white_concrete)
            #reg.setblock(17,0,j*2+6,white_concrete)
            #reg.setblock(18,0,j*2+6,white_concrete)

        if i == 1: ##middle_row2
            reg.setblock(16,3,j*2+4,prismarine_slab)
            reg.setblock(16,4,j*2+4,repeater_delay2)
            reg.setblock(16,3,j*2+5,dark_prismarine_slab)
            reg.setblock(16,4,j*2+5,prismarine_bricks)
            reg.setblock(15,3,j*2+5,prismarine_slab)
            reg.setblock(14,3,j*2+5,prismarine_slab)
            reg.setblock(14,4,j*2+5,prismarine_bricks)
            reg.setblock(15,4,j*2+5,repeater_sideFacing)
            
            reg.setblock(22,3,j*2+5,prismarine_slab)
            reg.setblock(22,4,j*2+5,repeater_delay2)
            reg.setblock(22,3,j*2+6,dark_prismarine_slab)
            reg.setblock(22,4,j*2+6,prismarine_bricks)
            reg.setblock(21,3,j*2+6,prismarine_slab)
            reg.setblock(20,3,j*2+6,prismarine_slab)
            reg.setblock(20,4,j*2+6,prismarine_bricks)
            reg.setblock(21,4,j*2+6,repeater_sideFacing)
            
        if i == 2: ##right_row1
            reg.setblock(4,0,j*2+4,prismarine_slab)
            reg.setblock(4,1,j*2+4,repeater_delay2)
            reg.setblock(4,0,j*2+5,dark_prismarine_slab)
            reg.setblock(4,1,j*2+5,prismarine_bricks)
            reg.setblock(3,0,j*2+5,prismarine_slab)
            reg.setblock(2,0,j*2+5,prismarine_slab)
            reg.setblock(2,1,j*2+5,prismarine_bricks)
            reg.setblock(3,1,j*2+5,repeater_sideFacing)
            
            reg.setblock(10,0,j*2+5,prismarine_slab)
            reg.setblock(10,1,j*2+5,repeater_delay2)
            reg.setblock(10,0,j*2+6,dark_prismarine_slab)
            reg.setblock(10,1,j*2+6,prismarine_bricks)
            reg.setblock(9,0,j*2+6,prismarine_slab)
            reg.setblock(8,0,j*2+6,prismarine_slab)
            reg.setblock(8,1,j*2+6,prismarine_bricks)
            reg.setblock(9,1,j*2+6,repeater_sideFacing)
        
        if i == 3: ##left_row1
            reg.setblock(28,0,j*2+4,prismarine_slab)
            reg.setblock(28,1,j*2+4,repeater_delay2)
            reg.setblock(28,0,j*2+5,dark_prismarine_slab)
            reg.setblock(28,1,j*2+5,prismarine_bricks)
            reg.setblock(27,0,j*2+5,prismarine_slab)
            reg.setblock(26,0,j*2+5,prismarine_slab)
            reg.setblock(26,1,j*2+5,prismarine_bricks)
            reg.setblock(27,1,j*2+5,repeater_sideFacing)
            
            reg.setblock(34,0,j*2+5,prismarine_slab)
            reg.setblock(34,1,j*2+5,repeater_delay2)
            reg.setblock(34,0,j*2+6,dark_prismarine_slab)
            reg.setblock(34,1,j*2+6,prismarine_bricks)
            reg.setblock(33,0,j*2+6,prismarine_slab)
            reg.setblock(32,0,j*2+6,prismarine_slab)
            reg.setblock(32,1,j*2+6,prismarine_bricks)
            reg.setblock(33,1,j*2+6,repeater_sideFacing)
            
        if i == 4: ##right_row2
            reg.setblock(4,3,j*2+4,prismarine_slab)
            reg.setblock(4,4,j*2+4,repeater_delay2)
            reg.setblock(4,3,j*2+5,dark_prismarine_slab)
            reg.setblock(4,4,j*2+5,prismarine_bricks)
            reg.setblock(3,3,j*2+5,prismarine_slab)
            reg.setblock(2,3,j*2+5,prismarine_slab)
            reg.setblock(2,4,j*2+5,prismarine_bricks)
            reg.setblock(3,4,j*2+5,repeater_sideFacing)
            
            reg.setblock(10,3,j*2+5,prismarine_slab)
            reg.setblock(10,4,j*2+5,repeater_delay2)
            reg.setblock(10,3,j*2+6,dark_prismarine_slab)
            reg.setblock(10,4,j*2+6,prismarine_bricks)
            reg.setblock(9,3,j*2+6,prismarine_slab)
            reg.setblock(8,3,j*2+6,prismarine_slab)
            reg.setblock(8,4,j*2+6,prismarine_bricks)
            reg.setblock(9,4,j*2+6,repeater_sideFacing)
        
        if i == 5: ##left_row2
            reg.setblock(28,3,j*2+4,prismarine_slab)
            reg.setblock(28,4,j*2+4,repeater_delay2)
            reg.setblock(28,3,j*2+5,dark_prismarine_slab)
            reg.setblock(28,4,j*2+5,prismarine_bricks)
            reg.setblock(27,3,j*2+5,prismarine_slab)
            reg.setblock(26,3,j*2+5,prismarine_slab)
            reg.setblock(26,4,j*2+5,prismarine_bricks)
            reg.setblock(27,4,j*2+5,repeater_sideFacing)
            
            reg.setblock(34,3,j*2+5,prismarine_slab)
            reg.setblock(34,4,j*2+5,repeater_delay2)
            reg.setblock(34,3,j*2+6,dark_prismarine_slab)
            reg.setblock(34,4,j*2+6,prismarine_bricks)
            reg.setblock(33,3,j*2+6,prismarine_slab)
            reg.setblock(32,3,j*2+6,prismarine_slab)
            reg.setblock(32,4,j*2+6,prismarine_bricks)
            reg.setblock(33,4,j*2+6,repeater_sideFacing)
            
        if i == 6: ##right_row3
            reg.setblock(4,6,j*2+4,prismarine_slab)
            reg.setblock(4,7,j*2+4,repeater_delay2)
            reg.setblock(4,6,j*2+5,dark_prismarine_slab)
            reg.setblock(4,7,j*2+5,prismarine_bricks)
            reg.setblock(3,6,j*2+5,prismarine_slab)
            reg.setblock(2,6,j*2+5,prismarine_slab)
            reg.setblock(2,7,j*2+5,prismarine_bricks)
            reg.setblock(3,7,j*2+5,repeater_sideFacing)
            
            reg.setblock(10,6,j*2+5,prismarine_slab)
            reg.setblock(10,7,j*2+5,repeater_delay2)
            reg.setblock(10,6,j*2+6,dark_prismarine_slab)
            reg.setblock(10,7,j*2+6,prismarine_bricks)
            reg.setblock(9,6,j*2+6,prismarine_slab)
            reg.setblock(8,6,j*2+6,prismarine_slab)
            reg.setblock(8,7,j*2+6,prismarine_bricks)
            reg.setblock(9,7,j*2+6,repeater_sideFacing)
        
        if i == 7: ##left_row3
            reg.setblock(28,6,j*2+4,prismarine_slab)
            reg.setblock(28,7,j*2+4,repeater_delay2)
            reg.setblock(28,6,j*2+5,dark_prismarine_slab)
            reg.setblock(28,7,j*2+5,prismarine_bricks)
            reg.setblock(27,6,j*2+5,prismarine_slab)
            reg.setblock(26,6,j*2+5,prismarine_slab)
            reg.setblock(26,7,j*2+5,prismarine_bricks)
            reg.setblock(27,7,j*2+5,repeater_sideFacing)
            
            reg.setblock(34,6,j*2+5,prismarine_slab)
            reg.setblock(34,7,j*2+5,repeater_delay2)
            reg.setblock(34,6,j*2+6,dark_prismarine_slab)
            reg.setblock(34,7,j*2+6,prismarine_bricks)
            reg.setblock(33,6,j*2+6,prismarine_slab)
            reg.setblock(32,6,j*2+6,prismarine_slab)
            reg.setblock(32,7,j*2+6,prismarine_bricks)
            reg.setblock(33,7,j*2+6,repeater_sideFacing)
            
        if i == 8: ##right_row4
            reg.setblock(4,9,j*2+4,prismarine_slab)
            reg.setblock(4,10,j*2+4,repeater_delay2)
            reg.setblock(4,9,j*2+5,dark_prismarine_slab)
            reg.setblock(4,10,j*2+5,prismarine_bricks)
            reg.setblock(3,9,j*2+5,prismarine_slab)
            reg.setblock(2,9,j*2+5,prismarine_slab)
            reg.setblock(2,10,j*2+5,prismarine_bricks)
            reg.setblock(3,10,j*2+5,repeater_sideFacing)
            
            reg.setblock(10,9,j*2+5,prismarine_slab)
            reg.setblock(10,10,j*2+5,repeater_delay2)
            reg.setblock(10,9,j*2+6,dark_prismarine_slab)
            reg.setblock(10,10,j*2+6,prismarine_bricks)
            reg.setblock(9,9,j*2+6,prismarine_slab)
            reg.setblock(8,9,j*2+6,prismarine_slab)
            reg.setblock(8,10,j*2+6,prismarine_bricks)
            reg.setblock(9,10,j*2+6,repeater_sideFacing)
        
        if i == 9: ##left_row4
            reg.setblock(28,9,j*2+4,prismarine_slab)
            reg.setblock(28,10,j*2+4,repeater_delay2)
            reg.setblock(28,9,j*2+5,dark_prismarine_slab)
            reg.setblock(28,10,j*2+5,prismarine_bricks)
            reg.setblock(27,9,j*2+5,prismarine_slab)
            reg.setblock(26,9,j*2+5,prismarine_slab)
            reg.setblock(26,10,j*2+5,prismarine_bricks)
            reg.setblock(27,10,j*2+5,repeater_sideFacing)
            
            reg.setblock(34,9,j*2+5,prismarine_slab)
            reg.setblock(34,10,j*2+5,repeater_delay2)
            reg.setblock(34,9,j*2+6,dark_prismarine_slab)
            reg.setblock(34,10,j*2+6,prismarine_bricks)
            reg.setblock(33,9,j*2+6,prismarine_slab)
            reg.setblock(32,9,j*2+6,prismarine_slab)
            reg.setblock(32,10,j*2+6,prismarine_bricks)
            reg.setblock(33,10,j*2+6,repeater_sideFacing)
            
        if i == 10: ##right_row5
            reg.setblock(4,12,j*2+4,prismarine_slab)
            reg.setblock(4,13,j*2+4,repeater_delay2)
            reg.setblock(4,12,j*2+5,dark_prismarine_slab)
            reg.setblock(4,13,j*2+5,prismarine_bricks)
            reg.setblock(3,12,j*2+5,prismarine_slab)
            reg.setblock(2,12,j*2+5,prismarine_slab)
            reg.setblock(2,13,j*2+5,prismarine_bricks)
            reg.setblock(3,13,j*2+5,repeater_sideFacing)
            
            reg.setblock(10,12,j*2+5,prismarine_slab)
            reg.setblock(10,13,j*2+5,repeater_delay2)
            reg.setblock(10,12,j*2+6,dark_prismarine_slab)
            reg.setblock(10,13,j*2+6,prismarine_bricks)
            reg.setblock(9,12,j*2+6,prismarine_slab)
            reg.setblock(8,12,j*2+6,prismarine_slab)
            reg.setblock(8,13,j*2+6,prismarine_bricks)
            reg.setblock(9,13,j*2+6,repeater_sideFacing)
        
        if i == 11: ##left_row5
            reg.setblock(28,12,j*2+4,prismarine_slab)
            reg.setblock(28,13,j*2+4,repeater_delay2)
            reg.setblock(28,12,j*2+5,dark_prismarine_slab)
            reg.setblock(28,13,j*2+5,prismarine_bricks)
            reg.setblock(27,12,j*2+5,prismarine_slab)
            reg.setblock(26,12,j*2+5,prismarine_slab)
            reg.setblock(26,13,j*2+5,prismarine_bricks)
            reg.setblock(27,13,j*2+5,repeater_sideFacing)
            
            reg.setblock(34,12,j*2+5,prismarine_slab)
            reg.setblock(34,13,j*2+5,repeater_delay2)
            reg.setblock(34,12,j*2+6,dark_prismarine_slab)
            reg.setblock(34,13,j*2+6,prismarine_bricks)
            reg.setblock(33,12,j*2+6,prismarine_slab)
            reg.setblock(32,12,j*2+6,prismarine_slab)
            reg.setblock(32,13,j*2+6,prismarine_bricks)
            reg.setblock(33,13,j*2+6,repeater_sideFacing)
            

#create blocks for each notes in layers (if a layer contains snare drum(sand), it will be placed in middle_row1)

rowx = [16, 22, 16, 22, 4, 10, 28, 34, 4, 10, 28, 34, 4, 10, 28, 34, 4, 10, 28, 34, 4, 10, 28, 34] ##coordinate of noteblock placement
rowy = [2, 2, 5, 5, 2, 2, 2, 2, 5, 5, 5, 5, 8, 8, 8, 8, 11, 11, 11, 11, 14, 14, 14, 14]

noteblock_keys = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24']
noteblock_instruments = ['harp', 'bass', 'basedrum', 'snare', 'hat', 'guitar', 'flute', 'bell', 'chime', 'xylophone', 'iron_xylophone', 'cow_bell', 'didgeridoo', 'bit', 'banjo', 'pling']
noteblock_instruments_BlockState = [BlockState('minecraft:dirt'), BlockState('minecraft:oak_planks'), BlockState('minecraft:cobblestone'), BlockState('minecraft:sand'), BlockState('minecraft:glass'), BlockState('minecraft:white_wool'), BlockState('minecraft:clay'), BlockState('minecraft:gold_block'), BlockState('minecraft:packed_ice'), BlockState('minecraft:bone_block'), BlockState('minecraft:iron_block'), BlockState('minecraft:soul_sand'), BlockState('minecraft:pumpkin'), BlockState('minecraft:emerald_block'), BlockState('minecraft:hay_block'), BlockState('minecraft:glowstone')]

for tick, chord in nbs2schematic_nbsfile:
    note_tick = [note.tick for note in chord]
    note_layer = [note.layer for note in chord]
    note_instrument = [note.instrument for note in chord]
    note_key = [note.key for note in chord]
    
    sand_layers = []
    perc_layers = []
    layer_sequence =[]
    
    for x in range(len(note_layer)):  ##get the array of number 0 to (len(note_layer) - 1)
        layer_sequence.append(x)
    
    
    for i in range(len(layer_sequence)):
        if note_instrument[i] == 2 or note_instrument[i] == 4:
            if layer_sequence[i] not in perc_layers:
                perc_layers.append(layer_sequence[i])
    
    for i in range(len(layer_sequence)):
        if note_instrument[i] == 3:
            if layer_sequence[i] not in sand_layers:
                sand_layers.append(layer_sequence[i])
    
    for x in perc_layers:
        if x in layer_sequence:
            layer_sequence.remove(x)
    
    for x in sand_layers:
        if x in layer_sequence:
            layer_sequence.remove(x)
    
    if len(sand_layers) > 9:
        print("error! sand layer number over 3 is not compatible!")
        msg.showwarning("error","there must be maximum 3 layers of snare drum(sand)!")
        sys.exit(0)
    
    layer_rearranged = sand_layers + perc_layers + layer_sequence
    
    """
    for a in range(len(note_key)):
        if note_instrument[a] == 2 or note_instrument[a] == 3 or note_instrument[a] == 4:    ##if instrument is percussion(bassdrum or click), it goes to lower layers of schematic
            #note_temp = note_layer.pop(a)
            #note_layer.insert(0,note_temp)
            
            sequence_temp = layer_sequence.pop(a)
            layer_sequence.insert(0,sequence_temp)
            
    
    for b in range(len(note_key)):          ##if instrument is sand, it goes to the lowest layer of schematic
        if note_instrument[b] == 3:
            #note_temp = note_layer.pop(b)
            #note_layer.insert(0,note_temp)
            
            sequence_temp = layer_sequence.pop(b)
            layer_sequence.insert(0,sequence_temp)
            
            sand_layers = sand_layers + 1
    """
    print(sand_layers, perc_layers, layer_sequence, layer_rearranged)
    
    #for c in range(layer_maximum):
        #layer_sequence[c] = (layer_maximum - 1) - layer_sequence[c]
    
    #print(layer_sequence)
    
    for j in range(len(layer_rearranged)):
        for i in range(len(note_layer)):
            if i == layer_rearranged[j]:
                
                if j % 3 == 0:
                    if note_tick[i] % 4 == 0:
                        reg.setblock(rowx[(j//3)*2]+1, rowy[(j//3)*2], (note_tick[i]//2)+5, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                        reg.setblock(rowx[(j//3)*2]+1, rowy[(j//3)*2]-1, (note_tick[i]//2)+5, noteblock_instruments_BlockState[note_instrument[i]])
                        if note_instrument[i] == 3:
                            reg.setblock(rowx[(j//3)*2]+1, rowy[(j//3)*2]-2, (note_tick[i]//2)+5, prismarine_slab)
                        reg.setblock(rowx[(j//3)*2], rowy[(j//3)*2], (note_tick[i]//2)+5, redstone)
                    elif note_tick[i] % 4 == 1:
                        reg.setblock(rowx[(j//3)*2+1]+1, rowy[(j//3)*2+1], (note_tick[i]//2)+6, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                        reg.setblock(rowx[(j//3)*2+1]+1, rowy[(j//3)*2+1]-1, (note_tick[i]//2)+6, noteblock_instruments_BlockState[note_instrument[i]])
                        if note_instrument[i] == 3:
                            reg.setblock(rowx[(j//3)*2+1]+1, rowy[(j//3)*2+1]-2, (note_tick[i]//2)+6, prismarine_slab)
                        reg.setblock(rowx[(j//3)*2+1], rowy[(j//3)*2+1], (note_tick[i]//2)+6, redstone)
                    elif note_tick[i] % 4 == 2:
                        reg.setblock(rowx[(j//3)*2]-3, rowy[(j//3)*2+1], (note_tick[i]//2)+4, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                        reg.setblock(rowx[(j//3)*2]-3, rowy[(j//3)*2+1]-1, (note_tick[i]//2)+4, noteblock_instruments_BlockState[note_instrument[i]])
                        if note_instrument[i] == 3:
                            reg.setblock(rowx[(j//3)*2]-3, rowy[(j//3)*2+1]-2, (note_tick[i]//2)+4, prismarine_slab)
                        reg.setblock(rowx[(j//3)*2]-2, rowy[(j//3)*2+1], (note_tick[i]//2)+4, redstone)
                    elif note_tick[i] % 4 == 3:
                        reg.setblock(rowx[(j//3)*2+1]-3, rowy[(j//3)*2+1], (note_tick[i]//2)+5, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                        reg.setblock(rowx[(j//3)*2+1]-3, rowy[(j//3)*2+1]-1, (note_tick[i]//2)+5, noteblock_instruments_BlockState[note_instrument[i]])
                        if note_instrument[i] == 3:
                            reg.setblock(rowx[(j//3)*2+1]-3, rowy[(j//3)*2+1]-2, (note_tick[i]//2)+5, prismarine_slab)
                        reg.setblock(rowx[(j//3)*2+1]-2, rowy[(j//3)*2+1], (note_tick[i]//2)+5, redstone)
                if j % 3 == 1:
                    if note_tick[i] % 4 == 0:
                        reg.setblock(rowx[(j//3)*2]+2, rowy[(j//3)*2], (note_tick[i]//2)+5, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                        reg.setblock(rowx[(j//3)*2]+2, rowy[(j//3)*2]-1, (note_tick[i]//2)+5, noteblock_instruments_BlockState[note_instrument[i]])
                        if note_instrument[i] == 3:
                            reg.setblock(rowx[(j//3)*2]+2, rowy[(j//3)*2]-2, (note_tick[i]//2)+5, prismarine_slab)
                        reg.setblock(rowx[(j//3)*2], rowy[(j//3)*2], (note_tick[i]//2)+5, redstone)
                    elif note_tick[i] % 4 == 1:
                        reg.setblock(rowx[(j//3)*2+1]+2, rowy[(j//3)*2+1], (note_tick[i]//2)+6, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                        reg.setblock(rowx[(j//3)*2+1]+2, rowy[(j//3)*2+1]-1, (note_tick[i]//2)+6, noteblock_instruments_BlockState[note_instrument[i]])
                        if note_instrument[i] == 3:
                            reg.setblock(rowx[(j//3)*2+1]+2, rowy[(j//3)*2+1]-2, (note_tick[i]//2)+6, prismarine_slab)
                        reg.setblock(rowx[(j//3)*2+1], rowy[(j//3)*2+1], (note_tick[i]//2)+6, redstone)
                    elif note_tick[i] % 4 == 2:
                        reg.setblock(rowx[(j//3)*2]-4, rowy[(j//3)*2+1], (note_tick[i]//2)+4, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                        reg.setblock(rowx[(j//3)*2]-4, rowy[(j//3)*2+1]-1, (note_tick[i]//2)+4, noteblock_instruments_BlockState[note_instrument[i]])
                        if note_instrument[i] == 3:
                            reg.setblock(rowx[(j//3)*2]-4, rowy[(j//3)*2+1]-2, (note_tick[i]//2)+4, prismarine_slab)
                        reg.setblock(rowx[(j//3)*2]-2, rowy[(j//3)*2+1], (note_tick[i]//2)+4, redstone)
                    elif note_tick[i] % 4 == 3:
                        reg.setblock(rowx[(j//3)*2+1]-4, rowy[(j//3)*2+1], (note_tick[i]//2)+5, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                        reg.setblock(rowx[(j//3)*2+1]-4, rowy[(j//3)*2+1]-1, (note_tick[i]//2)+5, noteblock_instruments_BlockState[note_instrument[i]])
                        if note_instrument[i] == 3:
                            reg.setblock(rowx[(j//3)*2+1]-4, rowy[(j//3)*2+1]-2, (note_tick[i]//2)+5, prismarine_slab)
                        reg.setblock(rowx[(j//3)*2+1]-2, rowy[(j//3)*2+1], (note_tick[i]//2)+5, redstone)
                if j % 3 == 2:
                    if note_tick[i] % 4 == 0:
                        reg.setblock(rowx[(j//3)*2]+1, rowy[(j//3)*2], (note_tick[i]//2)+6, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                        reg.setblock(rowx[(j//3)*2]+1, rowy[(j//3)*2]-1, (note_tick[i]//2)+6, noteblock_instruments_BlockState[note_instrument[i]])
                        if note_instrument[i] == 3:
                            reg.setblock(rowx[(j//3)*2]+1, rowy[(j//3)*2]-2, (note_tick[i]//2)+6, prismarine_slab)
                        reg.setblock(rowx[(j//3)*2], rowy[(j//3)*2], (note_tick[i]//2)+5, redstone)
                    elif note_tick[i] % 4 == 1:
                        reg.setblock(rowx[(j//3)*2+1]+1, rowy[(j//3)*2+1], (note_tick[i]//2)+7, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                        reg.setblock(rowx[(j//3)*2+1]+1, rowy[(j//3)*2+1]-1, (note_tick[i]//2)+7, noteblock_instruments_BlockState[note_instrument[i]])
                        if note_instrument[i] == 3:
                            reg.setblock(rowx[(j//3)*2+1]+1, rowy[(j//3)*2+1]-2, (note_tick[i]//2)+7, prismarine_slab)
                        reg.setblock(rowx[(j//3)*2+1], rowy[(j//3)*2+1], (note_tick[i]//2)+6, redstone)
                    elif note_tick[i] % 4 == 2:
                        reg.setblock(rowx[(j//3)*2]-3, rowy[(j//3)*2+1], (note_tick[i]//2)+5, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                        reg.setblock(rowx[(j//3)*2]-3, rowy[(j//3)*2+1]-1, (note_tick[i]//2)+5, noteblock_instruments_BlockState[note_instrument[i]])
                        if note_instrument[i] == 3:
                            reg.setblock(rowx[(j//3)*2]-3, rowy[(j//3)*2+1]-2, (note_tick[i]//2)+5, prismarine_slab)
                        reg.setblock(rowx[(j//3)*2]-2, rowy[(j//3)*2+1], (note_tick[i]//2)+4, redstone)
                    elif note_tick[i] % 4 == 3:
                        reg.setblock(rowx[(j//3)*2+1]-3, rowy[(j//3)*2+1], (note_tick[i]//2)+6, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                        reg.setblock(rowx[(j//3)*2+1]-3, rowy[(j//3)*2+1]-1, (note_tick[i]//2)+6, noteblock_instruments_BlockState[note_instrument[i]])
                        if note_instrument[i] == 3:
                            reg.setblock(rowx[(j//3)*2+1]-3, rowy[(j//3)*2+1]-2, (note_tick[i]//2)+6, prismarine_slab)
                        reg.setblock(rowx[(j//3)*2+1]-2, rowy[(j//3)*2+1], (note_tick[i]//2)+5, redstone)
                        




################################
####################
##########

#save .litematic file

schem.save(file_name + ".litematic")
