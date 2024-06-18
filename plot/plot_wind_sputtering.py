import os
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, "/Users/helenarichie/GitHub/my_scripts/")
from hconfig import *

plt.rcParams.update({'font.family': 'Helvetica'})
plt.rcParams.update({'font.size': 25})

csvdir = "/Users/helenarichie/Desktop/"
fontsize = 25
shielded_init = 0.76

# get times of snapshots
t_unshielded, r_unshielded, rho_d_unshielded = [], [], []
with open(os.path.join(csvdir, "single_cell_wind_unshielded.csv")) as f:
    for line in f:
        line = line.split(",")
        t_unshielded.append(float(line[0]))
        r_unshielded.append(float(line[1]))
        rho_d_unshielded.append(float(line[2]))

# get times of snapshots
t_shielded, r_shielded, rho_d_shielded = [], [], []
with open(os.path.join(csvdir, "single_cell_wind_shielded.csv")) as f:
    for line in f:
        line = line.split(",")
        t_shielded.append(float(line[0]))
        r_shielded.append(float(line[1]))
        rho_d_shielded.append(float(line[2]))

rho_d_unshielded = np.array(rho_d_unshielded)
rho_d_shielded = np.array(rho_d_shielded)

print(rho_d_shielded[0])

print(f"Unshielded dust survival: {round(np.amin(rho_d_unshielded)/rho_d_unshielded[0], 4)}")
print(f"Shielded dust survival: {round(np.amin(rho_d_shielded/rho_d_shielded[0])*shielded_init, 4)}")
r_shielded = np.array(r_shielded)

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(9.9, 9))
#ax.plot(np.log10(r_unshielded), rho_d_unshielded/rho_d_unshielded[0], linewidth=4, c="k")
#ax.plot(np.log10(r_shielded), rho_d_shielded/rho_d_shielded[0], linewidth=4, c="r")
ax.plot(r_shielded, (rho_d_shielded/rho_d_shielded[0])*shielded_init, linewidth=4, c="black", label="partially shielded")
ax.plot(r_unshielded, rho_d_unshielded/rho_d_unshielded[0], linewidth=4, c="black", label="unshielded", linestyle="--")
# ax.plot(r_shielded, rho_d_shielded/rho_d_shielded[0], linewidth=4, c="teal", label="partially shielded")
# ax.plot(r_unshielded, rho_d_unshielded/rho_d_unshielded[0], linewidth=4, c="teal", linestyle="--", label="unshielded")#1e81b0
#ax.set_xlim(np.amin(np.log10(r_unshielded)), np.amax(np.log10(r_unshielded)))
ax.set_xlim(0, 10)
#ax.set_xticks(np.linspace(np.amin(np.log10(r_unshielded)), np.amax(np.log10(r_unshielded)), 5).round(1))
#ax.set_xticks(np.linspace(np.amin(r_unshielded), np.amax(r_unshielded), 5).round(1))
ax.set_xlabel("r [kpc]", fontsize=fontsize+3)
ax.set_ylabel(r"$m_{dust}/m_{dust,i}$", fontsize=fontsize+5)
ax.tick_params(axis='both', which='both', direction='in', color='black', top=1, right=1, length=9, width=2, reset=True)
plt.legend(fontsize=fontsize-3)
plt.tight_layout()
plt.savefig("/Users/helenarichie/Desktop/single_cell_wind.png", bbox_inches="tight")
