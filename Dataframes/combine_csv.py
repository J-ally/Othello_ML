import os
import glob
import pandas as pd
import time

os.chdir("C:/Users/joseph/Dropbox/Joseph/AgroParisTech/IODAAAAA/Othello_ML/Dataframes")

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
#export to csv

now = int( time.time() )
combined_csv.to_csv( f"{now}_final_df.csv", index=False, encoding='utf-8-sig')