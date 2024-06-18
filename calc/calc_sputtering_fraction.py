import sys
sys.path.insert(0, "/ix/eschneider/helena/code/my_scripts")
from hconfig import *
from csv import writer

##################################################################
date = "frontier/2024-02-28"
##################################################################

##################################################################
basedir = f"/ix/eschneider/helena/data/cloud_wind/{date}/"
csvdir = os.path.join(basedir, "csv/")
tmax = None
##################################################################

sputter_hot = []
count = 0
with open(os.path.join(csvdir, "sputter_hot.csv")) as f:
    for line in f:
        line = line.split(",")
        count += float(line[0])
        sputter_hot.append(count)
sputter_hot = np.array(sputter_hot)

sputter = []
count = 0
with open(os.path.join(csvdir, "sputter.csv")) as f:
    for line in f:
        line = line.split(",")
        count += float(line[0])
        sputter.append(count)
sputter = np.array(sputter)

mass_dust = []
with open(os.path.join(csvdir, "mass_dust.csv")) as f:
    for line in f:
        line = line.split(",")
        mass_dust.append(float(line[0]))
mass_dust = np.array(mass_dust)

time = []
with open(os.path.join(csvdir, "time.csv")) as f:
    for line in f:
        time.append(float(line))
time = np.array(time)

f = open(os.path.join(csvdir, "results.csv"), "w")

with open(os.path.join(csvdir, "results.csv"), "a") as f:
    writer_obj = writer(f)
    writer_obj.writerow([f"Inital mass: {mass_dust[0]} M_sun"])
    writer_obj.writerow([f"Hot fraction sputtered: {sputter_hot[-1]/mass_dust[0]}"])
    writer_obj.writerow([f"Cool fraction sputtered: {sputter[-1]/mass_dust[0]}"])
    writer_obj.writerow([f"Total fraction sputtered: {(sputter[-1]+sputter_hot[-1])/mass_dust[0]}"])
    f.close()

if tmax == None:
    print(f"Inital mass: {mass_dust[0]} M_sun")
    print(f"Hot fraction sputtered: {sputter_hot[-1]/mass_dust[0]}")
    print(f"Cool fraction sputtered: {sputter[-1]/mass_dust[0]}")
    print(f"Total fraction sputtered: {(sputter[-1]+sputter_hot[-1])/mass_dust[0]}")
else:
    print(f"Inital mass: {mass_dust[0]} M_sun")
    print(f"Hot fraction sputtered: {sputter_hot[time<=tmax][-1]/mass_dust[0]}")
    print(f"Cool fraction sputtered: {sputter[time<=tmax][-1]/mass_dust[0]}")
    print(f"Total fraction sputtered: {(sputter[time<=tmax][-1]+sputter_hot[-1])/mass_dust[0]}")