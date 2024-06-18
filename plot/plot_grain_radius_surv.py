import sys
sys.path.insert(0, "/ix/eschneider/helena/code/my_scripts/")
from hconfig import *
import seaborn as sns

plt.rcParams.update({'font.family': 'Helvetica'})
fontsize = 25
plt.rcParams.update({'font.size': fontsize})
linewidth = 5.5

radii = [0.001, 0.01, 0.1]
dates = ["2024-02-19", "2024-02-08", "2024-02-06"]
colors = sns.color_palette("Paired", 3)
tickwidth = 1

fig = plt.figure(figsize=(9.9,9))

for j, date in enumerate(dates):
    basedir = f"/ix/eschneider/helena/data/cloud_wind/{date}/"
    pngdir = os.path.join(basedir, "png/")
    csvdir = os.path.join(basedir, "csv/")

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
    sputter_hot = np.array(sputter_hot)

    sputter = []
    with open(os.path.join(csvdir, "sputter.csv")) as f:
        for line in f:
            sputter.append(float(line))
    sputter = np.array(sputter)

    sputter_tot, sputter_tot_hot = [], []
    mass_cumulative, mass_cumulative_hot = 0, 0
    for i, mass in enumerate(sputter):
        mass_cumulative += mass
        mass_cumulative_hot += sputter_hot[i]
        sputter_tot.append(mass_cumulative)
        sputter_tot_hot.append(mass_cumulative_hot)
    sputter_tot = np.array(sputter_tot)
    sputter_tot_hot = np.array(sputter_tot_hot)
    xmax = np.amax(time)

    plt.plot(time*1e-3, sputter_tot/mass_dust[0], label=r"{} $\mu m$".format(radii[j]), color=colors[j], linewidth=4)


plt.tick_params(axis='both', which='both', direction='in', color='black', top=1, right=1, length=9, width=2, reset=True)
plt.xticks(np.linspace(0, xmax/1e3, 5).round(1))
plt.yticks(np.linspace(0, 0.5, 6).round(1))
plt.xlim(0, xmax/1e3)
plt.ylim(0-0.01, 0.5+0.01)
plt.xlabel("Time [Myr]", fontsize=fontsize+3)
plt.ylabel(r"$m_{d,sp}/m_{d,i}$", fontsize=fontsize+5)
plt.legend(fontsize=20)

plt.tight_layout()
plt.savefig("radius.png", dpi=300, bbox_inches="tight")