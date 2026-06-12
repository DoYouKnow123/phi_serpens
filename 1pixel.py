import mesa_reader as mr
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap

# 1. Load the history data
history_data = mr.MesaData('LOGS/history.data')

# 2. Extract arrays and downsample for slow playback
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
ax.axis('off')

# Position the star dead-center with a 1-pixel marker size and no border lines
star, = ax.plot([], [], marker='o', markersize=1.0, markeredgewidth=0, zorder=2)
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)

# 5. Position the time readout overlay in the corner
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
    
    # Update the star point color (Locked at exactly 1 pixel in size)
    star.set_data([0], [0])
    star.set_markerfacecolor(color)
        
    # Update the timestamp readout
    time_text.set_text(f"Age: {current_age_gyr:.3f} Gyr")
    
    return star, time_text

# 8. Compile and save the animation at the 10x slower speed
num_frames = len(ages)
ani = FuncAnimation(fig, update, frames=num_frames, init_func=init, blit=True, interval=400)

output_filename = 'phi_serpens_1pixel_pure.gif'
print("Compiling pure 1-pixel star profile... Saving GIF.")
ani.save(output_filename, writer='pillow', fps=2.5, dpi=100)
print(f"Success! 1-pixel animation saved as {output_filename}")

plt.show()
