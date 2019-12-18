# Project title: Super 11
## Team members: Guneet, Pranit, Karthik, Prithvi
## Graduate
<p align="center">
  <img src="https://storage.googleapis.com/kaggle-datasets-images/323/694/2dc6c609aa96286b209f346f0e75639b/dataset-cover.jpg"> 
</p>

# 1. Overview of the project and Motivation
Cricket is a sport that is played between two teams of eleven players comprising of batsmen, bowlers, and a wicketkeeper. A fantasy sport is a virtual game played online, where participants assemble their virtual teams of players of a professional sport. The number of fantasy sports users has grown steadily over the years and is still growing.  

Selecting a team of players that will perform well is not that complex, is it? (One can just pick any players that have the best performance to date! ) Well, the problem becomes complex when one has to pick a team within a finite budget. Also, a balanced team in Cricket has a good combination of batsmen, bowlers, fielders, and all-rounders adding to the complexity of selection of a team.  

#### Motivation 
The motivation behind this project is to help players all around the world (competing in fantasy league apps) by drafting a good team that can maximize their profits and earn them rewards on the platform. This will be in the form of smart suggestions for picking players or a complete team suggestion altogether. 
Our goal is to dynamically select 11 players to form a team on a Fantasy Cricket app for a given match. The platform that we have selected is called “Dream 11”. We will generate this team from the two playing teams squads looking back on past player performance. There is a cost associated while picking any player in Dream 11. So, we need to consider these costs as well as , and keep it under the budget based on specified constraints. While forming such a team, we will take into consideration various constraints imposed by platforms hosting fantasy cricket contests. 


# 2. Dataset
- from Kaggle: https://www.kaggle.com/manasgarg/ipl


# 3. Code and Instructions to run

##### Visualization (for exploratory data analysis)
We've provided:
- eda.py: 
    - running this will generate all the graphs as PNG images in the directory 'eda_plots' found at the same level as the eda.py
    - these plots document all the initial visualizations we've used for analysis
- Jupyter Notebook EDA.ipynb  (SAME CODE AS eda.py)
    - is the Jupyter notebook equivalent of the above notebook in case you want to visualize all graphs seperately with their corresponding code



##### Player statistics (the output '.csv' files of these two scripts act as input for optimizer)
- aggregate_stats.py: 
    - generates player stats for all players by analysing their performance from 2008 to 2016
    - output: generating player_stats.csv in 'CSVs' directory

- player_stats_for_match.py: 
    - generates player stats for all the matches between the 4 teams [SRH (Hyderabad), RCB (Bangalore), MI (Mumbai), KKR (Kolkata)] in 2017.
    - output: generates 12 .csv files in the 'CSVs' directory (match_x_stats.csv where x is the match_id) 


##### Optimizer Code 
###### How to run:
- The 'Super_11.ipynb' notebook contains the optimizer code
- 'Super_11.ipynb' this notebook requires the 'cvxpy' module. This and other modules are already installed on Google Collab, therefore we will use Google Colab to execute the code in this file for generating the output.

###### Running the optimizer code (On Google Colab)

1. Visit the link "https://colab.research.google.com/notebooks/welcome.ipynb#recent=true" and click on the upload tab.

2. Click on choose file and select 'Super_11.ipynb' notebook. This will open up the notebook provided by us.

3. Next you have to upload CSVs.zip and Helper_Files.zip to Google Colab. CSVs.zip contains data about player statistics
   , each player's cost, and match details as well. Helper_Files.zip contain utility python files used by the 
   Super_11.ipynb notebook.

4. Next, click on Runtime -> Run all. It will run both the cells in Super_11.ipynb. The first cell unzips CSVs.zip and
   Helper_Files.zip. The second cell computes and outputs the Predicted Team, Optimal Team and various charts for the 
   selected match.

5. To run the code for a different match, simply click on the the drop down list, select one of the 12 matches and run 
   only the second cell. (Running the first cell again will generate prompts for replacing the already existing files,
   which is unnecessary effort.) 

6. All the results are charts are outputted in the Google Colab console. You can analyse our results.
	chart 1: Points earned by the predicted players based on their performance in selected match.
	chart 2: Comparision between the total points of predicted team and optimal team

Note 1: We are already providing you the CSVs.zip folder. This is the same folder in which all the CSVs are generated after
you run player_stats_for_match.py file.

Note 2: In case you want to reset the entire enviroment to re-analyse the project, click Runtime -> Reset all runtimes.
Now again follow the steps 1 - 6. 

















