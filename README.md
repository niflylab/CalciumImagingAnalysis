# CalciumImagingAnalysis
An open-source method for analysis of confocal calcium imaging with sparse cells
The following codes are used to pre-process .tif files before running TrackMate, and to calculate and plot the change in fluorescence of neurons from the TrackMate output files for Calcium Imaging data. 

Sorting Code (gray_sort_tiff_1):
gray_sort_tiff() has the following functions:
-	Reads the Zeiss .tif files one at a time
-	Turns the .tif files gray if they are not grayscale already
-	Outputs  the gray .tif files into folders labeled by z stack and so TrackMate can be used. 

Fluoresence Extraction Code (individual_dFoverF0_1): 
fluorescence_extract() has the following functions:
-	Combines MEAN_INTENSITY values from the Spots Statistics TrackMate output files for a single neuron.
-	Subtracts the background, finds the maximum value for each timepoint 
-	Calculates the change in fluorescence (∆F/F0) and plots the ∆F/F0.
-	Outputs 2 files into the set results folder: the .csv with the combined data and calculations and the plot of the ∆F/F0 as a .png in a separate “Neuron Plots” folder within the results folder.

loop_fluorescence_extract() has the following functions:
-	Runs fluorescence_extract() on all the neurons in a folder. This requires specific file structure as an input. Refer to the Input and Output File Organization section and Organization Example C.
-	Outputs 2 files for each neuron into the set results folder: the .csv with the combined data and calculations and the plot of the ∆F/F0 as a .png in a separate “Neuron Plots” folder within the results folder

Merging Code (merge_dFoverF0_1):
merge_data() has the following functions:
-	Combines all the ∆F/F0 values for each neuron in the folder into one file. This requires specific file structure as an input. Refer to the Input and Output File Organization section and Organization Example E.
-	Calculates the average ∆F/F0 and the SEM and plots the Average ∆F/F0.
-	Outputs 2 files: merged_data.csv, and Average_dF_Fo.png into a merged_data folder within the results folder. 






Input and Output File organization

Sorting: Organization Example A and B

1)	In the paper, Zeiss confocal is used as an example. It automatically saves the file names identically to the folder they are in with a base name that you choose.
-	Therefore, the main folder will have the same name as all the files in the folder with "_h*t*z*c*.tif", (where the * stands for a number) at the end of each file to identify the phase (h*), time (t*), z position (z*), and channel (c*) of each file. 
-	In order for this code to work, the original name of the folder must be kept, or if moved, the file folder name must be identical to the beginning of each file. 
i.	For example, in the practice folder provided files are saved as Practice 3_h*t*z*c*.tif so the folder name is Practice 3.
2)	Using other confocal microscopes that export files differently than Zeiss:
a.	The files must be exported as .tif. The naming system is different for Nikon, Leica, Zeiss etc. 
b.	If other confocal files are to be used with this code, the 4 lines in the code where the _h*t*z*c*.tif is defined must be changed to match the naming system of the confocal export. For example if a file is exported as:
Practice 3_Z*T*C1.tif, the lines naming the file should be changed from:
file = f'{file_name}_{phase}t{t}z{z}{channel}.tif' 

to:
file = f'{file_name}_{phase}Z{z}T{t}{channel}.tif'
Where phase = ‘Na’ and channel = ‘C1’
c.	Another example if a file is exported as:
Practice.lif t01z01.tif, the lines naming the file should be changed to:
file = f'{file_name} {phase}t{t}z{z}{channel}.tif'
Where phase = ‘Na’ and channel = ‘Na’

3)	The code turns the files gray if the  is_gray parameter is set to ‘No’ and saves them into a new folder labeled with the file name and _gray_stacks one directory above (outside of the input folder) such that the original folder is never changed. 
-	If the is_gray parameter is set to ‘Yes’ a copy of the original file will be saved into a new folder one directory above.
-	The practice set is named Practice 3_gray_stacks and has the z stack folders named Practice 3_1","Practice 3_2" etc.
-	Refer to organization example A for how the files should be structured, and example B to what the file structure looks like after execution. 

