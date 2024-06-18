import sys
sys.path.insert(0, "/ix/eschneider/helena/code/my_scripts")
from hconfig import *
from csv import writer

density_conversion = 5.028e-34/(3.24e-22)**3 # g/cm^3 to M_sun/kpc^3

##################################################################
date_0209 = "frontier/2024-02-09"
date_0207 = "frontier/2024-02-07"
datestr = "0207"
cat = True
fontsize = 25
labelpad = 12
tickwidth = 1
plt.rcParams.update({'font.family': 'Helvetica'})
plt.rcParams.update({'font.size': fontsize})
plt.style.use('dark_background')
fnum_0207 = 400
fnum_0209 = 405
rho_cl_init = 10*0.6*MP * density_conversion
xmin = 0
pad = 0.0005
##################################################################

fnum = fnum_0207
fnum = fnum_0209

fnums = [fnum_0207, fnum_0209]

##################################################################
basedir_0207 = f"/ix/eschneider/helena/data/cloud_wind/{date_0207}/"
basedir_0209 = f"/ix/eschneider/helena/data/cloud_wind/{date_0209}/"
pngdir = os.path.join(basedir_0209, "png/")
##################################################################

fulldirs = [os.path.join(basedir_0207, "hdf5/full/"), os.path.join(basedir_0209, "hdf5/full/")]
csvdirs = [os.path.join(basedir_0207, "csv/"), os.path.join(basedir_0209, "csv/")]
labels = ["survived", "disrupted"]
colors = ["plum", "steelblue"]

xmins = []
xmaxs = []
ymins = []
ymaxs = []

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(9.9, 9))

for i, fnum in enumerate(fnums):
    print(i)
    """
    # data = ReadHDF5(fulldirs[i], cat=cat, fnum=fnum, dust=True)
    f = h5py.File(os.path.join(fulldirs[i], str(fnum)+".h5"), "r")
    head = f.attrs
    dx = head["dx"][0]
    t = head["t"][0]
    gamma = head["gamma"][0]
    mu = 0.6
    nx = head["dims"][0]

    d_gas = np.array(f["density"])
    d_dust = np.array(f["dust_density"])

    gas_sum = []
    dust_sum = []

    for k, d in enumerate(d_gas):
        # only get values for gas and dust that are in the cloud
        gas_sum.append(np.sum(d_gas[k,:,:][d_gas[k,:,:]>=rho_cl_init/30]))
        dust_sum.append(np.sum(d_dust[k,:,:][d_gas[k,:,:]>=rho_cl_init/30]))

    gas_sum = np.array(gas_sum)
    dust_sum = np.array(dust_sum)

    dust_to_gas = dust_sum/gas_sum

    x_arr = np.zeros(nx)
    for j, x in enumerate(x_arr):
        if j > 0:
            x_arr[j] = x_arr[j-1] + dx

    """
    x_arr, dust_to_gas = [], []
    with open(os.path.join(csvdirs[i], "dtg.csv")) as f:
        for line in f:
            line = line.split(",")
            x_arr.append(float(line[0]))
            if np.isnan(float(line[1])):
                dust_to_gas.append(0)
            else:
                dust_to_gas.append(float(line[1]))
    x_arr = np.array(x_arr)
    dust_to_gas = np.array(dust_to_gas)

    wh_real = np.isnan(dust_to_gas, where=False)
    print(x_arr[wh_real])
    print(dust_to_gas[wh_real])

    xmins.append(np.amin(x_arr[wh_real]))
    xmaxs.append(np.amax(x_arr[wh_real]))
    ymaxs.append(np.amax(dust_to_gas[wh_real]))
    ymins.append(np.amin(dust_to_gas[wh_real]))



    # , c="#f16948"
    if i == 1:
        ax.plot(x_arr[x_arr>=1.3], dust_to_gas[x_arr>=1.3], linewidth=4, label=labels[i], color=colors[i])
    if i == 0:
        ax.plot(x_arr, dust_to_gas, linewidth=4, label=labels[i], color=colors[i])
    ax.set_xlabel(r"r$~[kpc]$", fontsize=fontsize+3)
    ax.set_ylabel(r"dust-to-gas ratio", fontsize=fontsize+3, labelpad=5)
    #ax.tick_params(axis='both', which='both', direction='in', color='black', top=1, right=1, length=9, width=2, reset=True)
    ax.set_xticks(np.linspace(xmin, np.amax(x_arr[wh_real]), 5).round(1))
    #ax.set_yticks(np.linspace(0, np.amax(mass_dust_tot[t_arr<=tmax]), 5).round(2))
    #ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax.legend(loc="upper right", fontsize=fontsize-2)

    """

    with open(os.path.join(csvdirs[i], "dtg.csv"), "a") as ofile:
        writer_obj = writer(ofile)
        for k, xi in enumerate(x_arr):
            writer_obj.writerow([x_arr[k], dust_to_gas[k]])
        ofile.close()

    f.close()
    """

# plt.xlim(np.amin(xmins), np.amax(xmaxs))
xmin, xmax = 0.7, 6.4
ymin, ymax = 0, 0.01

plt.xlim(xmin, xmax)
plt.ylim(ymin-pad, ymax+pad)
plt.xticks(np.linspace(xmin, xmax, 6).round(0))
#plt.yticks(np.linspace(ymin, ymax, 5).round(3))
plt.tick_params(axis='both', which='both', direction='in', color='black', top=1, right=1, length=9, width=2, reset=True)
# plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
plt.savefig(pngdir + f"{fnum}_dust_to_gas_{datestr}_dark.png", dpi=300, bbox_inches="tight")