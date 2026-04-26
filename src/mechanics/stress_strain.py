import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
data = pd.read_excel(r"Folder\stress_strain_raw.xlsx") #Input here 

strain = data["Strain"].values #unit mm/mm
stress = data["Stress"].values #unit MPA

# Elastic modulus 
elastic_limit = 0.001
elastic_strain = strain[strain <= elastic_limit]
elastic_stress = stress[strain <= elastic_limit]

E, c = np.polyfit(elastic_strain, elastic_stress, 1)

# 0.2% offset yield strength
offset = 0.002
offset_line = E * (strain - offset)

diff = np.abs(stress - offset_line)
idx = np.argmin(diff)

YS = stress[idx]
YS_strain = strain[idx]

# UTS
UTS = np.max(stress)
UTS_idx = np.argmax(stress)
UTS_strain = strain[UTS_idx]

# PLOT
plt.rcParams['font.family'] = 'Times New Roman'

fig, ax = plt.subplots(figsize=(7,5))

# Main curve
ax.plot(strain, stress, color='black', linewidth=2.2, label='Stress–Strain')

# Elastic fit
ax.plot(elastic_strain, E*elastic_strain, linestyle='--', linewidth=2, label='Elastic fit')

# Offset line
ax.plot(strain, offset_line, linestyle='-.', linewidth=2, label='0.2% Offset')

# Points
ax.scatter(YS_strain, YS, s=60)
ax.scatter(UTS_strain, UTS, s=60)

# Annotations
ax.text(YS_strain, YS, '  YS', fontsize=14, fontweight='bold')
ax.text(UTS_strain, UTS, '  UTS', fontsize=14, fontweight='bold')

# Labels (BIG + BOLD)
ax.set_xlabel("Strain (mm/mm)", fontsize=24, fontweight='bold')
ax.set_ylabel("Stress (MPa)", fontsize=24, fontweight='bold')

# Ticks
ax.tick_params(axis='both', which='major', labelsize=16)

# FULL BOX (all spines visible & thick)
for spine in ax.spines.values():
    spine.set_linewidth(2)

# Remove grid
ax.grid(False)

# Legend (clean)
ax.legend(fontsize=14, frameon=False)

plt.tight_layout()
plt.show()
