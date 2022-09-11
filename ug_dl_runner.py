import subprocess
import time

#Need to run up until about 2 000 000
process_num = 0
for i in range(0, 2000000, 200000):
    #print("python3", "ug_downloader.py", "--start", str(i+1), "--end", str(i+200000), "--process_num", str(process_num))
    subprocess.Popen(["python3", "ug_downloader.py", "--start", str(i+1), "--end", str(i+200000), "--process_num", str(process_num)])
    process_num += 1
    time.sleep(10)
    