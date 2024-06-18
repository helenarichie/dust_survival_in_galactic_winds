import sys
sys.path.insert(0, "/ix/eschneider/helena/code/my_scripts/")
from hconfig import *
import seaborn as sns
from csv import writer

density_conversion = 5.028e-34/(3.24e-22)**3 # g/cm^3 to M_sun/kpc^3
plt.rcParams.update({'font.family': 'Helvetica'})

##############################################
date = "frontier/2024-04-09"
datestr = "0409"
vlims_gas = (18.2, 20.6)    # destroyed
vlims_dust = (-10, -5.2)   # destroyed
fnums = [0, 200, 400]     # disrupted
spacing, unit = 15, "pc" # pc, spacing of tick marks
##############################################

##############################################
cat = True
pad = 0.1
fontsize = 30
labelpad = 12
tickwidth = 2.25
ticklength = 14
##############################################

##############################################
basedir = f"/ix/eschneider/helena/data/cloud_wind/{date}/"
projdir = os.path.join(basedir, "hdf5/proj/")
pngdir = os.path.join(basedir, "png/")
csvdir = os.path.join(basedir, "csv/")
##############################################

f = open(os.path.join(csvdir, "results.csv"), "w")

cmap_gas = sns.color_palette("mako", as_cmap=True)
cmap_dust = sns.color_palette("rocket", as_cmap=True)
plt.rcParams.update({'font.size': fontsize})

fig, ax = plt.subplots(nrows=2, ncols=3, gridspec_kw={"width_ratios":[0.75, 2.125, 2.125], 'wspace':0, 'hspace':0}, figsize=(24,9.4))

snapshot_times = []
im_g = None
im_d = None
height = None
for i, row in enumerate(ax):
    for j, col in enumerate(row):
        data = ReadHDF5(projdir, proj="xy", cat=cat, dust=True, fnum=fnums[j])
        head = data.head
        conserved = data.conserved
        dx = head["dx"][0]
        nx, ny, nz = head["dims"]

        ylen = int(0.875*ny)
        #ylen = ny
        xlen = [int(0.75*ylen), int(2.125*ylen), int(2.125*ylen)]
        xs = [0, 325, 1700]
        #ys = [0, 0, 0]
        ys = [80, 80, 80]

        height = ylen

        if unit == "pc":
            dx *= 1e3  # pc
        d_gas = conserved["density"]
        d_gas *= head["mass_unit"] / (head["length_unit"] ** 2)
        n_gas = d_gas[0]/(0.6*MP) # column density
        d_dust = conserved["dust_density"][0]
        d_dust[d_dust==0] = 1e-40
        d_dust *= head["mass_unit"] / (head["length_unit"] ** 2)
        t = data.t_cgs() / yr_in_s  # yr
        if (i == 0):
            snapshot_times.append(t[0])

        if (i == 0):
            im_g = ax[i][j].imshow(np.log10(n_gas[xs[j]:(xs[j]+xlen[j]+1),ys[j]:(ys[j]+ylen+1)].T), origin="lower", vmin=vlims_gas[0], vmax=vlims_gas[1], extent=[0, xlen[j]*dx, 0, ylen*dx], cmap=cmap_gas, aspect='auto')
        if (i == 1):
            im_d = ax[i][j].imshow(np.log10(d_dust[xs[j]:(xs[j]+xlen[j]+1),ys[j]:(ys[j]+ylen+1)].T), origin="lower", vmin=vlims_dust[0], vmax=vlims_dust[1], extent=[0, xlen[j]*dx, 0, ylen*dx], cmap=cmap_dust, aspect='auto')

        if j == 0:
            if i == 1:
                ax[i][j].hlines(0.86*ylen*dx, 0.5*spacing, 1.5*spacing, color='white')
                ax[i][j].text(1.5*spacing+2, 0.83*dx*ylen, f'{spacing} {unit}', color='white', fontsize=fontsize)
                ax[i][j].text(0.65*spacing, 0.125*dx*ylen, 'dust', color='white', fontsize=fontsize)
        if i == 0:
            ax[i][j].text(0.5*spacing, 0.83*dx*ylen, f'{round(t[0]/1e6, 1)} Myr', color='white', fontsize=fontsize)
            if j == 0:
                ax[i][j].text(0.6*spacing, 0.125*dx*ylen, 'gas', color='white', fontsize=fontsize)

        yticks = [ylen*dx/2-spacing/2-spacing-spacing, ylen*dx/2-spacing/2-spacing, ylen*dx/2-spacing/2, ylen*dx/2+spacing/2, ylen*dx/2+spacing/2+spacing, ylen*dx/2+spacing/2+spacing+spacing]
        ax[i][j].set_xticks(np.arange(0, xlen[j]*dx, spacing))
        ax[i][j].set_yticks(yticks)
        ax[i][j].tick_params(axis='both', which='both', direction='in', color='white', labelleft=0, labelbottom=0, top=1, right=1, length=ticklength, width=tickwidth)
        [x.set_linewidth(4) for x in ax[i][j].spines.values()]
        [x.set_color('white') for x in ax[i][j].spines.values()]

        if (i == 0) and (j == 2):
            continue
            # cbar = fig.colorbar(im, ax=ax[i][j], location='right', pad=0.02, aspect=17)
            # cbar = fig.colorbar(im, ax=ax[i][j], pad=0.02, aspect=17)
            # cbar.set_label(r'$\mathrm{log}_{10}(N_{H, gas})$ [$\mathrm{cm}^{-2}$]', rotation=270, labelpad=40, fontsize=fontsize)
            # cbar.ax.tick_params(length=ticklength, width=tickwidth, color="white", labelsize=fontsize-5)
            # cbar.set_ticks(np.linspace(vlims_gas[0], vlims_gas[1], 4).round(1))
        if (i == 1) and (j == 2):
            continue
            # cbar = fig.colorbar(im, ax=ax[i][j], location='right', pad=0.02, aspect=17)
            # cbar = fig.colorbar(im, ax=ax[i][j], pad=0.02, aspect=17)
            # cbar.set_label(r'$\mathrm{log}_{10}(\Sigma_{dust})$ [$\mathrm{g}\,\mathrm{cm}^{-2}$]', rotation=270, labelpad=30, fontsize=fontsize)
            # cbar.ax.tick_params(length=ticklength, width=tickwidth, color="white", labelsize=fontsize-5)
            # cbar.set_ticks(np.linspace(vlims_dust[0], vlims_dust[1], 4).round(1))
        

