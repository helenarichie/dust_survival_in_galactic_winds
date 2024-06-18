import sys
sys.path.insert(0, "/ix/eschneider/helena/code/my_scripts/")
from hconfig import *

density_conversion = 5.028e-34/(3.24e-22)**3 # g/cm^3 to M_sun/kpc^3

plt.rcParams.update({'font.family': 'Helvetica'})
fontsize = 25
plt.rcParams.update({'font.size': fontsize})

##################################################################
date = "2024-06-13"
cat = True
pad = 0.01
labelpad = 12
linewidth = 5.5
tickwidth = 1
tmax_0206 = tmax_0204 = 58e3
tmax_0205 = 3e3
tmax_0210 = 3.1e3
tmax_0228 = 2.8e3
tmax_0207 = tmax_0209 = 52.1e3
tmax_frontier0207 = 77e3
tmax_0211 = 49e3
tmax_0209 = 44e3
tmax_0318 = 53e3
tmax_0409 = 2.9e3
tmax_0613 = 3.2e3
snapshot_times = [[1.5e3, 2.5e3], [20e3, 40e3], [20e3, 40e3], [12e3, 24e3], [0.5e3, 1.5e3]]
snapshot_markers = False
edges = True
##################################################################

if date == "frontier/2024-03-18":
    tmax = tmax_0318
if date == "2024-02-11":
    tmax = tmax_0211
if date == "frontier/2024-04-09":
    tmax = tmax_0409
if date == "2024-06-13":
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

if date == "frontier/2024-02-07":
    mass_cloud_unsorted = []
    time_cloud_unsorted = []
    with open(os.path.join(csvdir, "full_mass.csv"), "r") as f:
        for line in f:
            line = line.split(",")
            mass_cloud_unsorted.append(float(line[2]))
            time_cloud_unsorted.append(float(line[1]))

    mass_cloud = [x for _, x in sorted(zip(time_cloud_unsorted, mass_cloud_unsorted))]
    time_cloud = sorted(time_cloud_unsorted)
    mass_cloud = np.array(mass_cloud)
    time_cloud = np.array(time_cloud)

else:
    mass_cloud = []
    with open(os.path.join(csvdir, "mass_cloud.csv")) as f:
        for line in f:
            mass_cloud.append(float(line))
    mass_cloud = np.array(mass_cloud)

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
"""
"""
if edges:
    time_output = []
    with open(os.path.join(csvdir, "time_output.csv")) as f:
        for line in f:
            time_output.append(float(line))
    time_output = np.array(time_output)

    rate_dust = []
    with open(os.path.join(csvdir, "rate_dust.csv")) as f:
        for i, line in enumerate(f):
            line = line.split(",")
            rate_dust.append(np.array(line, dtype=float))

    dt_out = time_output[2] - time_output[1]

    rate_cloud = []
    with open(os.path.join(csvdir, "rate_cloud.csv")) as f:
        for line in f:
            line = line.rstrip("\n").split(",")
            rate_cloud.append(np.array(line, dtype=float))

    mass_out_dust = []
    mass_dust_cumulative = 0
    for i, rate in enumerate(rate_dust):
        rate = np.sum(rate)
        mass_dust_cumulative += rate * dt_out
        mass_out_dust.append(mass_dust_cumulative)
    mass_out_dust = np.array(mass_out_dust)

    mass_out_cloud = []
    mass_cloud_cumulative = 0
    for i, rate in enumerate(rate_cloud):
        rate = np.sum(rate)
        mass_cloud_cumulative += rate * dt_out
        mass_out_cloud.append(mass_cloud_cumulative)
    mass_out_cloud = np.array(mass_out_cloud)
"""
"""

sputter_tot, sputter_tot_hot = [], []
mass_cumulative, mass_cumulative_hot = 0, 0
for i, mass in enumerate(sputter):
    mass_cumulative += mass
    mass_cumulative_hot += sputter_hot[i]
    sputter_tot.append(mass_cumulative)
    sputter_tot_hot.append(mass_cumulative_hot)
sputter_tot = np.array(sputter_tot)
sputter_tot_hot = np.array(sputter_tot_hot)

ymin = np.amin([np.amin(mass_dust)]) - pad
ymax = np.amax([np.amax(mass_dust)]) + pad
xmin = np.amin(time[time<=tmax]) - pad
xmax = np.amax(time[time<=tmax]) + pad

if date == "2024-02-05":
    indices = [np.argmin(time), np.argmin(np.abs(time-snapshot_times[0][0])), np.argmin(np.abs(time-snapshot_times[0][1]))]
if date == "2024-02-04":
    indices = [np.argmin(time), np.argmin(np.abs(time-snapshot_times[1][0])), np.argmin(np.abs(time-snapshot_times[1][1]))]
if date == "2024-02-06":
    if snapshot_markers:
        indices = [np.argmin(time), np.argmin(np.abs(time-snapshot_times[1][0])), np.argmin(np.abs(time-snapshot_times[1][1]))]

if snapshot_markers:
    if date == "frontier/2024-02-07":
        indices_cl = [np.argmin(time_cloud), np.argmin(np.abs(time_cloud-snapshot_times[1]*1e-3)), np.argmin(np.abs(time_cloud-snapshot_times[2]*1e-3))]
    else:
        indices_cl = [np.argmin(time), np.argmin(np.abs(time-snapshot_times[1]*1e-3)), np.argmin(np.abs(time-snapshot_times[2]*1e-3))]
    indices_d  = [np.argmin(time), np.argmin(np.abs(time-snapshot_times[1]*1e-3)), np.argmin(np.abs(time-snapshot_times[2]*1e-3))]

fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(9.9, 13.75), gridspec_kw={'wspace':0, 'hspace':0})

