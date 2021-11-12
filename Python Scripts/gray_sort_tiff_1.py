#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This function performs the following:
    1) Reads the Zeiss .tif files one at a time
    2) Turns the .tif files gray if they are not grayscale already
    3) Outputs the gray .tif files into folders labeled by z stack positions that can be used by TrackMate.
    
@author: alisasmacbook
"""

import os
import cv2
import tifffile

def gray_sort_tiff(working_dir, phase = 'h01', position_t = 100, position_z = 15, channel= 'Na', is_grey = 'No'):
    
    os.chdir(working_dir)
    path = working_dir
    file_name = os.path.basename(path)
    new_path = os.path.dirname(path)
    
    all_new_files = f'{new_path}/{file_name}_gray_stacks'
    try:
        os.mkdir(all_new_files)
    
    except:
        pass
        
    if channel == 'Na':
        channel = ''
    
    if phase == 'Na':
        phase = ''
            
    num_t_position = len(str(position_t))
    num_z_position = len(str(position_z))
    
    
    for t_position in range(1,position_t+1):
        for z_position in range(1,position_z+1):
            new_dir = f'{all_new_files}/{file_name}_{z_position}'
            try:
                os.mkdir(new_dir)
                
            except OSError as error:
                pass   

            t_position = str(t_position)
            z_position = str(z_position)

            if int(t_position) <= 9:
                if int(z_position) <= 9:
                    t = t_position.zfill(2)
                    z = z_position.zfill(2)
                    
                    file = f'{file_name}_{phase}t{t}z{z}{channel}.tif'
                    file_path = os.path.join(new_dir, file)
                    file_new = tifffile.imread(file)
                    
                    if is_grey == 'No':
                        file_new = cv2.cvtColor(file_new, cv2.COLOR_BGR2GRAY)
                        tifffile.imwrite(file_path, file_new, photometric='minisblack')
                    if is_grey == 'Yes':
                        tifffile.imwrite(file_path, file_new)

                if int(z_position) > 9:
                    t = t_position.zfill(2)
                    z = z_position.zfill(num_z_position)
                    
                    file = f'{file_name}_{phase}t{t}z{z}{channel}.tif'
                    file_path = os.path.join(new_dir, file)
                    file_new = tifffile.imread(file)
                    
                    if is_grey == 'No':
                        file_new = cv2.cvtColor(file_new, cv2.COLOR_BGR2GRAY)
                        tifffile.imwrite(file_path, file_new, photometric='minisblack')
                    
                    if is_grey == 'Yes':
                        tifffile.imwrite(file_path, file_new)

            if int(t_position) > 9:
                if int(z_position) <=9:
                    t = t_position.zfill(num_t_position)
                    z = z_position.zfill(2)
                    
                    file = f'{file_name}_{phase}t{t}z{z}{channel}.tif'
                    file_path = os.path.join(new_dir, file)
                    file_new = tifffile.imread(file)
                    
                    if is_grey == 'No':
                        file_new = cv2.cvtColor(file_new, cv2.COLOR_BGR2GRAY)
                        tifffile.imwrite(file_path, file_new, photometric='minisblack')
                        
                    if is_grey == 'Yes':
                        tifffile.imwrite(file_path, file_new)
                    

            if int(t_position) > 9:
                if int(z_position) > 9:
                    t = t_position.zfill(num_t_position)
                    z = z_position.zfill(num_z_position)
                    
                    file = f'{file_name}_{phase}t{t}z{z}{channel}.tif'
                    file_path = os.path.join(new_dir, file)
                    file_new = tifffile.imread(file)
                    
                    if is_grey == 'No':
                        file_new = cv2.cvtColor(file_new, cv2.COLOR_BGR2GRAY)
                        tifffile.imwrite(file_path, file_new, photometric='minisblack')
                        
                    if is_grey == 'Yes':
                        tifffile.imwrite(file_path, file_new)

