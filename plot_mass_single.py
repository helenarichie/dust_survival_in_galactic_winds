import sys
sys.path.insert(0, "/ix/eschneider/helena/code/my_scripts/")
from hconfig import *

density_conversion = 5.028e-34/(3.24e-22)**3 # g/cm^3 to M_sun/kpc^3

plt.rcParams.update({'font.family': 'Helvetica'})
fontsize = 25
plt.rcParams.update({'font.size': fontsize})

##################################################################
date = "2024-06-13"
datestr = "0613"
res = "16"
cat = True
pad = 0.1
labelpad = 12
linewidth = 5.5
tickwidth = 1
tmax_0206 = tmax_0204 = 58e3
tmax_0205 = 3e3
tmax_0210 = 3.1e3
tmax_0207 = tmax_0209 = 52.1e3
tmax_frontier0207 = 77.1e3
tmax_0211 = 49e3
tmax_0209 = 44e3
snapshot_times = [[1.5e3, 2.5e3], [20e3, 40e3], [20e3, 40e3], [12e3, 24e3], [0.5e3, 1.5e3]]
snapshot_markers = False
tmax_0613 = 3.2e3
##################################################################

tmax = tmax_0613

##################################################################
basedir = f"/ix/eschneider/helena/data/cloud_wind/{date}/"
pngdir = os.path.join(basedir, "png/")
csvdir = os.path.join(basedir, "csv/")
##################################################################

if snapshot_markers:

    snapshot_times = None
    with open(os.path.join(csvdir, "snapshot_times.csv"), "r") as f:
        for line in f:
            line = line.split(",")
            snapshot_times = np.array(line, dtype=float)

time = []
with open(os.path.join(csvdir, "time.csv")) as f:
    for line in f:
        time.append(float(line))
time = np.array(time)

mass_dust = []
with open(os.path.join(csvdir, "mass_dust.csv")) as f:
    for line in f:
        mass_dust.append(float(line))
mass_dust = np.array(mass_dust)

sputter_hot = []
with open(os.path.join(csvdir, "sputter_hot.csv")) as f:
    for line in f:
        sputter_hot.append(float(line))

sputter = []
with open(os.path.join(csvdir, "sputter.csv")) as f:
    for line in f:
        sputter.append(float(line))

time_output = []
with open(os.path.join(csvdir, "time_output.csv")) as f:
    for line in f:
        time_output.append(float(line))
time_output = np.array(time_output)

rate_dust = []
with open(os.path.join(csvdir, "rate_dust.csv")) as f:
    for line in f:
        line = line.split(",")
        rate_dust.append(np.array(line, dtype=float))

dt_out = time_output[2] - time_output[1]

mass_out = []
mass_cumulative = 0
for i, rate in enumerate(rate_dust):
    rate = np.sum(rate)
    mass_cumulative += rate * dt_out
    mass_out.append(mass_cumulative)
mass_out = np.array(mass_out)

sputter_tot, sputter_tot_hot = [], []
mass_cumulative, mass_cumulative_hot = 0, 0
for i, mass in enumerate(sputter):
    mass_cumulative += mass
    mass_cumulative_hot += sputter_hot[i]
    sputter_tot.append(mass_cumulative)
    sputter_tot_hot.append(mass_cumulative_hot)
sputter_tot = np.array(sputter_tot)
sputter_tot_hot = np.array(sputter_tot_hot)

ymin = np.amin([np.amin(mass_dust), np.amin(mass_out)]) - pad
ymax = np.amax([np.amax(mass_dust), np.amax(mass_out)]) + pad
xmin = np.amin(time[time<=tmax]) - pad
xmax = np.amax(time[time<=tmax]) + pad

if datestr == "0205":
    indices = [np.argmin(time), np.argmin(np.abs(time-snapshot_times[0][0])), np.argmin(np.abs(time-snapshot_times[0][1]))]
if datestr == "0204":
    indices = [np.argmin(time), np.argmin(np.abs(time-snapshot_times[1][0])), np.argmin(np.abs(time-snapshot_times[1][1]))]
if datestr == "0206":
    indices = [np.argmin(time), np.argmin(np.abs(time-snapshot_times[1][0])), np.argmin(np.abs(time-snapshot_times[1][1]))]

if snapshot_markers:
    indices = [np.argmin(time), np.argmin(np.abs(time-snapshot_times[1]*1e-3)), np.argmin(np.abs(time-snapshot_times[2]*1e-3))]

fig = plt.figure(figsize=(9.9, 7.75))

ymin = np.amin(mass_dust) - pad
ymax = np.amax(mass_dust) + pad
xmin = np.amin(time[time<=tmax]) - pad
xmax = np.amax(time[time<=tmax]) + pad
old = "#C53f91"
new = "#d43a4f"
mass_dust_init = mass_dust[0]
plt.plot(time[time<=tmax]/1e3, mass_dust[time<=tmax]/mass_dust_init, label="total", linewidth=linewidth, c=new, zorder=0)
plt.plot(time_output[time_output<=tmax]/1e3, mass_out[time_output<=tmax]/mass_dust_init, linestyle="--", linewidth=linewidth-1, c=new, zorder=0, label="exited box")
plt.plot(time[time<=tmax]/1e3, (sputter_tot[time<=tmax]+sputter_tot_hot[time<=tmax])/mass_dust_init, c="k", label=r"sputtered", linewidth=linewidth, zorder=1)
plt.plot(time[time<=tmax]/1e3, sputter_tot[time<=tmax]/mass_dust_init, c="k", linestyle="--", linewidth=linewidth-2, zorder=1, label=r"$T<10^6~K$")
plt.plot(time[time<=tmax]/1e3, sputter_tot_hot[time<=tmax]/mass_dust_init, c="k", linestyle="-.", linewidth=linewidth-2, zorder=1, label=r"$T\geq10^6~K$")
plt.legend(fontsize=23, loc="center left")
plt.xlim(xmin/1e3, xmax/1e3)
plt.tick_params(axis='both', which='both', direction='in', color='black', top=1, right=1, length=9, width=2, reset=True)
plt.xticks(np.linspace(0, xmax/1e3, 5).round(1))
plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
if snapshot_markers:
    plt.scatter(time[indices]/1e3, mass_dust[indices]/mass_dust_init, marker="o", c=new, zorder=11, s=125, linewidths=3, edgecolors="k")
plt.xlabel("Time [Myr]", fontsize=fontsize+3)
plt.ylabel(r"$m_{dust}/m_{dust,i}$", fontsize=fontsize+5)
plt.tight_layout()
plt.savefig(pngdir + f"dust_mass_{datestr}_{res}.png", dpi=300, bbox_inches="tight")

print("Final total sputtered mass fraction: ", (sputter_tot[time<=tmax][-1]+sputter_tot_hot[time<=tmax][-1])/mass_dust[0])
print("Final hot phase sputtered mass fraction: ", (sputter_tot_hot[time<=tmax][-1])/mass_dust[0])
print("Final cool phase sputtered mass fraction: ", (sputter_tot[time<=tmax][-1])/mass_dust[0])