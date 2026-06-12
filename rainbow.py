import mesa_reader as mr
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection

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

# 5. Dynamic Scaling: Set vmax higher than the maximum temp to avoid the dark/black clipping zone
min_temp = teff.min()
max_temp = teff.max()

# Padding vmax slightly (adding ~200K) pushes the track away from the darkest purple/black edge
norm = plt.Normalize(vmin=min_temp - 50, vmax=max_temp + 200) 

# Use 'turbo_r' for the full vibrant rainbow sequence
lc = LineCollection(segments, cmap='turbo_r', norm=norm)

# 6. Apply temperature array and line thickness
lc.set_array(teff)
lc.set_linewidth(3.5)
line = ax.add_collection(lc)

# 7. Add the rainbow colorbar
cbar = fig.colorbar(line, ax=ax, pad=0.02)
cbar.set_label('Effective Temperature $T_{\\text{eff}}$ (Kelvin)', fontsize=11)
cbar.ax.invert_yaxis() # High temps (blue) at the top, low temps (red) at the bottom

# 8. Mark the physical milestones of Phi Serpentis
ax.axvline(x=3.42e9, color='black', linestyle='--', alpha=0.4, label='Observed Age (3.42 Gyr)')
ax.axhline(y=41.7, color='black', linestyle=':', alpha=0.4, label='Observed $L_{\\odot}$ (~41.7)')

# 9. Format labels and log scales
ax.set_xlabel('Stellar Age (Years)', fontsize=12)
ax.set_ylabel('Luminosity ($L_{\\odot}$)', fontsize=12)
ax.set_title('$\\phi$ Serpentis: Clean Rainbow Temperature Track', fontsize=14, weight='bold')

ax.set_xscale('log')
ax.set_yscale('log')

# Manual limits to bound the LineCollection canvas
ax.set_xlim(ages.min() * 0.9, ages.max() * 1.1)
ax.set_ylim(luminosities.min() * 0.9, luminosities.max() * 1.1)

ax.grid(True, linestyle='--', alpha=0.3)
ax.legend(loc='lower left')
plt.savefig('colortemp.png')
# 10. Display the plot
plt.show()