Fluorescence Extraction: Organization Example C and D
1)	The All Spots Statistics files from TrackMate should be saved in the following format:
-	"Mean_Intensity*.csv", where * stands for the number of the z position these values came from. 
i.	For example, TrackMate All Spots Statistic file for z-stack 3 should be saved as Mean_Intensity03.csv. 
ii.	This way, the stack the mean intensity values came from can be tracked by replacing the general MEAN_INTENSITY column names with the file name Mean_Intensity* in the merged document.
2)	If running multiple neurons together, the Mean_Intensity*.csv files for each neuron should be saved into a folder labeled Neuron *, where * stands for the number of the neuron in the set the mean intensity belongs to. 
-	The first neuron in the set is always Neuron 0, the second is Neuron 1 etc. Organization Example C shows an example of folder organization.
3)	The loop_fluorescence_extraction() code will combine the mean intensity in the Neuron * folder into one file, calculate the maximum intensity for each and the change in fluorescence (∆F/F0) for that neuron, and output them to a results folder with the name “Neuron *.csv”
-	The default creates a folder named “results” in the directory the Neuron folders reside. 
i.	In Organization Example D, the results folder would be created in the Analysis folder. 
ii.	Within the results folder, there are the .csv files with the merged mean intensity and the ∆F/F0 calculation labeled after each neuron. 
iii.	There will also be a folder called “Neuron Plots” which will have the output plots for each ∆F/F0 value.
-	A results folder can also be set to any location by setting the results_folder parameter. 
4)	A background_list.csv file must be present in the same folder as the Neuron * folders. 
a.	The background_list has a column labeled Neuron * for each neuron and must have the background values for each z slice. The number of rows for each neuron must equal the number of Mean_Intensity*.csv files in each neuron folder. The columns must be in numerical order and must not skip values.  
5)	Alternatively, you can run one neuron at a time using fluorescence_extraction(). This allows analysis from different folders. 
-	Instead of a Background_list.csv, the values for the background are entered as a list into the background_averages parameter. 
-	If analyzing multiple neurons separately but part of the same group, the output result should be set to same folder so that the merging code will work and easily implemented.


Merging: Organization Example E

1)	The merging code saves all the outputs to a merged_data folder which is automatically created within the results folder (Organization Example E). 
-	It then combines all the ∆F/F0 columns from the Neuron *.csv files into one file and renames each column to match the Neuron *.csv file it came from. 
-	Next it calculates the average of the ∆F/F0 columns and the SEM. 
-	This file is named merged_data.csv and is saved into the merged_data folder. 
2)	The code also creates and saves a graph named Average_dF_F0.png which plots the Average ∆F/F0 with the Z stack as the x axis into the merged_data folder. 
3)	All the Neuron *.csv files have to be in the same folder so the ∆F/F0 of each can be averaged and plotted.

Organization Examples:

A. Set-up for gray_sort_tiff() :
--------------------------------------------------
Practice_3
Neuron0to2
Neuron0to2_ h01t01z01c2.tif	Neuron0to2_ h01t02z05c2.tif
Neuron0to2_ h01t01z02c2.tif 	Neuron0to2_ h01t02z06c2.tif
Neuron0to2_ h01t01z03c2.tif 	Neuron0to2_ h01t02z07c2.tif
Neuron0to2_ h01t01z04c2.tif 	Neuron0to2_ h01t03z01c2.tif
Neuron0to2_ h01t01z05c2.tif 	Neuron0to2_ h01t03z02c2.tif
Neuron0to2_ h01t01z06c2.tif 	Neuron0to2_ h01t03z03c2.tif
Neuron0to2_ h01t01z07c2.tif 	Neuron0to2_ h01t03z04c2.tif
Neuron0to2_ h01t02z01c2.tif 	Neuron0to2_ h01t03z05c2.tif
Neuron0to2_ h01t02z02c2.tif 	Neuron0to2_ h01t03z06c2.tif
Neuron0to2_ h01t02z03c2.tif 	Neuron0to2_ h01t03z07c2.tif
Neuron0to2_ h01t02z04c2.tif
--------------------------------------------------
B. After gray_sort_tiff() is executed:
--------------------------------------------------
Practice
Practice_gray_stacks
	Neuron0to2_1				Neuron0to2_5
		Neuron0to2_ h01t01z01c2.tif		Neuron0to2_ h01t01z05c2.tif
Neuron0to2_ h01t02z01c2.tif		Neuron0to2_ h01t01z05c2.tif
Neuron0to2_ h01t03z01c2.tif		Neuron0to2_ h01t01z05c2.tif
	Neuron0to2_2				Neuron0to2_6
Neuron0to2_ h01t01z02c2.tif		Neuron0to2_ h01t01z06c2.tif
Neuron0to2_ h01t02z02c2.tif		Neuron0to2_ h01t01z06c2.tif
Neuron0to2_ h01t03z02c2.tif		Neuron0to2_ h01t01z06c2.tif
	Neuron0to2_3				Neuron0to2_7
