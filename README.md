# CalciumImagingAnalysis
An open-source method for analysis of confocal calcium imaging with sparse cells

---

### Table of Contents

- [Installation](#installation)
- [Description](#description)
- [Input and Output File Organization](#input-and-output-file-organization)
	- [Sorting Organization Example A and B](#sorting-organization-example-a-and-b)
		- [Organization Example A](#organization-example-a)	
		- [Organization Example B](#organization-example-b) 	
	- [Fluorescence Extraction Organization Example C and D](#fluorescence-extraction-organization-example-c-and-d)
		- [Organization Example C](#organization-example-c)
		- [Organization Example D](#organization-example-d)
	- [Merging Organization Example E](#merging-organization-example-e)
		- [Organization Example E](#organization-example-e)
	- [Background List File](#background-list-file)
- [Code Documentation](#code-documentation)
	- [Sorting](#sorting)
	- [Fluorescence Extraction](#fluorescence-extraction)
	- [Merging](#merging)

---
## Installation
The Anaconda environment was downloaded to use these codes. Additionally these are the dependencies for this code. The following packages must be installed for the codes to work:

pip install opencv-python==4.4.0.42 tifffile imagecodecs

## Description

The following scripts are used to pre-process .tif files before running TrackMate, as well as to calculate and plot the change in fluorescence of neurons from the TrackMate output files for calcium imaging data. 

***Sorting Code (gray_sort_tiff_1)*:**
- gray_sort_tiff() has the following functions:
	- Reads the Zeiss .tif files one at a time
	- Turns the .tif files gray if they are not grayscale already
	- Outputs the gray .tif files into folders labeled by z stack positions that can be used by TrackMate. 

***Fluoresence Extraction Code (individual_dFoverF0_1)*:** 
- fluorescence_extract() has the following functions:
	- Combines MEAN_INTENSITY values from the All Spots statistics TrackMate output files for a single neuron.
	- Subtracts the background and finds the maximal value for each timepoint. 
	- Calculates the change in fluorescence (∆F/F<sub>0</sub>) and plots the ∆F/F<sub>0</sub> over time.
	- Outputs a .csv with the combined data and calculations, and a "Neuron Plots" folder containing the plot of the ∆F/F<sub>0</sub> as a .png into the "results" folder.

- loop_fluorescence_extract() has the following functions:
	- Runs fluorescence_extract() on all the neurons in a folder. This requires specific file structure as an input. Refer to the [Input and Output File Organization](#input-and-output-file-organization) section [Organization Example C](#organization-example-c).
	- Outputs .csv files and a "Neuron Plots" folder containing the plots into the "results" folder

***Merging Code (merge_dFoverF0_1)**:*
- merge_data() has the following functions:
	- Combines all the ∆F/F<sub>0</sub> values for each neuron in the folder into one file. This requires specific file structure as an input. Refer to the [Input and Output File Organization](#input-and-output-file-organization) section and [Organization Example E](#organization-example-e).
	- Calculates the average and SEM of ∆F/F<sub>0</sub> values and plots the average ∆F/F<sub>0</sub> over time.
	- Outputs "merged_data.csv" and "Average_dF_F0.png" into a "merged_data" folder within the "results" folder. 
---
## Input and Output File Organization
### Sorting Organization Example A and B

1) In the paper, Zeiss confocal is used as an example. It automatically saves the .tif file names identically to the folder they are in with a base name that you choose.
	- Therefore, the files in the folder will have the same name as the folder with “_h#t#z#c#.tif”, (where the # stands for a number) at the end of each file to identify the phase (h#), time point (t#), z-position (z#), and channel (c#) of each file. 
	- In order for this code to work, the original name of the folder must be kept, or if changed, the file folder name must be identical to the beginning of each file. 
		- For example, in the practice folder, files are saved as “Neuron0to2_h#t#z#c#.tif”, so the folder name is “Neuron0to2”.
  
2) Using other confocal microscopes that export .tif files:
	- The files must be exported as .tif. The naming systems are different for Nikon, Leica, Zeiss etc. 
	- If other confocal files are to be used with this code, the 4 lines in the code where the "_#h#t#z#c#.tif" is defined must be changed to match the system of the confocal export. For example if a file is exported as **Neuron0to2_Z#T#C1.tif**, the lines naming the file should be changed from:  
		``` python
			file = f'{file_name}_{phase}t{t}z{z}{channel}.tif'  
		```  
		to:
  
		``` python
			file = f'{file_name}_{phase}Z{z}T{t}{channel}.tif'  
			#where phase = ‘Na’ and channel = ‘C1’. 
		```  
  
		  
	- Another example if a file is exported as **Neuron0to2.lif t01z01.tif**, the lines naming the file should be changed to:  
		``` python
			file = f'{file_name} {phase}t{t}z{z}{channel}.tif'  
			#where phase = ‘Na’ and channel = ‘Na’ 
		``` 

3) The code turns the files gray if the is_gray parameter is set to ‘No’ and saves them into a new folder labeled with the file name and _gray_stacks one directory above (outside of the input folder) such that the original folder is never changed. 
	- If the is_gray parameter is set to ‘Yes’, a copy of the original file is saved into a new folder one directory above.
	- The practice set is named “Neuron0to2_gray_stacks” and has the z-position folders named “Neuron0to2_1”, “Neuron0to2_2” etc.	
	- Refer to [Organization Example A](#organization-example-a) for an example of how the files should be structured and [Organization Example B](#organization-example-b) for what the file structure looks like after execution.
 
#### Organization Example A: 
##### Set-up for gray_sort_tiff() :

```bash
├── Analysis
└── Neuron0to2
    ├── Neuron0to2_h01t01z01c2.tif
    ├── Neuron0to2_h01t01z02c2.tif
    ├── Neuron0to2_h01t01z03c2.tif
    ├── Neuron0to2_h01t01z04c2.tif
    ├── Neuron0to2_h01t01z05c2.tif
    ├── Neuron0to2_h01t01z06c2.tif
    ├── Neuron0to2_h01t01z07c2.tif
    ├── Neuron0to2_h01t02z01c2.tif
    ├── Neuron0to2_h01t02z02c2.tif
    ├── Neuron0to2_h01t02z03c2.tif
    ├── Neuron0to2_h01t02z04c2.tif
    ├── Neuron0to2_h01t02z05c2.tif
    ├── Neuron0to2_h01t02z06c2.tif
    ├── Neuron0to2_h01t01z07c2.tif
    ├── Neuron0to2_h01t03z01c2.tif
    ├── Neuron0to2_h01t03z02c2.tif
    ├── Neuron0to2_h01t03z03c2.tif
    ├── Neuron0to2_h01t03z04c2.tif
    ├── Neuron0to2_h01t03z05c2.tif
    ├── Neuron0to2_h01t03z06c2.tif
    └── Neuron0to2_h01t03z07c2.tif

```
#### Organization Example B: 
##### After gray_sort_tiff() is executed:


```bash
├── Analysis
├── Neuron0to2
└── Neuron0to2_gray_stacks
    ├── Neuron0to2_1
    │   ├── Neuron0to2_h01t01z01c2.tif
    │   ├── Neuron0to2_h01t02z01c2.tif
    │   └── Neuron0to2_h01t03z01c2.tif
    ├── Neuron0to2_2
    │   ├── Neuron0to2_h01t01z02c2.tif
    │   ├── Neuron0to2_h01t02z02c2.tif
    │   └── Neuron0to2_h01t03z02c2.tif
    ├── Neuron0to2_3
    │   ├── Neuron0to2_h01t01z03c2.tif
    │   ├── Neuron0to2_h01t02z03c2.tif
    │   └── Neuron0to2_h01t03z03c2.tif
    ├── Neuron0to2_4
    │   ├── Neuron0to2_h01t01z04c2.tif
    │   ├── Neuron0to2_h01t02z04c2.tif
    │   └── Neuron0to2_h01t03z04c2.tif
    ├── Neuron0to2_5
    │   ├── Neuron0to2_h01t01z05c2.tif
    │   ├── Neuron0to2_h01t02z05c2.tif
    │   └── Neuron0to2_h01t03z05c2.tif
    ├── Neuron0to2_6
    │   ├── Neuron0to2_h01t01z06c2.tif
    │   ├── Neuron0to2_h01t02z06c2.tif
    │   └── Neuron0to2_h01t03z06c2.tif
    └── Neuron0to2_7
        ├── Neuron0to2_h01t01z07c2.tif
	├── Neuron0to2_h01t02z07c2.tif
	└── Neuron0to2_h01t03z07c2.tif

```

### Fluorescence Extraction Organization Example C and D
1) The “All Spots statistics” files from TrackMate should be saved in the following format:
	- "Mean_Intensity#.csv", where # stands for the number of the z-position where values come from. 
		- For example, TrackMate “All Spots statistic” file for z-position 3 should be saved as “Mean_Intensity03.csv”. 
		- This way, the mean intensity values in each z-position can be tracked by replacing the general MEAN_INTENSITY column names with the file name “Mean_Intensity#” in the merged document.

2) If running multiple neurons together, the “Mean_Intensity#.csv” files for each neuron should be saved into a folder labeled “Neuron #”, where # stands for the number of the neuron. 
	- The first neuron in the set is always “Neuron 0”, the second is “Neuron 1” etc. [Organization Example C](#organization-example-c) and [Organization Example D](#organization-example-d) show an example of folder organization before and after execution respectively.

3) The loop_fluorescence_extraction() code will combine the mean intensity in the “Neuron #” folder into one file, calculate the maximal intensity for each time point and the change in fluorescence (∆F/F<sub>0</sub>) for that neuron, and output them to a “results” folder with the name “Neuron #.csv”
	- The default creates a folder named “results” in the directory where the “Neuron #” folders reside. 
		- In [Organization Example D](#organization-example-d), the “results” folder would be created in the “Analysis” folder. 
		- Within the “results” folder, there are the .csv files with the merged mean intensity and the ∆F/F<sub>0</sub> calculation labeled after each neuron. 
		- There is also a folder called “Neuron Plots” that will have the output plots for each ∆F/F<sub>0</sub> value.
	- A “results” folder can also be set to any location by setting the results_folder parameter. 

4) A “Background_list.csv” file must be present in the same folder as the “Neuron #” folders. 
	- The background_list has a column labeled “Neuron #” for each neuron and must have the background values for each z-positions. The number of z-positions for each neuron must equal to the number of “Mean_Intensity#.csv” files in each neuron folder. The columns must be in numerical order and must not skip values.  

5) Alternatively, you can run one neuron at a time using fluorescence_extraction(). This allows analysis from different folders. 
	- Instead of a “Background_list.csv”, the values for the background must be entered as a list into the background_averages parameter. 
	- If analyzing multiple neurons separately that belong to the same group, the output result should be set to a same folder so that the merging code can be easily implemented.

#### Organization Example C: 
##### Set-up for loop_fluorescence_extract()
``` bash
├── Analysis
│   ├── Background_list.csv
│   ├── Neuron 0
│   │   ├── Mean_Intensity_01.csv
│   │   ├── Mean_Intensity_02.csv
│   │   └── Mean_Intensity_03.csv
│   ├── Neuron 1
│   │   ├── Mean_Intensity_04.csv
│   │   ├── Mean_Intensity_05.csv
│   │   ├── Mean_Intensity_06.csv
│   │   └── Mean_Intensity_07.csv
│   └── Neuron 2
│       ├── Mean_Intensity_04.csv
│       ├── Mean_Intensity_05.csv
│       ├── Mean_Intensity_06.csv
│       └── Mean_Intensity_07.csv
├── Neuron0to2
└── Neuron0to2_gray_stacks
  
```
#### Organization Example D: 
##### After loop_fluorescence_extract() is executed:
``` bash
├── Analysis
│   ├── Background_list.csv
│   ├── Neuron 0
│   ├── Neuron 1
│   ├── Neuron 2
│   └── results
│       ├── Neuron 0.csv
│       ├── Neuron 1.csv
│       ├── Neuron 2.csv
│       └── Neuron Plots
│           ├── Neuron 0.png
│           ├── Neuron 1.png
│           └── Neuron 2.png
│   
├── Neuron0to2
└── Neuron0to2_gray_stacks
```  
### Merging Organization Example E
1) The merging code saves all the outputs to a “merged_data” folder which is automatically created within the “results” folder as seen in [Organization Example E](#organization-example-e). 
	- It then combines all the ∆F/F<sub>0</sub> columns from the “Neuron #.csv” files into one file and renames each column to match the “Neuron #.csv” file it came from. 
	- Next, it calculates the average and SEM of the ∆F/F<sub>0</sub> columns. 
	- This file is named “merged_data.csv” and is saved into the “merged_data” folder. 
2) The code also creates and saves a graph named Average_dF_F0.png which plots the average ∆F/F<sub>0</sub> with the position T into the “merged_data” folder. 
3) All the “Neuron #.csv” files have to be in the same folder so the ∆F/F<sub>0</sub> of each neuron can be averaged and plotted.

#### Organization Example E: 
##### After merge_data() is executed:

``` bash
├── Analysis
│   ├── Background_list.csv
│   ├── Neuron 0
│   ├── Neuron 1
│   ├── Neuron 2
│   └── results
│       ├── merged_data
│       │   ├── Average_dF_F0.png
│       │   └── merged_data.csv
│       ├── Neuron 0.csv
│       ├── Neuron 1.csv
│       ├── Neuron 2.csv
│       └── Neuron Plots
├── Neuron0to2
└── Neuron0to2_gray_stacks
```  
### Background List File
1) The background values are entered into an excel file that is saved as a .csv. 
2) The excel file should have a column for each neuron labeled as “Neuron #”. Make sure there is no space after the number in the neuron, as the following "Neuron # " will show an error.
	- Each column must contain the background values for the z-positions being analyzed. 
	- The number of background values must match the number of “Mean_Intensity#.csv” files in each neuron folder.
		- For example, in "Practice 3", there are 3 neuron folders in “Analysis”, “Neuron 0” with 3 “Mean_Intensity#.csv” files, “Neuron 1” with 4 “Mean_Intensity#.csv”, and “Neuron 2” with 4 “Mean_Intensity#.csv” files. 
		- The “Background_list.csv” would look like the following. Note, since “Neuron 1” and “Neuron 2” appear in the same z-positions, the background values are the same.  
		  
			|Neuron 0|Neuron 1|Neuron 2|
			|--------------|---------------|---------------|
			|1.978       |  1.084       |  1.084       |
			|2.435       |  1.150       |  1.150       |
			|2.335       |  0.430       |  0.430       |
			|            |   0.297      |   0.297      |
 ----------------
  
## Code Documentation

### Sorting:

#### gray_sort_tiff(*working_dir, num_z_stacks=15,num_t_position=100, channel= 'c2'*)  
  
1) Creates a folder for each z-position.
2) Turns images grayscale.
3) Saves grayscale images into the correct z-position folder.
  
#### Parameters
<dl>
	<dt>working_dir: path object or file-like object</dt> 
		<dd>A string path (location) of the folder: all the images that will be sorted and turned gray.</dd>
		<dd>When loading the file location into the function, make sure that there is no "/" or “\” after the folder name or it will not read the file name properly. For example:</dd>
		<dd>This is wrong: '/Users/nilabuser/Desktop/Practice/'</dd>
		<dd>This is correct: '/Users/nilabuser/Desktop/Practice'</dd>
	<dt>phase: str, default ‘h01’</dt> 
		<dd>Set the phase if it exists. You can sort files by the phase name but only one phase at a time. The code must be separately run with each different phase name.The folders created by the script should be edited to add phase name upon completion. If the folder name is not edited, the z-position folders will have timepoints for all phases in them. </dd>
		<dd>The default parameter is set to 'Na'. If there is no phase in the name (starting with h), the parameter should be set "phase='Na'" (default). This is used for the following file names:</dd>
		<dd>Neuron0to2_ t#z#.tif</dd>
		<dd>To include the phase name, set the parameter “phase=‘h#’”. For example, if the files are Neuron0to2_h01t#z#c#.tif, set the phase parameter as "phase = 'h01'".</dd>
	<dt>position_t: int, default 100</dt>
		<dd>Set the position_t to the number of timepoints in the time-lapse.</dd>
		<dd>A number smaller than the actual number of timepoints can be used to sort less images. The first image sorted will always be timepoint 1. This method does not allow for using a subset of images that doesn’t incorporate the first image.</dd> 
	<dt>position_z: int, default 15</dt>
		<dd>Set the position_z to the number of z-positions in the stack.</dd>
		<dd>A number smaller than the actual number of z-positions can be used to sort less images. The first image sorted will always be z-position 1. This method does not allow for using a subset of images that doesn’t incorporate the first z-position.</dd>
	<dt>channel: str, default ‘Na’</dt>
		<dd>Set the channel if it exists.You can sort files by the channel but only one channel at a time. The code must be separately run with each different channel name.The folders created by the script should be edited to add channel name upon completion. If the folder name is not edited, the z-position folders will have timepoints for all channels in them. </dd> 
		<dd>The default parameter is set to Na. If there is no channel at the end of the name, parameter should be set "channel='Na'" (default). This is used for the following file names:</dd>
		<dd>Neuron0to2_h#t#z#.tif</dd>
		<dd>To include the channel name, set the parameter as the following “channel=‘c#’”. For example, if the files are Neuron0to2_h#t#z#c3.tif, set the channel parameter as "channel = 'c3'".</dd>
	<dt>is_gray: str, default ‘No’</dt>
		<dd>Describe whether the .tif files are grayscale. If they are grayscale, “is_gray = ‘Yes’” or they are not grayscale, “is_gray = ‘No’”.</dd>
		<dd>The default is “is_gray = ‘No’” and this will turn the files grayscale for TrackMate use.</dd>
</dl>

### Fluorescence Extraction:
#### fluorescence_extract(*working_dir, results_folder = 'results', trial_name = 'Neuron', position_t=100, background_averages=[1]*)  
  
1) Default: Creates a “results” folder in the same directory as the folder of the neuron. The results_folder parameter can be changed to create a folder in a different location or with a different name. 
2) Merges all the “Mean_Intensity#.csv” files for the neuron based on the POSITION_T and MEAN_INTENSITY columns. 
3) Renames the MEAN_INTENSITY columns to the matching Mean_Intensity# and keeps track of the timepoint that the values come from. Missing values are left blank. 
4) Subtracts the background values based on the background_averages inputted list. The background_averages list must be the same length as number of “Mean_Intensity#.csv” files. 
5) Finds the maximal value for each timepoint from the Mean_Intensity columns.
6) Calculates the ∆F/F<sub>0</sub> columns for the given neuron based on the first maximal value found.
7) Saves the file as the "trial_name".csv in the “results” folder. The default is "trial_name = 'Neuron'" making the default output file "Neuron.csv".
8) Plots ∆F/F<sub>0</sub> against the POSITION_T and uses the "trial_name" parameter as the title. The output file is saved as "trial_name".png. The default is "trial_name = 'Neuron'" making the default output "Neuron.png".
  
