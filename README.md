This repo contains programs and scripts for the multiclass (three or four classes) classification of Killer Whale-KW, Humpback-HB, Dolphin-D (included only in four classes), and background/other.

# Instructions to run scripts on cedar:
The instructions to run python scripts via Jupiter notebooks can be found on the Compute Canada documentation web page (https://docs.computecanada.ca/wiki/JupyterNotebook)
- Log in to cedar: ssh username@cedar.computecanada.ca
- [Installing Jupyter Notebook](https://docs.computecanada.ca/wiki/JupyterNotebook#Installing_Jupyter_Notebook): This is a one-time task, so after installing once, no need to do this step later again.
- [Activating the environment](https://docs.computecanada.ca/wiki/JupyterNotebook#Activating_the_environment): After installation, every time need to activate the environment, similar to a typical Python virtual environment as well.
- **Create a script to launch Jupyter Lab**
 Use nano (text editor in Linux) to create a bash script that we'll call upon to open up a Jupyter Lab session.

   * Create a script in your virtual environment (make sure `jupyter1` is active), in the bin folder: `nano $VIRTUAL_ENV/bin/notebook.sh`

   * This opens up the nano text editor so that we can create the bash script (see the [Youtube video](https://youtu.be/5yCUDqAbBUk?t=969) for more details):

       ```bash
       #!/bin/bash
       unset XDG_RUNTIME_DIR
       jupyter-lab --ip $(hostname -f) --no-browser
       ```

       Press ctrl-O to save, ctrl-X to exit. 

   * Back in your home directory, change the user privileges of the `notebook.sh` that you just created (we'll allow the user, *u*, to execute, *x*, the file). This is needed so that we can run the script in the bin folder: `chmod u+x $VIRTUAL_ENV/bin/notebook.sh `
   
- [Starting Jupyter Notebook](https://docs.computecanada.ca/wiki/JupyterNotebook#Starting_Jupyter_Notebook): 
Need to use the salloc command with appropriate arguments in order to put a resource allocation request in the queue. 
   While in your virtual environment, run a similar command to the following:

   * ```
     salloc --time=1:0:0 --ntasks=1 --cpus-per-task=4 --mem-per-cpu=2048M --account=def-stanmat-ab srun $VIRTUAL_ENV/bin/notebook.sh
     ```
     
     * Allocate 1 hour for 1 task, using 4 CPUs and 2048 MB of RAM/CPU.
     * For requesting GPUs: [Check this documentation of GPU](https://docs.computecanada.ca/wiki/Using_GPUs_with_Slurm/en)
     * An example to request for GPU for 12 hours is as follows:

    ```
     salloc --time=12:00:0 --ntasks=1 --cpus-per-task=4 --gres=gpu:4 --mem=16G --account=def-stanmat-ab srun $VIRTUAL_ENV/bin/notebook.sh
    ```


- [Connecting to Jupyter Notebook](https://docs.computecanada.ca/wiki/JupyterNotebook#Connecting_to_Jupyter_Notebook): SSH tunnel from your local computer into the Jupyter Notebook

 The Jupyter Notebook is now running on the Compute Canada HPC. We need to "tunnel" into the HPC system and show the notebook on our local computer.
   * Open a new terminal window.
   * In the new terminal, ssh into the graham server. Type something like this, based on what is shown on the other terminal you have open showing the notebook access token:

     ``` 
     ssh -L 8888:cdr767.int.cedar.computecanada.ca:8888 username@cedar.computecanada.ca
     ```
   * It will ask you for your login credentials. Fill that in.
   * Then on the local browser, copy the link to Jupyter lab with the access token, like: `http://localhost:8888/?token=<token>`. Or, you can copy the link from your terminal (or click it if your terminal client allows you to).

# Repository structure:
## annotations:
- original: contains the original annotations given by the annotator
- train/test: train and test folder contains the split version of the train and test annotation. The multi-class annotations files are created by running the code/create_db/split_train_test_annot.ipynb notebook. These two folders also contain the older annotations which we used for binary detector development.

## code:
The python scripts/notebooks are organized as follows in the "**code**" directory:
- preprocessing:
    - dfo_annot_format.ipynb: this notebook loads original DFO annotation which contains overlapping annotations and merges them to get non-overlapping annotations
    - hdf5_analysis.ipynb: this notebook is used to plot spectrograms from dataset groups at random!
- create_db:
    - DownloadONChydrophoneData.py: this script is used to download ONC hydrophone data of Barkley Canyon Jasper Kanes
    - JASCO_Malahat_VFPA_missing_file.ipynb: this script is used to find the missing audio files in the JASCO Malahat VFPA annotations
    - prepare_db.ipynb: this notebook is used to create the training dataset using all data except the DFO dataset
    - prepare_dfo_db.ipynb: this notebook reads the dfo dataset from .tar and appends it to the previously created (using prepare_db.ipynb script) hdf5 dataset
    - split_train_test_annot.ipynb: loads the new annotations from original annotations folders (multi-class annots only) and stores separate annotations in train and test annotations folder.
- training:
    - densenet_recipe_1.json: recipe for the utilized dense net architecture
    - train_nn.ipynb: contains code for training the multi-class detector
- testing:
    - get_model_detections.ipynb: reads all test file list and save trained models detections to "model_detections" folder
    - calculate_multi_class_performance.ipynb.ipynb: compares model detection scores with ground truth annotations and calculates the performance metrices

## model_detections:
- This directory contains the saved detection scores given by the trained model

## trained_models:
- Contains the trained model file (.kt)

## file_lists/test:
- Contains the list of files used from each test data source.

# Dataset:
## Training
There are three main datasets for the training set:
- JASCO Boundary Pass and JASCO Robert's Bank (annotations/train/JASCO_fp_train.csv and annotations/train/JASCO_tp_train.csv)
- DFO (annotations/train/dfo_no_overlap_train_multiclass.csv)
- ONC Barkley Canyon (annotations/train/onc_barkley_canyon_train_multiclass.csv)

The main source of data for the HALLO project is a series of recordings provided by JASCO. These recordings were made in two nearby locations in British Columbia: Robert's Bank and Boundary pass.
All of the recordings have passed through JASCO's detector and have been validated as **true positive** (i.e., a killer whale was present at that moment) or **false positive** (i.e., a false alarm, no killer whales present at that moment).

The data validation process identified true positives (meaning KW found) and false positives (no KW found).
- FileName: the name of the .wav file
- CallLength: the estimated length of the call in ms
- ActualTime: the timestamp of the call (DetectionTime) converted to seconds elapsed from the beginning of the .wav file.

## Testing
The level of annotation for the Robert's Bank and Boundary pass recordings is too coarse to provide good test cases. Since only the outputs of the JASCO detector were validated, anything missed by it has not been inspected by a bio-acoustician and therefore **cannot be considered a true negative**.

To that end, selected files from the Robert's Bank and Boundary pass hydrophones have been fully inspected by bio-acousticians to be included as test sets.
These annotations are present in the *tests/annotations* directories in this repository. These have all the sounds identified by the bio-acoustician (not only the killer whales).

These .csv annotations have the following fields (some annotation files might have a few more columns, but all have at least should have the following):
- filename: the name of the .wav file, including the path in the cedar
- start: the start of the call in seconds from the beginning of the file
- end: the end of the call in seconds from the beginning of the file
- freq_min: the lower frequency limit of annotation box (missing in Orcasound test data)
- freq_max: the upper-frequency limit of annotation box (missing in Orcasound test data)
- label: the label identifying the annotation (all labels are "KW" for Killer Whale)

A few more columns available in some of the test annotations are:
- offset: the start of the call in seconds from the beginning of the first file in a series of files (this is only relevant for bio-acousticians, who are using Raven for annotations)
- kw_ecotype: a label identifying the ecotype for killer whale sound
- pod: a label identifying the pod for killer whale sounds
- call_type: a label identifying the call type for killer whale sounds
- comments: any comments added by the bio-acoustician
- annotator: a field identifying the annotator
- path: the path to the .wav file in the orca-VM filesystem.
- Confidence: annotator's confidence in the annotation.

#### List of test sets:

- JASCO Robert's Bank
- JASCO Boundary Pass 
- ONC Barkley Canyon: Data from the Barkley Canyon node containing mostly Southern Residents and Transient killer whale calls
- Orcasound:  Primary focus on Southern Resident Killer Whales. This consists of recordings from the [OrcasoundLab] (https://www.orcasound.net/portfolio/orcasound-lab-hydrophone) hydrophone node on September 27th, 2017.
- Lime Kiln Superpod Event: These are all annotations from the Lime Kiln Stat Park hydrophone.

#### Test sets details:

|         Data source         | Total number of annotations | Number of Files | Total duration |
|:---------------------------:|:---------------------------:|:---------------:|:---------------:|
|     Jasco Robert's Bank     |             2138            |        207      |2h:30m| 
|     Jasco Boundary Pass     |             1100            |        5        |3h:30m|
|   ONC Barkley Canyon        |             1357            |        73       |2h:13m|
|          Orcasound          |             520             |        22       |0h:51m|
| Lime Kiln superpod events   |             1513            |        133      |6h:05m|

# Results:
The following graph shows the performance matrices on the test annotations for the three-class model (KW, HB, Other). The ONC Barkley Canyon result is the mean result of the test/onc_barkley_canyon_annot.csv and test/onc_barkley_canyon_test_multiclass_annot.csv annotation files.
## False positive rate:
![Alt text](images/performance_measures_FPR.png?raw=true)
## Precision:
![Alt text](images/performance_measures_precision.png?raw=true)
## Recall:
![Alt text](images/performance_measures_recall.png?raw=true)
## Specificity or True negative rate:
![Alt text](images/performance_measures_specificity.png?raw=true)
