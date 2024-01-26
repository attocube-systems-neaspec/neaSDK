"""
Records streamed data (tip position, channel data) and writes them to a *.txt on desktop.

"""
from pathlib import Path
from os import path
from time import sleep, time
from datetime import datetime
from nea_tools.microscope import stream

title = "recorded_data" # title of savefile
t_record = 60 # total recording time, in sec
dt = 0.2 # time between two data points, in sec
channels_to_record = ['time','AveragedX','AveragedY','AveragedZ','M0A','M1A']


date = datetime.now().strftime("%Y-%m-%d_%H-%M")
fname    = f"{date}_{title}.txt"
fullpath = path.join(Path().home(),'Desktop',fname)
print(f"Saving data to {fullpath}")
start = time()
stopwatch = time()

with open(fullpath,'w',encoding="utf-8") as file:
    file.write("# "+"\t".join(channels_to_record)+"\n")
    def write_data_to_file(data):
        line_data = []
        for channel in channels_to_record:
            if channel == 'time':
                data_point = data[channel][-1]-start
            else:
                data_point = data[channel][-1]
            line_data.append(str(data_point))
        line = "\t".join(line_data)+"\n"
        global stopwatch
        if time() - stopwatch >= dt:
            file.write(line)
            stopwatch = time()
            
    try:
        with stream.Stream(callback=write_data_to_file) as recorder:
            sleep(t_record)
    except Exception as e:
        file.write(e)