Neuron0to2_ h01t01z03c2.tif		Neuron0to2_ h01t01z07c2.tif
Neuron0to2_ h01t02z03c2.tif		Neuron0to2_ h01t01z07c2.tif
Neuron0to2_ h01t03z03c2.tif		Neuron0to2_ h01t01z07c2.tif

Neuron0to2_4
Neuron0to2_ h01t01z04c2.tif
Neuron0to2_ h01t02z04c2.tif
Neuron0to2_ h01t03z04c2.tif

--------------------------------------------------

C. Set-up for loop_fluorescence_extract() :
--------------------------------------------------
Analysis
	Neuron 0
		Mean_Intensity_01.csv
Mean_Intensity_02.csv
Mean_Intensity_03.csv
	Neuron 1
Mean_Intensity_04.csv
Mean_Intensity_05.csv
		Mean_Intensity_06.csv
Mean_Intensity_07.csv
	Neuron 2
Mean_Intensity_04.csv
Mean_Intensity_05.csv
		Mean_Intensity_06.csv
Mean_Intensity_07.csv
	Background_list.csv
--------------------------------------------------

D. After loop_fluorescence_extract() is executed:
--------------------------------------------------
Neurons_to_analyze
	Neuron 0
Neuron 1
Neuron 2
	Results
		Neuron 0.csv
		Neuron 1.csv
		Neuron 2.csv
		Neuron Plots
			Neuron 0.png
			Neuron 1.png
			Neuron 2.png
	Background_list.csv
--------------------------------------------------

E. After merge_data () is executed:
--------------------------------------------------
Neurons_to_analyze
	Neuron 0
Neuron 1
Neuron 2
	Results
		Neuron 0.csv
		Neuron 1.csv
		Neuron 2.csv
		Neuron Plots
		merged_data
			Average_dF_Fo.png
			merged_data.csv
-----------------------------------------------------

Background_list.csv file:

1.	The background averages are entered into an excel file that is saved as a .csv. 
2.	The excel file should have a column for each neuron labeled as Neuron *. Make sure there is no space after the number in the neuron, as the following “Neuron * “ will show an error.
-	Each column must contain the background averages for the stacks being analyzed. 
-	The number of background averages must match the number of Mean_Intensity*.csv files in each neuron folder.
o	For example, in Practice 3 there are 3 neuron folders in Analysis, Neuron 0 with 3 Mean_Intensity*.csv files, Neuron 1 with 4 Mean_Intensity*.csv, and Neuron 2 with 4 Mean_Intensity*.csv files. The ¬¬¬¬¬Background_list.csv would look like the following. Note, since Neuron 1 and Neuron 2 came from the same z-stacks, the background values are the same. 
____________________________
|Neuron 0|  Neuron 1|   Neuron 2|  
|1.978       |  1.084       |  1.084       |
|2.435       |  1.150       |  1.150       |
|2.335       |  0.430       |  0.430       |
|___          |   0.297      |   0.297      |



Code Documentation: 

Sorting Code (gray_sort_tiff_1.0):

gray_sort_tiff(working_dir, num_z_stacks=15,num_t_position=100, channel= 'c2')

1)	Creates a folder for each Z stack (up to 99 Z stacks)
2)	Turns images grayscale.
3)	Saves grayscale images into the correct Z stack folder (up to 999 time points)

Parameters
working_dir: path object or file-like object 
A string path (location) of the folder all the images that will be sorted and turned gray.

When loading the file location into the function make sure that there is no "/" after the folder name or else it will not read the file name properly. For example:
This is wrong: 'C:/Users/nilabuser/Desktop/Practice/'
This is correct: 'C:/Users/nilabuser/Desktop/Practice'

phase: str, default ‘h01’
Set the phase if it exists. You can sort files by the phase name but only one phase at a time. The code must be separately run with each different phase name. Folders created should be edited once finished to incorporate the phase name if these are to be kept separate. If the folder name is not edited, the z stack folders will have all the timepoints for all of the phases in them. 

The default parameter is set to Na. If there is no phase in the name (starting with h), the parameter should be set "channel='Na'" (default). This is used for file names that look like the following:
Practice 3_ t*z*.tif
To include the phase name set the parameter as the following “phase=‘h*’”. For example, if the files are Practice_h01t*z*c*.tif, set the phase parameter as "phase = 'h01'".

