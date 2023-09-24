import matplotlib.pyplot as plt
import matplotlib.path as path
import csv
import os
from math import pi
# Set the number of self.angles and the values for each angle
from readcsv import readcsv

class MultiRadar():
    categories = ['Business_Ethics:0', 'Data_Security:1', 'Access_And_Affordability:2', 'Business_Model_Resilience:3',
              'Competitive_Behavior:4', 'Critical_Incident_Risk_Management:5', 'Customer_Welfare:6',
              'Director_Removal:7', 'Employee_Engagement_Inclusion_And_Diversity:8', 'Employee_Health_And_Safety:9',
              'Human_Rights_And_Community_Relations:10', 'Labor_Practices:11', 'Management_Of_Legal_And_Regulatory_Framework:12',
              'Physical_Impacts_Of_Climate_Change:13', 'Product_Quality_And_Safety:14', 'Product_Design_And_Lifecycle_Management:15',
              'Selling_Practices_And_Product_Labeling:16', 'Supply_Chain_Management:17', 'Systemic_Risk_Management:18',
              'Waste_And_Hazardous_Materials_Management:19', 'Water_And_Wastewater_Management:20', 'Air_Quality:21',
              'Customer_Privacy:22', 'Ecological_Impacts:23', 'Energy_Management:24', 'GHG_Emissions:25'
              ]
    # categories = ['Business Ethics:0', 'Data Security:1', 'Access And Affordability:2', 'Business Model Resilience:3',
    # 'Competitive Behavior:4', 'Critical Incident Risk Management:5', 'Customer Welfare:6',
    # 'Director Removal:7', 'Employee Engagement Inclusion And Diversity:8', 'Employee Health And Safety:9',
    # 'Human Rights And Community Relations:10', 'Labor Practices:11', 'Management Of Legal And Regulatory Framework:12',
    # 'Physical Impacts Of Climate Change:13', 'Product Quality And Safety:14', 'Product Design And Lifecycle Management:15',
    # 'Selling Practices And Product Labeling:16', 'Supply Chain Management:17', 'Systemic Risk Management:18',
    # 'Waste And Hazardous Materials Management:19', 'Water And Wastewater Management:20', 'Air Quality:21',
    # 'Customer Privacy:22', 'Ecological Impacts:23', 'Energy Management:24', 'GHG Emissions:25', 'No Enough Information:26'
    # ]

    def __init__(self, N, nation, word_cnt, png_directory) -> None:
        self.N = N
        self.ax = None
        self.angles = None
        self.nation = nation
        self.word_cnt = word_cnt
        self.png_type = None
        self.png_directory = png_directory

    def initfig(self):
        plt.figure(figsize=(1920 / 96, 1080 / 96), dpi=96)
        # What will be the angle of each self.axis in the plot? (we divide the plot / number of variable)
        self.angles = [n / float(self.N) * 2 * pi for n in range(self.N)]
        self.angles += self.angles[:1]
        # Initialise the spider plot
        self.ax = plt.subplot(111, polar=True)
        #   set the plt start at top and turn clockwise
        self.ax.set_theta_offset(pi / 2)
        self.ax.set_theta_direction(direction='clockwise')
        # Draw one self.axe per variable + add labels
        plt.xticks(self.angles[:-1], self.categories, color='black', size=14)
        #   set the x label position to not collision
        rstep = int(self.ax.get_theta_direction())
        if rstep > 0:
            rmin = 0
            rmax = len(self.angles)
        else:
            rmin = len(self.angles) - 1
            rmax = -1

        for label, i in zip(self.ax.get_xticklabels(), range(rmin, rmax, rstep)):
            angle_rad = self.angles[i] + self.ax.get_theta_offset()
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
        # Draw ylabels
        self.ax.set_rlabel_position(0)
        plt.yticks([20, 40, 60, 80], ["20", "40", "60", "80"], color="black", size=16)
        plt.ylim(0, 100)
        self.angles = self.angles
        return self.ax, self.angles

    
    def draw_company_average(self, read_directory):
        self.png_type = 'company vs. average'
        filenames = os.listdir(read_directory)
        for filename in filenames:
            plt.close()
            self.ax, self.angles = self.initfig()
            average = self.get_average(read_directory, False)
            # self.ax.plot(self.angles, average, linewidth=1, linestyle='solid', label='average')
            # self.ax.fill(self.angles, average, 'b', alpha=0.1)
            values = readcsv(f'{read_directory}', filename)
            values += values[:1]
            filename = filename.strip('.csv')
            self.ax.plot(self.angles, values, linewidth=1, linestyle='solid', label=f'{filename}')
            self.ax.fill(self.angles, values, 'b', alpha=0.1)
            # plt.suptitle(f'{self.nation}_{self.word_cnt} {filename} {self.png_type}', fontsize=30)
            plt.suptitle(f'{filename} {self.png_type}', fontsize=30)
            # plt.legend(loc='center right', bbox_to_anchor=(0.1, 1.0), fontsize='20')
            plt.legend( bbox_to_anchor=(-0.09, 1.15) ,fontsize='25')
            plt.savefig(f'../png/{self.png_directory}/{filename}_{self.png_type}.png', format='png', dpi=96)
        # filename = '21_microsoft_1_89.csv'
        # self.ax, self.angles = self.initfig()
        # average = self.get_average(read_directory, False)
        # self.ax.plot(self.angles, average, linewidth=1, linestyle='solid', label='average')
        # self.ax.fill(self.angles, average, 'b', alpha=0.1)
        # values = readcsv(f'{read_directory}', filename)
        # values += values[:1]
        # filename = filename.strip('.csv')
        # self.ax.plot(self.angles, values, linewidth=1, linestyle='solid', label=f'{filename}')
        # self.ax.fill(self.angles, values, 'b', alpha=0.1)
        # # plt.suptitle(f'{self.nation}_{self.word_cnt} {filename} {self.png_type}', fontsize=30)
        # plt.suptitle(f'Microsoft vs. average', fontsize=30)
        # # plt.legend(loc='center right', bbox_to_anchor=(0.1, 1.0), fontsize='20')
        # plt.legend( bbox_to_anchor=(-0.09, 1.15) ,fontsize='25')
        # plt.savefig(f'./png/{self.png_directory}/{filename}_{self.png_type}.png', format='png', dpi=96)
    def draw_full25(self, read_directory):
        self.png_type = 'full 25 company compare'
        filenames = os.listdir(read_directory)
        plt.close()
        self.ax, self.angles = self.initfig()
        for filename in filenames:
            values = readcsv(f'{read_directory}', filename)
            values += values[:1]
            self.ax.plot(self.angles, values, linewidth=1, linestyle='solid')
            self.ax.fill(self.angles, values, 'b', alpha=0.1)
        plt.suptitle(f'{self.nation}_{self.word_cnt} {self.png_type}', fontsize=30)
        # plt.legend( bbox_to_anchor=(-0.09, 1.15) ,fontsize='25')
        plt.savefig(f'../png/{self.png_directory}/{self.png_type}.png', format='png', dpi=96)
    
    def label_vs_human(self, read_directory):
        self.png_type = 'label'
        filenames = os.listdir(read_directory)
        plt.close()
        self.ax, self.angles = self.initfig()
        for filename in filenames:
            values = readcsv(f'{read_directory}', filename)
            values += values[:1]
            self.ax.plot(self.angles, values, linewidth=1, linestyle='solid')
            self.ax.fill(self.angles, values, 'b', alpha=0.1)
        plt.suptitle(f'{self.nation}_{self.word_cnt} {self.png_type}', fontsize=30)
        plt.savefig(f'./png/{self.png_directory}/{self.png_type}.png', format='png', dpi=96)
        
    def get_average(self, read_directory, draw):
        self.png_type = 'average'
        if draw:
            plt.close()
            self.ax, self.angles = self.initfig()
        self.ax, self.angles = self.initfig()
        
        average = self._draw_get_average(read_directory)
        
        # 畫平均
        if draw:
            plt.suptitle(f'{self.nation}_{self.word_cnt} {self.png_type}', fontsize=30)
            plt.savefig(f'../png/{self.png_directory}/{self.png_type}.png', format='png', dpi=96)
        return average
    
    def taiwan_vs_american(self, read_directory):
        self.ax, self.angles = self.initfig()
        read_directory = f'../csv/predict_american_xml/'
        self._draw_get_average(read_directory)
        read_directory = f'../csv/predict_taiwan_xml/'
        self._draw_get_average(read_directory)
        plt.suptitle(f'Taiwan vs. American', fontsize=30)
        plt.legend( bbox_to_anchor=(-0.12, 1.15) ,fontsize='25')
        plt.savefig(f'../png/taiwanvsamerican.png', format='png', dpi=96)
        
    def _draw_get_average(self, read_directory):
        label = 'American Average' if 'american' in read_directory else 'Taiwan Average '
        average = [0] * self.N
        filenames = os.listdir(read_directory)
        company_values = []
        for filename in filenames:
            values = readcsv(f'{read_directory}', filename)
            values += values[:1]
            company_values.append(values)
            #   each 26 labels add to average[0] ~ average[26]
            for i in range(self.N):
                average[i] += values[i]
        for i in range(self.N):
            average[i] /= len(filenames)
        average += average[:1]
        self.ax.plot(self.angles, average, linewidth=1, linestyle='solid', label=label)
        self.ax.fill(self.angles, average, 'b', alpha=0.1)
        
        return average
    
    # 搞不懂
    # def get_average(self, read_directory, draw):
    #     self.png_type = 'average'
    #     if draw:
    #         plt.close()
    #         self.ax, self.angles = self.initfig()
    #     self.ax, self.angles = self.initfig()
    #     # read_directory = f'./predict_american_eight/'
    #     # 畫 美國公司的
    #     average = [0] * self.N
    #     filenames = os.listdir(read_directory)
    #     company_values = []
    #     for filename in filenames:
    #         values = readcsv(f'{read_directory}', filename)
    #         values += values[:1]
    #         company_values.append(values)
    #         #   each 26 labels add to average[0] ~ average[26]
    #         for i in range(self.N):
    #             average[i] += values[i]
    #     for i in range(self.N):
    #         average[i] /= len(filenames)
    #     average += average[:1]
    #     # self.ax.plot(self.angles, average, linewidth=1, linestyle='solid', label='American')
    #     # self.ax.fill(self.angles, average, 'b', alpha=0.1)
        
            
    #     # 拿台灣公司平均 並畫圖
    #     # average = [0] * self.N
    #     # read_directory = f'./predict_taiwan_eight/'
    #     # filenames = os.listdir(read_directory)
    #     # company_values = []
    #     # for filename in filenames:
    #     #     values = readcsv(f'{read_directory}', filename)
    #     #     values += values[:1]
    #     #     company_values.append(values)
    #     #     #   each 26 labels add to average[0] ~ average[26]
    #     #     for i in range(self.N):
    #     #         average[i] += values[i]
    #     # for i in range(self.N):
    #     #     average[i] /= len(filenames)
    #     # average += average[:1]
    #     # self.ax.plot(self.angles, average, linewidth=1, linestyle='solid', label='Taiwan')
    #     # self.ax.fill(self.angles, average, 'b', alpha=0.1)
    #     # plt.suptitle(f'Taiwan vs. American', fontsize=30)
    #     # plt.legend( bbox_to_anchor=(-0.12, 1.15) ,fontsize='25')
    #     # plt.savefig(f'./png/taiwanvsamerican.png', format='png', dpi=96)
        
    #     # 畫平均
    #     if draw:
    #         self.ax.plot(self.angles, average, linewidth=1, linestyle='solid', label='average')
    #         self.ax.fill(self.angles, average, 'b', alpha=0.1)
    #         plt.suptitle(f'{self.nation}_{self.word_cnt} {self.png_type}', fontsize=30)
    #         plt.savefig(f'../png/{self.png_directory}/{self.png_type}.png', format='png', dpi=96)
    #     return average