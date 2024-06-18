import sys
sys.path.insert(0, "../")
from hconfig import *
fontsize = 30
linewidth = 6
pad = 0.01
colors = ["#D1E8F3", "#9ebcda", "#8856a7"]
"""
################################################################
dates = ["2024-02-07", "frontier/2024-02-08", "frontier/2024-02-09"]  # 16, 32, 64
labels = [r"$r_{cl}/16$", r"$r_{cl}/32$", r"$r_{cl}/64$"]
tmax = 52e3
# colors = ["#8856a7", "#9ebcda", "#e0ecf4"]
title = "disrupted"
################################################################
################################################################
dates = ["2024-02-06", "frontier/2024-02-04", "frontier/2024-02-07"]  # 16, 32
labels = [r"$r_{cl}/16$", r"$r_{cl}/32$", r"$r_{cl}/64$"]
tmax = 77e3
title = "survived"
################################################################
"""
################################################################
dates = ["frontier/2024-02-05", "frontier/2024-02-10", "frontier/2024-02-28"]  # 16, 32
labels = [r"$r_{cl}/16$", r"$r_{cl}/32$", r"$r_{cl}/64$"]
tmax = 3.1e3
title = "destroyed"
################################################################

plt.rcParams.update({'font.size': fontsize})

basedirs = []
for date in dates:
    basedirs.append(f"/ix/eschneider/helena/data/cloud_wind/{date}/")

pngdirs, csvdirs = [], []
for basedir in basedirs:
    pngdirs.append(os.path.join(basedir, "png/"))
    csvdirs.append(os.path.join(basedir, "csv/"))

times, masses_dust, sputters_hot, sputters, times_output, rates_dust, dts_output, masses_out = [], [], [], [], [], [], [], []
for n, csvdir in enumerate(csvdirs):
    time = []
    with open(os.path.join(csvdir, "time.csv")) as f:
        for line in f:
            time.append(float(line))
    times.append(np.array(time))

    mass_dust = []
    with open(os.path.join(csvdir, "mass_dust.csv")) as f:
        for line in f:
            mass_dust.append(float(line))
    masses_dust.append(np.array(mass_dust))

    sputter_hot = []
    with open(os.path.join(csvdir, "sputter_hot.csv")) as f:
        for line in f:
            sputter_hot.append(float(line))
    sputters_hot.append(np.array(sputter_hot))

    sputter = []
    with open(os.path.join(csvdir, "sputter.csv")) as f:
        for line in f:
            sputter.append(float(line))
    sputters.append(np.array(sputter))

    time_output = []
    with open(os.path.join(csvdir, "time_output.csv")) as f:
        for line in f:
            time_output.append(float(line))
    times_output.append(np.array(time_output))

    rate_dust = []
    with open(os.path.join(csvdir, "rate_dust.csv")) as f:
        for line in f:
            line = line.split(",")
            rate_dust.append(np.array(line, dtype=float))
    rates_dust.append(rate_dust)

    dt_out = time_output[1] - time_output[0]
    dts_output.append(dt_out)
    dt_special = time_output[-1] - time_output[-2]

    mass_out = []
    mass_cumulative = 0
    for ir, rate in enumerate(rate_dust):
        rate = np.sum(rate)
        if (title == "disrupted") and (n == 0) and (times_output[n][ir] > 40e3):
            print("I'm true!")
            print(times[n][ir])
            mass_cumulative += rate * dt_special
        else:
            mass_cumulative += rate * dt_out
        mass_out.append(mass_cumulative)
    mass_out = np.array(mass_out)
    masses_out.append(mass_out)

times = np.array(times)
times_output = np.array(times_output)
masses_dust = np.array(masses_dust)

sputters_tot, sputters_tot_hot = [], []
for s, sputter in enumerate(sputters):
    sputter_tot, sputter_tot_hot = [], []
    mass_cumulative, mass_cumulative_hot = 0, 0
    for i, mass in enumerate(sputter):
        mass_cumulative += mass
        mass_cumulative_hot += sputters_hot[s][i]
        sputter_tot.append(mass_cumulative)
        sputter_tot_hot.append(mass_cumulative_hot)
    sputters_tot.append(np.array(sputter_tot))
    sputters_tot_hot.append(np.array(sputter_tot_hot))

sputters_tot = np.array(sputters_tot)
sputters_tot_hot = np.array(sputters_tot_hot)
masses_out = np.array(masses_out)

plt.figure(figsize=(9.9, 9))

xmins, xmaxs = [], []
for i, label in enumerate(labels):
    print(label)
    # ymin = np.amin([np.amin(mass_dust), np.amin(mass_out)]) - pad
    # ymax = np.amax([np.amax(mass_dust), np.amax(mass_out)]) + pad
    xmins.append(np.amin(times_output[i][times_output[i]<=tmax]))
    xmaxs.append(np.amax(times_output[i][times_output[i]<=tmax]))

    print(len(times[i]))
    print(len(sputters_tot[i]), len(sputters_tot_hot[i]))

    mass_dust_i = masses_dust[i][0]
    plt.plot(times[i][times[i]<=tmax]/1e3, masses_dust[i][times[i]<=tmax]/mass_dust_i, label=label, linewidth=linewidth, c=colors[i], zorder=0)
    plt.plot(times_output[i][times_output[i]<=tmax]/1e3, masses_out[i][times_output[i]<=tmax]/mass_dust_i, linestyle=":", linewidth=linewidth, c=colors[i], zorder=0)
    plt.plot(times[i][times[i]<=tmax]/1e3, (sputters_tot[i][times[i]<=tmax]+sputters_tot_hot[i][times[i]<=tmax])/mass_dust_i, linestyle="--", linewidth=linewidth, c=colors[i], zorder=0)

plt.tick_params(axis='both', which='both', direction='in', color='black', top=1, right=1, length=11, width=2.5, reset=True)
plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
if title == "destroyed":
    plt.legend(fontsize=fontsize-5, loc="upper right")
plt.xlabel("Time [Myr]")
plt.ylabel(r"$m_{dust}/m_{dust,i}$")
plt.title(title)
# plt.xlim(np.amin(xmins)/1e3 - pad, np.amax(xmaxs)/1e3 + pad)
plt.xlim(0 - pad, tmax/1e3 + pad)
# plt.xticks(np.linspace(0, np.amax(xmaxs)/1e3, 5).round(1))
if title == "destroyed":
    plt.xticks(np.linspace(0, tmax/1e3, 5).round(1))
else:
    plt.xticks(np.linspace(0, tmax/1e3, 5).round(0))
plt.tight_layout()
for pngdir in pngdirs:
    plt.savefig(os.path.join(pngdir, f"{title}_res_comp.png"), bbox_inches="tight")