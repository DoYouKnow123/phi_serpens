import mesa_reader as mr
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap

# 1. Load the history data
history_data = mr.MesaData('LOGS/history.data')

# 2. Extract arrays
ages = history_data.star_age
luminosities = history_data.L
teff = 10**history_data.log_Teff  # Effective temperature in Kelvin

# 3. Format coordinates into segments for LineCollection
points = np.array([ages, luminosities]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

# 4. Initialize the figure
fig, ax = plt.subplots(figsize=(10, 6))

# 5. Define a physically accurate human-eye stellar colormap
# Mapped sequentially from cool/red (left, 3500K) to hot/blue (right, 7500K)
stellar_hex_colors = [
    "#ff3800",  # 3,500 K  (Deep Red-Orange / M-dwarf / cool giant)
    "#ff8b3d",  # 4,200 K  (Orange / K-giant / Current Phi Serpens)
    "#ffb07a",  # 4,800 K  (Light Orange-Yellow)
    "#fff4ea",  # 5,500 K  (Pale Yellow-White / G-dwarf / Sun-like)
    "#f8f7ff",  # 6,100 K  (Pure White / F-dwarf)
    "#d1e6ff",  # 6,800 K  (Pale Sky Blue / A-dwarf)
    "#b8d5ff"   # 7,500 K  (Soft Light Blue)
]

# Create the matplotlib colormap object
true_stellar_cmap = ListedColormap(stellar_hex_colors)

# Normalize the temperatures to match our hex boundaries
# Bounds 3,800K to 6,400K cover the exact spectrum your 1.25 M_sun star runs through
norm = plt.Normalize(vmin=3800, vmax=6400) 
lc = LineCollection(segments, cmap=true_stellar_cmap, norm=norm)

# 6. Apply temperature array and line thickness
lc.set_array(teff)
lc.set_linewidth(4.0)  # Thicker line makes the subtle color shifts easier to see
line = ax.add_collection(lc)

# 7. Add the realistic temperature colorbar
cbar = fig.colorbar(line, ax=ax, pad=0.02)
cbar.set_label('Perceived Human Eye Color vs $T_{\\text{eff}}$ (Kelvin)', fontsize=11)
cbar.ax.invert_yaxis()  # Puts hotter temperatures (blue-white) at the top

# 8. Mark the physical milestones of Phi Serpentis
ax.axvline(x=3.42e9, color='black', linestyle='--', alpha=0.4, label='Observed Age (3.42 Gyr)')
ax.axhline(y=41.7, color='black', linestyle=':', alpha=0.4, label='Observed $L_{\\odot}$ (~41.7)')

# 9. Format labels and log scales
ax.set_xlabel('Stellar Age (Years)', fontsize=12)
ax.set_ylabel('Luminosity ($L_{\\odot}$)', fontsize=12)
ax.set_title('$\\phi$ Serpentis: Visually Realistic Stellar Color Track', fontsize=14, weight='bold')

ax.set_xscale('log')
ax.set_yscale('log')

# Manual limits to properly bound the canvas
ax.set_xlim(ages.min() * 0.9, ages.max() * 1.1)
ax.set_ylim(luminosities.min() * 0.9, luminosities.max() * 1.1)

ax.grid(True, linestyle='--', alpha=0.25)
ax.legend(loc='lower left')
plt.savefig('actualcolor.png')
# 10. Display the plot
plt.show()
