import matplotlib.pyplot as plt
import matplotlib.path as path
import csv
from math import pi
# Set the number of angles and the values for each angle
with open('./american_csv/15_itt_1_44.csv', 'r') as f:
    # Create a CSV reader object
    reader = csv.reader(f)
    labels = []
    counts = []
    # Iterate through the rows of the CSV file
    for row in reader:
        labels.append(row[1])
    for i in range(26):
        count = labels.count(str(i))
        counts.append(count)
# Set data
values = counts
min_value = min(values)
max_value = max(values)
# Calculate the range of the values
value_range = max_value - min_value
# Normalize the values and store them in a new list
normalized_values = []
for value in values:
    normalized_value = ((value - min_value) / value_range) * 100
    normalized_value = int(normalized_value)
    normalized_values.append(normalized_value)
# number of variable
N = 26
categories = ['Business_Ethics:0', 'Data_Security:1', 'Access_And_Affordability:2', 'Business_Model_Resilience:3',
              'Competitive_Behavior:4', 'Critical_Incident_Risk_Management:5', 'Customer_Welfare:6',
              'Director_Removal:7', 'Employee_Engagement_Inclusion_And_Diversity:8', 'Employee_Health_And_Safety:9',
              'Human_Rights_And_Community_Relations:10', 'Labor_Practices:11', 'Management_Of_Legal_And_Regulatory_Framework:12',
              'Physical_Impacts_Of_Climate_Change:13', 'Product_Quality_And_Safety:14', 'Product_Design_And_Lifecycle_Management:15',
              'Selling_Practices_And_Product_Labeling:16', 'Supply_Chain_Management:17', 'Systemic_Risk_Management:18',
              'Waste_And_Hazardous_Materials_Management:19', 'Water_And_Wastewater_Management:20', 'Air_Quality:21',
              'Customer_Privacy:22', 'Ecological_Impacts:23', 'Energy_Management:24', 'GHG_Emissions:25'
              ]
print(len(categories))
# We are going to plot the first line of the data frame.
# But we need to repeat the first value to close the circular graph:
values += values[:1]

# What will be the angle of each axis in the plot? (we divide the plot / number of variable)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

# Initialise the spider plot
ax = plt.subplot(111, polar=True)
#
ax.set_theta_offset(pi / 2)
ax.set_theta_direction(direction='clockwise')
# Draw one axe per variable + add labels
plt.xticks(angles[:-1], categories, color='grey', size=8)
#   set the x label position to not collision
rstep = int(ax.get_theta_direction())
if rstep > 0:
    rmin = 0
    rmax = len(angles)
else:
    rmin = len(angles) - 1
    rmax = -1

for label, i in zip(ax.get_xticklabels(), range(rmin, rmax, rstep)):
    angle_rad = angles[i] + ax.get_theta_offset()
    if angle_rad <= pi / 2:
        ha = 'left'
        va = "bottom"
    elif pi / 2 < angle_rad <= pi:
        ha = 'right'
        va = "bottom"
    elif pi < angle_rad <= (3 * pi / 2):
        ha = 'right'
        va = "top"
    else:
        ha = 'left'
        va = "top"
    label.set_verticalalignment(va)
    label.set_horizontalalignment(ha)
#
# plt.thetagrids(angles[:-1], labels=categories, fontsize=8, rotation=2 * pi / float(N))
# Draw ylabels
ax.set_rlabel_position(0)
plt.yticks([20, 40, 60, 80], ["20", "40", "60", "80"], color="grey", size=7)
plt.ylim(0, 100)

# Plot data
ax.plot(angles, values, linewidth=1, linestyle='solid')

# Fill area
ax.fill(angles, values, 'b', alpha=0.1)

# Show the graph

plt.show()