cbar_height = 0.3765
cbar_ax = fig.add_axes([0.903, 0.499, 0.03, cbar_height])
cbar = fig.colorbar(im_g, cax=cbar_ax, pad=0.1)
cbar.set_label(r'$\mathrm{log}_{10}(N_{H, gas})$ [$\mathrm{cm}^{-2}$]', rotation=270, labelpad=50, fontsize=fontsize-2)
cbar.ax.tick_params(length=ticklength, width=tickwidth, color="white", labelsize=fontsize-7)
cbar_spacing = (vlims_gas[1] - vlims_gas[0])/8
cbar.set_ticks(np.linspace(vlims_gas[0]+cbar_spacing, vlims_gas[1]-cbar_spacing, 4).round(1))
cbar.outline.set_edgecolor('black')
cbar.outline.set_linewidth(1.5)

cbar_ax = fig.add_axes([0.903, 0.1137, 0.03, cbar_height])
cbar = fig.colorbar(im_d, cax=cbar_ax)
cbar.set_label(r'$\mathrm{log}_{10}(\Sigma_{dust})$ [$\mathrm{g}\,\mathrm{cm}^{-2}$]', rotation=270, labelpad=50, fontsize=fontsize-2)
cbar.ax.tick_params(length=ticklength, width=tickwidth, color="white", labelsize=fontsize-7)
cbar_spacing = (vlims_dust[1] - vlims_dust[0])/8
cbar.set_ticks(np.linspace(vlims_dust[0]+cbar_spacing, vlims_dust[1]-cbar_spacing, 4).round(1))
cbar.outline.set_edgecolor('black')
cbar.outline.set_linewidth(1.5)

plt.savefig(pngdir + f"snapshots_dest.png", dpi=300, bbox_inches="tight")
plt.close()

with open(os.path.join(csvdir, "snapshot_times.csv"), "w") as f:
    writer_obj = writer(f)
    writer_obj.writerow(snapshot_times)
    f.close()

