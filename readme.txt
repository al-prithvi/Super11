# Project title: Super 11
## Team members: Guneet (gkhosla3), Pranit (pkaul9), Karthik (kanil3), Prithvi (psuresh38)
## Graduate team
         
### Files in the code directory
-   codebase (contains all the code)
    - aggregate_stats.py 
    - eda.py 
    - player_stats_for_match.py
    - CSVs: results after running above scripts 

-   data (2 csv files)
    - deliveries.csv
    - matches.csv

# Code and Instructions to run

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

