position_t: int, default 100
Set the position_t to the number of timepoints in the time-lapse.

A number smaller than the actual number of timepoints can be used to sort a less images. The first image sorted will always be timepoint 1. This method does not allow for using a subset that doesn’t incorporate the first image. 

position_z: int, default 15
Set the position_t to the number of z positions in the stack.

A number smaller than the actual number of z positions can be used to sort a less images. The first image sorted will always be z position 1. This method does not allow for using a subset that doesn’t incorporate the first z position. 

channel: str, default ‘Na’
Set the channel if it exists. You can sort files by the channel name but only one channel at a time. The code must be separately run with each different channel name. Folders created should be edited once finished to incorporate the channel name if these are to be kept separate. If the folder name is not edited, the z stack folders will have all the timepoints for all of the channels in them. 

The default parameter is set to Na. If there is no channel at the end of the name, parameter should be set "channel='Na'" (default). This is used for file names that look like the following:
Practice 3_h*t*z*.tif
To include the channel name set the parameter as the following “channel=‘c*’”. For example, if the files are Practice_h*t*z*c3.tif, set the channel parameter as "channel = 'c3'".

is_gray: str, default ‘No’
Describe whether the exported .tif files are already grayscale “is_gray = ‘Yes’” or whether they are not grayscale “is_gray = ‘No’”.

The default is “is_gray = ‘No’” and this will turn the files grayscale for TrackMate use. 

Fluorescence Extraction Code:

fluorescence_extract(working_dir, results_folder = "results", trial_name = "Neuron_", position_t=100, background_averages=[[1]])

1)	Default: Creates a “results” folder in the same directory as given neuron folder. The results_folder parameter can be changed to create a folder in a different location or with a different name. 
2)	Merges all the Mean_Intensity*.csv files for the given neuron based on the POSITION_T and MEAN_INTENSITY columns. 
3)	Renames the MEAN_INTENSITY columns to the matching Mean_Intensity* to keep track of the stack the values came from. Missing values are replaced with ‘NA’. 
4)	Subtracts the background values based on the background_averages inputed list. The background_averages list must be the same length as number of Mean_Intensity*.csv files. 
5)	Finds the maximum value for each timepoint from the Mean_Intensity columns.
6)	Calculates the ∆F/F0 columns for the given neuron based on the first maximum_value found.
7)	Saves the file in the results folder as the trial_name.csv. The default is set to trial_name = “Neuron” with an output Neuron.csv
8)	Creates a graph of the ∆F/F0 with z stack (POSITION_T) as the x axis and trial_name as the Title and saves as trial_name.png. The default is set to trial_name = “Neuron” with an output Neuron.png

Parameters
working_dir: path object or file-like object 
A string path (location) of the folder neuron folder is. 

When loading the file location into the function make sure that there is no "/" after the folder name or else it will not read the file name properly. For example:
This is wrong: 'C:/Users/nilabuser/Desktop/Example/Neurons_to_analyze/Neuron 0/'
This is correct: 'C:/Users/nilabuser/Desktop/Example/Neurons_to_analyze/Neuron 0’

results_folder: str, default ‘results’
Set the location the output files are saved. The default creates a results folder in the same folder that contains the neuron folder. The location can be set, and if the folder does not exist, it will be created.
trial_name: str, default ‘Neuron_’
Set the name of the output .csv and .png file. This will also be the title of the ∆F/F0 plot. 
position_t:  int, default 100
Set the number of time points (given by the POSITION_T column in the mean intensity file) to be analyzed and merged in each z stack. This can be set to less than the actual number of time points that are in the .csv files. 

Set the actual number time points there are. For example, the number of time points is 100 which has time points 0-99 in the Mean_Intensity*.csv file. Set 100 as the number of frames.
background_averages:  list of int, default [1]
Set the background values for each column. Therefore, the number of background averages given must equal to the number of Mean_Intensity*.csv files in the folder. The background averages must be given in a list (annotated by brackets []). So, if you have 3 columns with the same background average of 2.5, your parameter will look like this:

background_averages = [2.5, 2.5, 2.5]

The default is set to one column (one .csv file) with 1 as the background_average. 

loop_fluorescence_extract(working_dir, background_list, result_folder = "results",  number_of_position_t=100)

