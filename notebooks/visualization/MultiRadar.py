from typing import List
import matplotlib.pyplot as plt
import matplotlib.path as path
import csv
import os
from math import pi
import sys
sys.path.append('d:\\VScodeProject\\ESG-GPT\\notebooks\\')
# Set the number of self.angles and the values for each angle
from utils.utils import get_lda_list

class MultiRadar():
    def __init__(self, nation, png_path, csv_folder_path, label_cnt) -> None:
        self.LABEL_CNT = label_cnt
        self.ax = None
        self.angles = None
        self.NATION = nation
        self.png_type = None
        self.PNG_PATH = png_path
        self.categories = get_lda_list(self.LABEL_CNT)
        self.CSV_PATH = csv_folder_path
        self.TAIWAN_CSV_PATH = f'{self.CSV_PATH}/taiwan'
        self.AMERICAN_CSV_PATH = f'{self.CSV_PATH}/american'
        
    def _plot(self, to_plot, label=None):
        self.ax.plot(self.angles, to_plot, linewidth=1, linestyle='solid', label=label)
        self.ax.fill(self.angles, to_plot, 'b', alpha=0.1)

    def _save_plot(self, output_path, output_name, title):
        plt.suptitle(title, fontsize=30)
        plt.legend( bbox_to_anchor=(-0.12, 1.15) ,fontsize='25')
        plt.savefig(f'{output_path}/{output_name}', format='png', dpi=96)

    def _read_csv(self, file_path):
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            labels = []
            counts = []
            # Iterate through the rows of the CSV file
            for row in reader:
                #   collect column value
                labels.append(row[1])
            for i in range(self.LABEL_CNT):
                # count label number in collected column value
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
        return normalized_values
    
    def initfig(self):
        plt.close()
        plt.figure(figsize=(1920 / 96, 1080 / 96), dpi=96)
        # What will be the angle of each self.axis in the plot? (we divide the plot / number of variable)
        self.angles = [n / float(self.LABEL_CNT) * 2 * pi for n in range(self.LABEL_CNT)]
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

    
    def draw_company_average(self, csv_path):
        self.png_type = 'company vs. average'
        filenames: List[str] = os.listdir(csv_path)
        for filename in filenames:
            self.ax, self.angles = self.initfig()
            average = self._get_average(csv_path)
            self._plot(average, 'average')
            values = self._read_csv(f'{csv_path}/{filename}')
            values += values[:1]
            filename = filename.strip('.csv')
            self._plot(values, f'{filename.strip('.csv')}')
            self._save_plot(f'{self.PNG_PATH}/{self.NATION}', f'{filename} vs. average.png', f'{filename} vs. average')
            
    def draw_full25(self, csv_path):
        filenames = os.listdir(csv_path)
        self.ax, self.angles = self.initfig()
        for filename in filenames:
            values = self._read_csv(f'{csv_path}/{filename}')
            values += values[:1]
            self._plot(values)
        self._save_plot(f'{self.PNG_PATH}/{self.NATION}', 'full 25 company compare.png', f'{self.NATION} full 25 company compare')
        
    def draw_average(self, csv_path):
        self.ax, self.angles = self.initfig()
        average = self._get_average(csv_path)
        label = 'American Average' if self.NATION == 'american' else 'Taiwan Average'
        self._plot(average, label)
        self._save_plot(f'{self.PNG_PATH}/{self.NATION}', f'{self.NATION}_average.png', f'{self.NATION} Average')
    
    def taiwan_vs_american(self):
        self.ax, self.angles = self.initfig()
        average_taiwan = self._get_average(self.TAIWAN_CSV_PATH)
        self._plot(average_taiwan, label='Taiwan')
        average_american = self._get_average(self.AMERICAN_CSV_PATH)
        self._plot(average_american, label='American')
        self._save_plot(self.PNG_PATH, 'taiwan vs. american.png', 'Taiwan vs. American')
        
    def _get_average(self, csv_path):
        average = [0] * self.LABEL_CNT
        filenames = os.listdir(csv_path)
        company_values = []
        for filename in filenames:
            values = self._read_csv(f'{csv_path}/{filename}', )
            values += values[:1]
            company_values.append(values)
            #   each 26 labels add to average[0] ~ average[26]
            for i in range(self.LABEL_CNT):
                average[i] += values[i]
        for i in range(self.LABEL_CNT):
            average[i] /= len(filenames)
        average += average[:1]
        return average
