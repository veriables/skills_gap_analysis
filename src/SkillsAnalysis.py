import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from adjustText import adjust_text
sns.set_theme()
from config import CONFIG

class SkillsAnalysis():
    def __init__(self, raw_data_df):
        self.data = raw_data_df
        self.job_postings_mean = 0
        self.applicants_mean = 0
        self.job_postings_std = 0
        self.applicants_std = 0

    def setDescriptiveStatistics(self):
        '''
            Calculate and record the mean and standard deviation 
            values for job_postings and applicants.
        '''
        self.job_postings_mean = self.data['Job_Posting_Count'].mean()
        self.job_postings_std = self.data['Job_Posting_Count'].std()
        self.job_postings_min = self.data['Job_Posting_Count'].min()
        self.job_postings_max = self.data['Job_Posting_Count'].max()

        self.applicants_mean = self.data['Applicant_Count'].mean()
        self.applicants_std = self.data['Applicant_Count'].std()
        self.applicants_min = self.data['Applicant_Count'].min()
        self.applicants_max = self.data['Applicant_Count'].max()

    def dropZeroedData(self):
        '''
            If there are any skills listed that have zero counts (i.e., are
            never mentioned in Job Postings or Applicants' profiles), then
            we can drop them here.  This should not happen, so this function
            should not do anything, but I'll leave it in just in case I 
            ever want to consider cases like that.
        '''
        self.data['Sum'] = (self.data['Job_Posting_Count'] + self.data['Applicant_Count'])
        self.data = self.data[(self.data['Sum'] > 0)]

    def normaliseData(self):
        '''
            Calculate z-scores for each value and record in columns
            named 'x' and 'y'.  The use of z-score standardization or
            mean normalization is debateable.  I chose mean normalization
            because it retains the scale of the data.  For example, if 
            we have two points and their distances from the 0,0 origin
            point are (1,0) and (3,0), then the second point is mentioned
            three times more often than the first point in Job Postings.
            I'll include (and comment out) the lines for z-score 
            standardization in case you want to use them.
        '''
        # Z-score standardization
        #self.data['x'] = (self.data['Job_Posting_Count'] - self.job_postings_mean) / self.job_postings_std 
        #self.data['y'] = (self.data['Applicant_Count'] - self.applicants_mean)  / self.applicants_std
        
        # Mean normalization
        self.data['x'] = (self.data['Job_Posting_Count'] - self.job_postings_mean) / (self.job_postings_max - self.job_postings_min) 
        self.data['y'] = (self.data['Applicant_Count'] - self.applicants_mean)  / (self.applicants_max - self.applicants_min) 

    def plotAll(self):
        '''
            Plot all the Skills as data points in a 2D scatter plot.
            Also, save the dataset into a file.
        '''
        self.data.to_csv(CONFIG['all_skills_dataset_export_file'])
        fig = plt.figure(figsize=(8, 8))
        plt.scatter(self.data['x'], self.data['y'])
        plt.title("All Skills")
        plt.xlabel("Job Posting Skills")
        plt.ylabel("Applicant Skills")
        plt.grid(visible=True, color="blue", alpha=.1)

        # Add labels for each point
        x = self.data['x'].to_list()
        y = self.data['y'].to_list()
        labels = self.data['Skill'].to_list()

        # Add mean value lines for each axis
        plt.vlines(self.data['x'].mean(), -6, 6, linestyles ="solid", colors ="r")
        plt.hlines(self.data['y'].mean(), -6, 6, linestyles ="solid", colors ="r")
        plt.xlim(-6, 6)
        plt.ylim(-6, 6)
                
        texts = [plt.text(x[i], y[i], labels[i], fontsize=6) for i in range(len(x))]
        adjust_text(texts, 
            expand_points=(2, 2),
            arrowprops=dict(
                arrowstyle="-", 
                color='#a2a2c2', 
                lw=1
            ),
            ax=fig.axes[0]
        )

        #plt.show()
        plt.savefig(CONFIG['all_skills_scatterplot_export_file'])

    def plotLowerRightQuandrant(self):
        '''
            Plot the Skills which score below average as data points in 
            a 2D scatter plot.  Also, save the dataset into a file.
        '''
        fig = plt.figure(figsize=(8, 8))
        High_Emp_Low_App = self.data[(self.data['x'] >= self.data['x'].mean()) & (self.data['y'] <= self.data['y'].mean())]
        High_Emp_Low_App.to_csv(CONFIG['skills_gap_dataset_export_file'])
        plt.scatter(High_Emp_Low_App['x'], High_Emp_Low_App['y'])
        plt.title("The Skills Gap Quadrant")
        plt.xlabel("Job Posting Skills")
        plt.ylabel("Applicant Skills")
        plt.grid(visible=True, color="blue", alpha=.1)

        # Add mean value lines for each axis
        plt.vlines(0, -1, 0.5, linestyles ="solid", colors ="r")
        plt.hlines(0, -0.5, 3, linestyles ="solid", colors ="r")
        plt.xlim(-0.5, 3)
        plt.ylim(-1, 0.5)

        # Add labels for each point
        x = High_Emp_Low_App['x'].to_list()
        y = High_Emp_Low_App['y'].to_list()
        labels = High_Emp_Low_App['Skill'].to_list()
                
        texts = [plt.text(x[i], y[i], labels[i], fontsize=6) for i in range(len(x))]
        adjust_text(texts, 
            expand_points=(2, 2),
            arrowprops=dict(
                arrowstyle="-", 
                color='#2121c1', 
                lw=1
            ),
            ax=fig.axes[0]
        )
        #plt.show()
        plt.savefig(CONFIG['skills_gap_scatterplot_export_file'])

    def plotAboveAverageJobPostingSkills(self):   
        '''
            Select the Skills which score above average on the x-axis
            (meaning they more often than average they are mentioned 
            in Job Postings).  Then, sort them in descending order
            and plot them in a column chart.  Also, save the dataset 
            into a file.
        ''' 
        fig = plt.figure(figsize=(8, 8))
        High_Emp = self.data[(self.data['x'] >= self.data['x'].mean())]
        High_Emp = High_Emp.sort_values(by='x', ascending=False)
        High_Emp.to_csv(CONFIG['all_skills_ranked_dataset_export_file'])
        values = High_Emp['x'].to_list()
        labels = High_Emp['Skill'].to_list()
        plt.xticks(rotation=45, ha='right', fontsize=6)
        plt.bar(labels, values, color ='blue', width = 0.4) 
        plt.xlabel("Skills")
        plt.ylabel("Normalized Frequency")
        plt.title("Skills listed more often than average by employers")
        #plt.show()
        plt.savefig(CONFIG['all_skills_ranked__barchart_export_file'])

    def plotSkillsGapSkillsImportance(self): 
        '''
            Select the Skills Gap skills.  Then, sort them in descending 
            order (by x-axis score) and plot them in a column chart.  
            Also, save the dataset into a file.
        '''    
        fig = plt.figure(figsize=(8, 8))
        High_Emp_Low_App = self.data[(self.data['x'] >= self.data['x'].mean()) & (self.data['y'] <= self.data['y'].mean())]
        High_Emp_Low_App = High_Emp_Low_App.sort_values(by='x', ascending=False)
        High_Emp_Low_App.to_csv(CONFIG['skills_gap_ranked_dataset_export_file'])
        values = High_Emp_Low_App['x'].to_list()
        labels = High_Emp_Low_App['Skill'].to_list()
        plt.xticks(rotation=45, ha='right', fontsize=6)
        plt.bar(labels, values, color ='blue', width = 0.4) 
        plt.xlabel("Skills")
        plt.ylabel("Normalized Frequency")
        plt.title("Skills Gap Skills in order of Importance")
        #plt.show()
        plt.savefig(CONFIG['skills_gap_ranked_barchart_export_file'])

    def run(self):
        '''
            Run each of the functions in this class in the correct 
            order.  This could go in (or be called from) the __init__ 
            method, but leaving it separate makes for easier testing
            of each individual method.
        '''
        self.setDescriptiveStatistics()
        self.dropZeroedData()
        self.normaliseData()

        
            