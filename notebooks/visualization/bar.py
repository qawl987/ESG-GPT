import matplotlib.pyplot as plt
import matplotlib.path as path
import csv
import numpy as np
from math import pi
# Set the number of angles and the values for each angle
with open('./american_csv_new/15_itt_1_44.csv', 'r') as f:
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
# We are going to plot the first line of the data frame.
# But we need to repeat the first value to close the circular graph:
x_pos = np.arange(len(categories))
plt.figure(figsize=(1680 / 96, 1080 / 96), dpi=96)
plt.bar(x_pos, values)
plt.xticks(x_pos, categories, rotation=80)
plt.subplots_adjust(bottom=0.4, top=0.99)
# Show the graph

plt.show()