#### Parameters
<dl>
	<dt>working_dir: path object or file-like object</dt> 
		<dd>A string path (location) of the folder neuron folder is.</dd>
		<dd>When loading the file location into the function make sure that there is no "/" or “\” after the folder name or it will not read the file name properly. For example:</dd>
		<dd>This is wrong: '/Users/nilabuser/Desktop/Example/Neurons_to_analyze/Neuron 0/'</dd>
		<dd>This is correct: '/Users/nilabuser/Desktop/Example/Neurons_to_analyze/Neuron 0’</dd>
	<dt> results_folder: str, default ‘results’</dt>
		<dd>Set the location the output files are saved. The default creates a “results” folder in the same folder that contains the “Neuron #” folders. The location can be set, and if the folder does not exist, it will be created.</dd>
	<dt>trial_name: str, default ‘Neuron’<dt/>
		<dd>Set the name of the output .csv and .png file. This will also be the title of the ∆F/F0 plot.</dd>
	<dt>position_t:  int, default 100<dt/>
		<dd>Set the number of time points (given by the POSITION_T column in the “Mean _Intensity#.csv file) to be analyzed and merged in each time point. This can be set to less than the actual number of time points that are in the .csv files.</dd> 
		<dd>Set the actual number time points there are. For example, the number of time points is 100 which has time points 0-99 in the Mean_Intensity#.csv file. Set 100 as the number of frames.</dd>
	<dt>background_averages:  list of int, default [1]<dt/>
		<dd>Set the background values for each column. Therefore, the number of background values given must equal to the number of “Mean_Intensity#.csv” files in the folder. The background values must be given in a list (annotated by brackets []). So, if you have 3 columns with the same background average of 2.5, your parameter will look like this:</dd>
		<dd>background_averages = [2.5, 2.5, 2.5]</dd>
		<dd>The default is set to one column (one .csv file) with 1 as the background_average.</dd> 
</dl>

#### loop_fluorescence_extract(*working_dir, background_list, result_folder = 'results',  number_of_position_t=100*)  

1) Default: Creates a “results” folder in the same directory as "Neuron #" folders. The results_folder parameter can be changed to create a folder in a different location or with a different name. 
2) Merges all the Mean_Intensity#.csv files for each "Neuron #" folder based on the POSITION_T and MEAN_INTENSITY columns. 
3) Renames the MEAN_INTENSITY columns to the matching Mean_Intensity# and keeps track of the time point that the values come from. Missing values are left blank.
4) Subtracts the background values based on each "Background_list.csv" column. The "Backgroung_list.csv" columns must be the same length as number of "Mean_Intensity#.csv" files for each neuron. The labeling must be in order starting with "Neuron 0" and cannot have skipped numbers.
5) Finds the maximal value for each timepoint from the Mean_Intensity# columns.
6) Calculates the ∆F/F<sub>0</sub> columns for each "Neuron #" folder based on the first maximal value found.
7) Saves the file in the "results" folder with the following format “Neuron #.csv” 
8) Creates a graph of the ∆F/F<sub>0</sub> with POSITION_T and "Neuron #" as the title. The graph is saved as "Neuron #.png".
 
