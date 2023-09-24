import matplotlib.pyplot as plt
import matplotlib.path as path
import csv
import os
from math import pi
# Set the number of angles and the values for each angle
from readcsv import readcsv
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
#   -------draw background
def initfig():
    plt.figure(figsize=(1400 / 96, 1080 / 96), dpi=96)
    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    # Initialise the spider plot
    ax = plt.subplot(111, polar=True)
    #   set the plt start at top and turn clockwise
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
    # plt.yticks([10, 20, 30], ["10", "20", "30"], color="grey", size=7)
    # plt.ylim(0, 40)
    return ax, angles
# ---------choose directory
# Plot data
word_cnts = ['eight', 'five']
nations = ['american', 'taiwan']
png_type = 'full 25 company compare'
# png_type = 'company vs. average'
# png_type = 'average'
# png_type = 'testpercentage'
#   ------choose figure
def draw_full25(read_directory):
    filenames = os.listdir(read_directory)
    plt.close()
    ax, angles = initfig()
    for filename in filenames:
        values = readcsv(f'{read_directory}', filename)
        values += values[:1]
        ax.plot(angles, values, linewidth=1, linestyle='solid')
        ax.fill(angles, values, 'b', alpha=0.1)
    plt.suptitle(f'{nation}_{word_cnt} {png_type}', fontsize=30)
    plt.savefig(f'./png/{png_directory}/{png_type}.png', format='png', dpi=96)
def get_average(read_directory):
    # plt.close()
    # ax, angles = initfig()
    average = [0] * N
    filenames = os.listdir(read_directory)
    company_values = []
    for filename in filenames:
        values = readcsv(f'{read_directory}', filename)
        values += values[:1]
        company_values.append(values)
        #   each 26 labels add to average[0] ~ average[26]
        for i in range(N):
            average[i] += values[i]
    for i in range(N):
        average[i] /= len(filenames)
    average += average[:1]
    ax.plot(angles, average, linewidth=1, linestyle='solid', label='average')
    ax.fill(angles, average, 'b', alpha=0.1)
    # plt.suptitle(f'{nation}_{word_cnt} {png_type}', fontsize=30)
    # plt.savefig(f'./png/{png_directory}/{png_type}.png', format='png', dpi=96)
    return average
def draw_company_average(read_directory):
    filenames = os.listdir(read_directory)
    for filename in filenames:
        plt.close()
        ax, angles = initfig()
        average = get_average(read_directory)
        ax.plot(angles, average, linewidth=1, linestyle='solid', label='average')
        ax.fill(angles, average, 'b', alpha=0.1)
        values = readcsv(f'{read_directory}', filename)
        values += values[:1]
        filename = filename.strip('.csv')
        ax.plot(angles, values, linewidth=1, linestyle='solid', label=f'{filename}')
        ax.fill(angles, values, 'b', alpha=0.1)
        plt.suptitle(f'{nation}_{word_cnt} {filename} {png_type}', fontsize=30)
        plt.legend(loc='center right', bbox_to_anchor=(0.1, 1.0), fontsize='20')
        plt.savefig(f'./png/{png_directory}/{filename}_{png_type}.png', format='png', dpi=96)

for word_cnt in word_cnts:
    for nation in nations:
        read_directory = f'./predict_{nation}_{word_cnt}/'
        png_directory = f'./{nation}/{word_cnt}'
        filenames = os.listdir(read_directory)
        #   choose picture to draw
        # get_average(read_directory)
        draw_full25(read_directory)
        # draw_company_average(read_directory)

#   ------test
ax, angles = initfig()
# ex = [90,80,85,90,95,80,90,70,80,85,94,74,60,90,80,91,50,80,80,100,50,70,80,75,89,90,90]
# ax.plot(angles, ex, linewidth=1, linestyle='solid', label='average')
# ax.fill(angles, ex, 'b', alpha=0.1)
# plt.suptitle(f'Ideal', fontsize=30)
# plt.show()
# word_cnt = 'eight'
word_cnt = 'five'
# nation = 'american'
nation = 'taiwan'
read_directory = f'./predict_{nation}_{word_cnt}/'
png_directory = f'{nation}/{word_cnt}'
# # # # draw_full25(read_directory)
# draw_company_average(read_directory)
get_average(read_directory)
nation = 'american'
read_directory = f'./predict_{nation}_{word_cnt}/'
get_average(read_directory)
#   ------plot
# plt.suptitle(f'{nation}_{word_cnt} {png_type}', fontsize=8)
plt.savefig(f'./png/{png_directory}/american vs taiwan.png', format='png', dpi=96)
plt.show()