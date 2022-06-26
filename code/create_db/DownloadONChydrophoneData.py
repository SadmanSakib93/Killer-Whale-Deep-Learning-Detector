import os
from onc.onc import ONC
import pandas as pd

# Changing the CWD
os.chdir('/data/audio/ONC/BarkleyCanyon_Jasper_Kanes_New_Download/')

onc = ONC('6c154298-42fd-4fbe-80c5-26e2d274b577')

# This path is according to the ORCA-VM, Needs update if want to run in cedar
data_df=pd.read_csv("/home/sadmans/KW_detector_multiclass/annotations/original/ONC_BarkleyCanyon.csv")

unique_filenames=data_df['filename'].unique()
print("unique_filenames:", len(unique_filenames))

existing_filelists=[name for path, subdirs, files in os.walk("/data/audio/ONC/BarkleyCanyon") for name in files]
print("existing_filelists:", len(existing_filelists))

total_downloaded=0
downloaded_files=[]
for each_file in unique_filenames:
    filename=os.path.basename(each_file)
    if(filename not in existing_filelists):
        print(filename, "Downloading . . .")
        result = onc.getFile(filename)
        downloaded_files.append(filename)
        total_downloaded+=1
        print("Done!")
    else:
        print(filename, "Already exists!")
         
print("total_downloaded:", total_downloaded)
df = pd.DataFrame(data={"downloaded_filename": downloaded_files})
df.to_csv("/home/sadmans/output/ONC_downloaded_files.csv", sep=',', index=False)