#### Parameters
<dl>
	<dt>working_dir: path object or file-like object</dt> 
		<dd>A string path (location) of the folder all the Neuron # folders are.<dd> 
		<dd>When loading the file location into the function make sure that there is no "/" or "\" after the folder name or it will not read the file name properly. For example:</dd>
		<dd>This is wrong: '/Users/nilabuser/Desktop/Example/Neurons_to_analyze/ '</dd>
		<dd>This is correct: '/Users/nilabuser/Desktop/Example/Neurons_to_analyze’</dd>
	<dt>background_list:  path object or file-like object</dt>
		<dd>Set the path to the "Background_list.csv" file.</dd>
		<dd>The .csv file should have a column for every neuron in the working_dir. The number of background values given in each column must equal to the number of Mean_Intensity#.csv files in each neuron folder it pertains to. Each column labeled must be identical to the neuron it pertains to. 
For example, in "Practice 3" there are 3 neuron folders in "Analysis": "Neuron 0" with 3 "Mean_Intensity#.csv" files, "Neuron 1" with 4 "Mean_Intensity#.csv" files, and "Neuron 2" with 4 "Mean_Intensity#.csv" files. Note, since "Neuron 1" and "Neuron 2" appear in the same z-positions, the background values are the same. For an example of the Background_list.csv refer to the Background List File section:
</dl>
  