old = "#C53f91"
new = "#d43a4f"
mass_dust_init = mass_dust[0]
ax[1].plot(time[time<=tmax]/1e3, mass_dust[time<=tmax]/mass_dust_init, label="total", linewidth=linewidth, c=new, zorder=0)
print("Final total sputtered mass fraction: ", (sputter_tot[time<=tmax][-1]+sputter_tot_hot[time<=tmax][-1])/mass_dust[0])
print("Final hot phase sputtered mass fraction: ", (sputter_tot_hot[time<=tmax][-1])/mass_dust[0])
print("Final cool phase sputtered mass fraction: ", (sputter_tot[time<=tmax][-1])/mass_dust[0])
if edges:
    ax[1].plot(time_output[time_output<=tmax]/1e3, mass_out_dust[time_output<=tmax]/mass_dust_init, linestyle="--", linewidth=linewidth-1, c=new, zorder=0, label="exited box")
ax[1].plot(time[time<=tmax]/1e3, (sputter_tot[time<=tmax]+sputter_tot_hot[time<=tmax])/mass_dust_init, c="k", label=r"sputtered", linewidth=linewidth, zorder=1)
ax[1].plot(time[time<=tmax]/1e3, sputter_tot[time<=tmax]/mass_dust_init, c="k", linestyle="--", linewidth=linewidth-2, zorder=1, label=r"$T<10^6~K$")
ax[1].plot(time[time<=tmax]/1e3, sputter_tot_hot[time<=tmax]/mass_dust_init, c="k", linestyle="-.", linewidth=linewidth-2, zorder=1, label=r"$T\geq10^6~K$")
if date == "frontier/2024-02-07":
    ax[1].legend(fontsize=23, loc="center left")
elif date == "frontier/2024-03-18":
    ax[1].legend(fontsize=23, loc="center left")
elif date == "frontier/2024-04-09":
    ax[1].legend(fontsize=23, loc="center left")
elif date == "2024-02-11":
    ax[1].legend(fontsize=23, loc="center left")
elif date == "2024-06-13":
    ax[1].legend(fontsize=23, loc="center left")
else:
    ax[1].legend(fontsize=23, loc="upper right")
# ax[1].set_xlim(xmin/1e3, xmax/1e3)
ax[1].tick_params(axis='both', which='both', direction='in', color='black', top=1, right=1, length=9, width=2, reset=True)
if date == "frontier/2024-04-09":
    # ax[1].set_xticks(np.linspace(0, xmax/1e3, 5).round(1))
    pass
ax[1].ticklabel_format(axis='y', style='sci', scilimits=(0,0))
if snapshot_markers:
    ax[1].scatter(time[indices_d]/1e3, mass_dust[indices_d]/mass_dust_init, marker="o", c=new, zorder=11, s=125, linewidths=3, edgecolors="k")
ax[1].set_xlabel("Time [Myr]", fontsize=fontsize+3)
ax[1].set_ylabel(r"$m_{dust}/m_{dust,i}$", fontsize=fontsize+5)

ymin = np.amin([np.amin(mass_cloud)]) - pad
ymax = np.amax([np.amax(mass_cloud)]) + pad
xmin = np.amin(time[time<=tmax]) - pad
xmax = np.amax(time[time<=tmax]) + pad

if date == "frontier/2024-02-07":
    ax[0].plot(time_cloud[time_cloud<=tmax]/1e3, mass_cloud[time_cloud<=tmax]/mass_cloud[0], linewidth=linewidth, c="#49b4ab", label="total")
else:
    ax[0].plot(time[time<=tmax]/1e3, mass_cloud[time<=tmax]/mass_cloud[0], linewidth=linewidth, c="#49b4ab", label="total")

if edges:
    ax[0].plot(time_output[time_output<=tmax]/1e3, mass_out_cloud[time_output<=tmax]/mass_cloud[0], linewidth=linewidth-1, linestyle="--", c="#49b4ab", label="exited box")

if snapshot_markers:
    if date == "frontier/2024-02-07":
        ax[0].scatter(time_cloud[indices_cl]/1e3, mass_cloud[indices_cl]/mass_cloud[0], marker="o", c="#49b4ab", zorder=11, s=125, linewidths=3, edgecolors="k")
    else:
        ax[0].scatter(time[indices_cl]/1e3, mass_cloud[indices_cl]/mass_cloud[0], marker="o", c="#49b4ab", zorder=11, s=125, linewidths=3, edgecolors="k")
        print("Snapshot cloud masses: ", mass_cloud[indices_cl]/mass_cloud[0])

ax[0].set_ylabel(r"$m_{cl}/m_{cl,i}$", fontsize=fontsize+5)
ax[0].set_xlim(0, xmax/1e3)
ax[1].set_yticks(np.linspace(0, 1, 6).round(1))
# ax[0].set_yticks(np.linspace(0, np.amax(mass_out_cloud[time_output<=tmax]/mass_cloud[0]), 5).round(2))
ax[0].tick_params(axis='both', which='both', direction='in', color='black', top=1, right=1, length=9, width=2, reset=True, labelbottom=False)
ax[0].ticklabel_format(axis='y', style='sci', scilimits=(0,0))

if date == "frontier/2024-02-07":
    ax[0].legend(fontsize=23, loc="center left")
elif date == "frontier/2024-03-18":
    ax[0].legend(fontsize=23, loc="upper left")
elif date == "2024-02-11":
    ax[0].legend(fontsize=23, loc="center left")
elif date == "2024-06-13":
    ax[0].legend(fontsize=23, loc="upper right")
else:
    ax[0].legend(fontsize=23, loc="upper right")

plt.tight_layout()
date = date.lstrip("frontier/")
plt.savefig(pngdir + f"dust_cloud_mass_{date}.png", dpi=300, bbox_inches="tight")