1)	Default: Creates a “results” folder in the same directory as neuron folders. The results_folder parameter can be changed to create a folder in a different location or with a different name. 
2)	Merges all the Mean_Intensity*.csv files for each Neuron * folder based on the POSITION_T and MEAN_INTENSITY columns. 
3)	Renames the MEAN_INTENSITY columns to the matching Mean_Intensity* to keep track of the stack the values came from. Missing values are left blank.
4)	Subtracts the background values based on each Background_list.csv column. The Backgroung_list.csv columns must be the same length as number of Mean_Intensity*.csv files for each neuron. The labeling must be in order starting with Neuron 0 and cannot have skipped numbers.
5)	Finds the maximum value for each timepoint from the Mean_Intensity* columns.
6)	Calculates the ∆F/F0 columns for each Neuron * folder based on the first maximum_value found.
7)	Saves the file in the results folder with the following format “Neuron *.csv” 
8)	Creates a graph of the ∆F/F0 with POSITION_T as the x axis and Neuron * as the title. The graph is saved as Neuron *.png
 
Parameters
working_dir: path object or file-like object 
A string path (location) of the folder all the Neuron * folders are. 

When loading the file location into the function make sure that there is no "/" after the folder name or else it will not read the file name properly. For example:
This is wrong: 'C:/Users/nilabuser/Desktop/Example/Neurons_to_analyze/ '
This is correct: 'C:/Users/nilabuser/Desktop/Example/Neurons_to_analyze’

background_list:  path object or file-like object
Set the path to the background values .csv file.

The .csv file should have a column for every neuron in the working_dir. The number of background averages given in each column must equal to the number of Mean_Intensity*.csv files in each neuron folder it pertains to. Each column labeled must be identical to the neuron it pertains to. 
For example, in Practice 3 there are 3 neuron folders in Analysis, Neuron 0 with 3 Mean_Intensity*.csv files, Neuron 1 with 4 Mean_Intensity*.csv, and Neuron 2 with 4 Mean_Intensity*.csv files. The ¬¬¬¬¬Background_list.csv would look like the following. Note, since Neuron 1 and Neuron 2 came from the same z-stacks, the background values are the same. 
_____________________________________________
| Neuron 0    |  Neuron 1    |  Neuron 2    |  
| 1.978       |  1.084       |  1.084       |
| 2.435       |  1.150       |  1.150       |
| 2.335       |  0.430       |  0.430       |
|             |  0.297       |  0.297       |

result_folder:  path object or file-like object, str, default ‘results’
Set the location the output files are saved. The default creates a results folder in the same folder that contains the neuron folder. The location can be set, and if the folder does not exist, it will be created.

number_of_position_t: int, default 100
Set the number of time points (given by the FRAMES and POSITION_T column in the mean intensity file) to be analyzed and merged in each z stack. This can be set to less than the actual number of time points that are in the .csv files. 

Set the actual number time points there are. For example, the number of time points is 100 which has time points 0-99 in the Mean_Intensity*.csv file. Set 100 as the number of frames.
Merging Code:

merge_data(results_folder ,  frames=100, plot_title= ‘Average ∆F/F0’)
1)	Creates a merged_data folder in the results folder.
2)	Reads all the .csv files in the results folder
3)	Merges the ∆F/F0 columns from each Neuron into one file and labels the column with the neuron name (Neuron 0, Neuron 1 etc.)
4)	Calculates the average ∆F/F0 and SEM and saves merged_data.csv file in the merged_data folder
5)	Creates and saves a plot for the average ∆F/F0 in the merged_data folder as .png with the plot_title as the name.

Parameters
results_folder, path object or file-like object 
A string path (location) of the folder all the Neuron*.csv files are. 

When loading the file location into the function make sure that there is no "/" after the folder name or else it will not read the file name properly. For example:
This is wrong: 'C:/Users/nilabuser/Desktop/Example/Neurons_to_analyze/results/'
This is correct: 'C:/Users/nilabuser/Desktop/Example/Neurons_to_analyze/results’
frames:  int, default 100
Set the number of time points (also given by the FRAMES column in the mean intensity file) to be analyzed and merged in each z stack. This can be set to less than the actual number of time points that are in the .csv files. 

Set the actual number time points there are. For example, the number of time points is 100 which has time points 0-99 in the Mean_Intensity*.csv file. Set 100 as the number of frames.
plot_title: str, default ‘Average ∆F/F0’
Set the name of the title the output plot will have. This will also be the name of the .png file when it is saved.

![image](https://user-images.githubusercontent.com/85447873/121700082-8978be80-ca9d-11eb-98ee-c66e3ff3c097.png)