└── [Background List File](#background-list-file)
  
<dl>
	<dt>result_folder:  path object or file-like object, str, default ‘results’</dt>
		<dd>Set the location the output files are saved. The default creates a "results" folder in the same folder that contains the "Neuron #" folders. The location can be set, and if the folder does not exist, it will be created.</dd>
	<dt>number_of_position_t: int, default 100</dt>
	<dd>Set the number of time points (given by the POSITION_T column in the "Mean_Intensity,#.csv" files) to be analyzed and merged for each z-position. This can be set to less than the actual number of time points that are in the .csv files.</dd>
	<dd>Set the actual number time points there are. For example, the number of time points is 100 which has time points 0-99 in the Mean_Intensity#.csv file. Set 100 as the number of frames.</dd>
</dl>

### Merging:
#### merge_data(*results_folder , position_t=999, plot_title= ‘Average ∆F/F0’*)  
  
1) Creates a "merged_data" folder in the "results" folder.
2) Reads all the .csv files in the "results" folder.
3) Merges the ∆F/F<sub>0</sub> columns from each Neuron into one file and labels the column with the neuron name ("Neuron 0", "Neuron 1" etc.)
4) Calculates the average and SEM of ∆F/F<sub>0</sub> and saves a "merged_data.csv" file in the "merged_data" folder.
5) Creates and saves a plot for the average ∆F/F<sub>0</sub> over time in the "merged_data" folder as .png with the plot_title parameter as the name.
  
#### Parameters
<dl>
	<dt>results_folder, path object or file-like object</dt>
		<dd>A string path (location) of the folder all the "Neuron #.csv" files are.</dd> 
		<dd>When loading the file location into the function make sure that there is no "/" or "\" after the folder name or it will not read the file name properly. For example:</dd>
		<dd>This is wrong: '/Users/nilabuser/Desktop/Example/Neurons_to_analyze/results/'</dd>
		<dd>This is correct: '/Users/nilabuser/Desktop/Example/Neurons_to_analyze/results’</dd>
	<dt>position_t: int, default 999</dt>
		<dd>Set the number of time points (also given by the POSITION_T column in the "Mean_Intensity#.csv" file) to be analyzed and merged in each z-position. This can be set to less than the actual number of time points that are in the .csv files.</dd> 
		<dd>Set the actual number time points there are. For example, the number of time points is 100 which has time points 0-99 in the "Mean_Intensity#.csv" file. Set 100 as the number of frames.</dd>
	<dt>plot_title: str, default ‘Average ∆F/F0’</dt>
		<dd>Set the name of the title the output plot will have. This will also be the name of the .png file when it is saved.<dd>

