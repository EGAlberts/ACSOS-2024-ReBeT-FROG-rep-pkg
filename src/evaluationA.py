import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

OPACITY = 0.3

def apply_transparency(color):
    as_list = list(color)
    as_list[3] = OPACITY
    return tuple(as_list)

res_df = pd.read_csv("data/EvaluationA/1.csv")

categories = res_df["current_task"]

unique_categories = np.unique(categories)
num_categories = len(unique_categories)

# Choose a colormap
cmap = plt.get_cmap('Set2')  # You can choose other colormaps like 'viridis', 'plasma', etc.

# Create a dictionary mapping categories to colors
category_colors = {category: cmap(i / num_categories) for i, category in enumerate(unique_categories)}

current_category = categories[0]
start_index = 0
phases = []



# Iterate through the list
for i, category in enumerate(categories[1:], start=1):
    if category != current_category:
        # Detected a change in category, create a phase tuple
        phases.append((start_index, i, category_colors[current_category]))
        start_index = i
        current_category = category
    elif i == len(categories[1:]):
        phases.append((start_index, i, category_colors[current_category]))


x = np.arange(0, len(categories))
y = np.sin(0.1 * x)

# Create a figure and axis
fig, ax = plt.subplots()


# Add colored background spans for each phase
for start, end, color in phases:
    ax.axvspan(start, end, facecolor=color, alpha=OPACITY)


legend_labels = unique_categories
legend_handles = [plt.Rectangle((0, 0), 1, 1, color=apply_transparency(color)) for color in category_colors.values()]
legend_phases = ax.legend(legend_handles, legend_labels, loc='lower right', fontsize=14)

# Add the legends to the axis
ax.add_artist(legend_phases)

ax.set_xlabel('Time (s)', fontsize=16)  # Increase font size for x-axis label
ax.set_ylabel('MinBatterySystem', fontsize=16)  # Increase font size for y-axis label

plt.style.use('ggplot')
plt.margins(x=0)
plt.plot(res_df["power_status"])

ax.set_yticklabels(["Satisfied","Below\nMinimum"], fontsize=14)  # Increase font size for y-axis tick labels
ax.tick_params(axis='x', which='major', labelsize=14)

plt.show()