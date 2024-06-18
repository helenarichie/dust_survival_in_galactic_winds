import sys
sys.path.insert(0, "/ix/eschneider/helena/code/my_scripts/")
from hconfig import *
import seaborn as sns

density_conversion = 5.028e-34/(3.24e-22)**3 # g/cm^3 to M_sun/kpc^3

##############################################
date = "frontier/2024-02-09"
datestr = "0209"
vlims_gas = (19.3, 22)
vlims_dust = (-9.6, -4.3)
fnum = 0
unit = "kpc"
spacing = 320*1e-3
##############################################

basedir = f"/ix/eschneider/helena/data/cloud_wind/{date}/"
projdir = os.path.join(basedir, "hdf5/proj/")
pngdir = os.path.join(basedir, "png/")

##############################################
cat = True
pad = 0.1
fontsize = 25
labelpad = 12
tickwidth = 2
ticklength = 13
##############################################

plt.rcParams.update({'font.family': 'Helvetica'})
plt.rcParams.update({'font.size': fontsize})
plt.style.use('dark_background')

cmap_gas = sns.color_palette("mako", as_cmap=True)
cmap_dust = sns.color_palette("rocket", as_cmap=True)

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20, 6))


data = ReadHDF5(projdir, proj="xy", cat=cat, dust=False, fnum=fnum)
head = data.head
conserved = data.conserved
dx = head["dx"][0]
nx, ny, nz = head["dims"]

# ylens = [int(ny/2), ny-int(ny/4), ny-int(ny/4)]
ylen = ny
xlen = nx
xs, ys = 0, 0

if unit == "pc":        
    dx *= 1e3  # pc 
d_gas = conserved["density"]
d_gas *= head["mass_unit"] / (head["length_unit"] ** 2)
n_gas = d_gas[0]/(0.6*MP) # column density
t = data.t_cgs() / yr_in_s  # yr

im = ax.imshow(np.log10(n_gas[xs:(xs+xlen),ys:(ys+ylen)].T), origin="lower", vmin=vlims_gas[0], vmax=vlims_gas[1], extent=[0, xlen*dx, 0, ylen*dx], cmap=cmap_gas)

ax.hlines(spacing, 1*spacing, 2*spacing, color='white', linewidth=2)
ax.text(2*spacing+0.05, spacing-0.05, '320 pc', color='white', fontsize=fontsize)
ax.text(15*spacing+0.05, spacing-0.05, r'$6.4\times1.6\times1.6\,\,kpc^3$', color='white', fontsize=fontsize)
ax.text(14.5*spacing, dx*ylen-(spacing+0.05), r'$2048\times512\times512\,\,cells$', color='white', fontsize=fontsize)

yticks = [ylen*dx/2-spacing/2-spacing, ylen*dx/2-spacing/2, ylen*dx/2+spacing/2, ylen*dx/2+spacing/2+spacing]
xticks = [ylen*dx/2-spacing/2-spacing, ylen*dx/2-spacing/2, ylen*dx/2+spacing/2, ylen*dx/2+spacing/2+spacing]

ax.set_xticks(np.delete(np.arange(0, xlen*dx, spacing), 0))
ax.set_yticks(np.delete(np.arange(0, ylen*dx, spacing), 0))
ax.tick_params(axis='both', which='both', direction='in', color='white', labelleft=0, labelbottom=0, top=1, right=1, length=ticklength, width=tickwidth)

[x.set_linewidth(1.25) for x in ax.spines.values()]
[x.set_color('white') for x in ax.spines.values()]

divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.07)
cbar = fig.colorbar(im, cax=cax)
cbar.set_label(r'$\mathrm{log}_{10}(N_{H, gas})$ [$\mathrm{cm}^{-2}$]', rotation=270, labelpad=40, fontsize=fontsize-2)
cbar.ax.tick_params(length=ticklength, width=tickwidth, color="white", labelsize=fontsize-8)
cbar_spacing = (vlims_gas[1] - vlims_gas[0])/8
cbar.set_ticks(np.linspace(vlims_gas[0]+cbar_spacing, vlims_gas[1]-cbar_spacing, 4).round(1))
cbar.outline.set_edgecolor('white')
cbar.outline.set_linewidth(1.25)
"""
cbar_height = 0.385
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.8, 0.0, 0.03, cbar_height])
cbar = fig.colorbar(im, cax=cbar_ax)
cbar.set_label(r'$\mathrm{log}_{10}(N_{H, gas})$ [$\mathrm{cm}^{-2}$]', rotation=270, labelpad=50, fontsize=fontsize-2)
cbar.ax.tick_params(length=ticklength, width=tickwidth, color="white", labelsize=fontsize-7)
cbar_spacing = (vlims_dust[1] - vlims_dust[0])/8
cbar.set_ticks(np.linspace(vlims_dust[0]+cbar_spacing, vlims_dust[1]-cbar_spacing, 4).round(1))
cbar.outline.set_edgecolor("white")
cbar.outline.set_linewidth(4)
"""

plt.savefig(pngdir + f"IC_snapshot_dark.png", dpi=300, bbox_inches="tight")
