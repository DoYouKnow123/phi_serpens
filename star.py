import mesa_reader as mr
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap

# 1. Load the history data
history_data = mr.MesaData('LOGS/history.data')
ages_gyr = history_data.star_age / 1e9  # Scales from years to Gyr
radii_solar = history_data.R            # Radius in solar units (R_sun)
# 3. Define your target age in Gyr

# 2. Extract arrays and downsample for smooth playback
step = 10 
ages = history_data.star_age[::step]
teff = (10**history_data.log_Teff)[::step]

# 3. Define the physically accurate human-eye color map (3500K - 6400K)
stellar_hex_colors = ["#ff3800", "#ff8b3d", "#ffb07a", "#fff4ea", "#f8f7ff", "#d1e6ff", "#b8d5ff"]
true_stellar_cmap = LinearSegmentedColormap.from_list("true_stellar", stellar_hex_colors)
norm = plt.Normalize(vmin=3800, vmax=6400)

# 4. Set up dark canvas without any axes, ticks, or borders
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(8, 8), facecolor='black')
ax.set_facecolor('black')

# Hide all grid lines and graph framing elements
ax.axis('off')

# Position the star dead-center in our coordinate space
star, = ax.plot([0], [0], marker='o', markersize=20, markeredgecolor='white', markeredgewidth=0.5, zorder=2)

# Keep the window framed tightly around the central coordinate
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)

# 5. Position a clean time readout overlay in the top-left corner
time_text = ax.text(-0.9, 0.85, '', fontsize=14, color='white', fontfamily='monospace', weight='bold')

# 6. Initialize frame elements
def init():
    star.set_data([], [])
    time_text.set_text('')
    return star, time_text

# 7. Animation frame update loop
def update(frame):
    current_temp = teff[frame]
    current_age_gyr = ages[frame] / 1e9
    
    # Extract the true perceived color based on temperature
    color = true_stellar_cmap(norm(current_temp))
    
    # Update the star point color
    star.set_data([0], [0])
    star.set_markerfacecolor(color)
    
    # Optional: Slightly scale marker size to visualize the actual physical expansion of the giant phase
    # Comment this out if you prefer the point of light to remain exactly a constant size
    target_age_gyr = current_age_gyr 
    interpolated_radius = np.interp(target_age_gyr, ages_gyr, radii_solar)
    star.set_markersize(20+interpolated_radius)  
    # Update the timestamp readout
    time_text.set_text(f"Age: {current_age_gyr:.3f} Gyr")
    
    return star, time_text

# 8. Compile and save the animation
num_frames = len(ages)
ani = FuncAnimation(fig, update, frames=num_frames, init_func=init, blit=True, interval=400)

output_filename = 'phi_serpens_star_only.gif'
print("Compiling star profile... Saving GIF.")
ani.save(output_filename, writer='pillow', fps=2.5, dpi=100)
print(f"Success! Visual animation saved as {output_filename}")

# Display the window playback
plt.show()
