
# coding: utf-8

# > **Tip**: Welcome to the Investigate a Dataset project! You will find tips in quoted sections like this to help organize your approach to your investigation. Before submitting your project, it will be a good idea to go back through your report and remove these sections to make the presentation of your work as tidy as possible. First things first, you might want to double-click this Markdown cell and change the title so that it reflects your dataset and investigation.
# 
# # Project: TMDb movie data
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>
# 
# This data set contains information about 10,000 movies collected from The Movie Database (TMDb), including user ratings and revenue.
# 
# - Certain columns, like ‘cast’ and ‘genres’, contain multiple values separated by pipe `(|)` characters.
# - There are some odd characters in the ‘cast’ column. Don’t worry about cleaning them. You can leave them as is.
# - The final two columns ending with “_adj” show the budget and revenue of the associated movie in terms of 2010 dollars, accounting for inflation over time.

# <a id='intro'></a>
# ## Introduction
# 
# > **Tip**: In this section of the report, provide a brief introduction to the dataset you've selected for analysis. At the end of this section, describe the questions that you plan on exploring over the course of the report. Try to build your report around the analysis of at least one dependent variable and three independent variables.
# >
# > If you haven't yet selected and downloaded your data, make sure you do that first before coming back here. If you're not sure what questions to ask right now, then make sure you familiarize yourself with the variables and the dataset context for ideas of what to explore.
# 
# Which genres are most popular from year to year? What kinds of properties are associated with movies that have high revenues?

# In[3]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# > **Tip**: In this section of the report, you will load in the data, check for cleanliness, and then trim and clean your dataset for analysis. Make sure that you document your steps carefully and justify your cleaning decisions.
# 
# ### General Properties

# In[5]:


# Load the data
df = pd.read_csv('tmdb-movies.csv')
df.info()


# In[6]:


df.head(1)


# It seems that columns `homepage`, `tagline`, `overview` can be dropped.

# > **Tip**: You should _not_ perform too many operations in each cell. Create cells freely to explore your data. One option that you can take with this project is to do a lot of explorations in an initial notebook. These don't have to be organized, but make sure you use enough comments to understand the purpose of each code cell. Then, after you're done with your analysis, create a duplicate notebook where you will trim the excess and organize your steps so that you have a flowing, cohesive report.
# 
# > **Tip**: Make sure that you keep your reader informed on the steps that you are taking in your investigation. Follow every code cell, or every set of related code cells, with a markdown cell to describe to the reader what was found in the preceding cell(s). Try to make it so that the reader can then understand what they will be seeing in the following cell(s).
# 
# ### Data Cleaning
# #### Step 1: Drop columns
# Drop three columns: `homepage`, `tagline`, `overview`: 

# In[7]:


# Drop columns
df.drop(['homepage', 'tagline', 'keywords', 'overview'], axis=1, inplace=True)


# In[8]:


# confirm changes
df.head(1)


# #### Step 2: Check nulls

# In[9]:


# View missing counts for each feature in the data
df.isnull().sum()


# In[10]:


# Drop the column `imdb_id` since we already have id.
df.drop(['imdb_id'], axis=1, inplace=True)
df.isnull().sum()


# In[11]:


# Drop the rows where the column `genres` has null cells, since genres is a key metric that we need to explore.
df.dropna(subset=['genres'], inplace=True)
df.isnull().sum()


# In[12]:


# Drop the rows where the columns `cast`, `director`, and `production_companies` has null cells.
df.dropna(subset=['cast', 'director', 'production_companies'], inplace=True)
df.isnull().sum()


# In[13]:


df.shape # finally, the not null dataset has 9773 rows and 16 columns.


# #### Step 3: Check and drop the duplicated data.

# In[14]:


# check the duplicated row.
df.duplicated().sum()


# In[15]:


# drop the duplicated row.
df.drop_duplicates(inplace=True)


# In[16]:


# check the number of rows.
df.shape


# In[17]:


# save to a new csv file
df.to_csv('imbd_clean.csv')


# #### Step 4: Check the columns that contain `|` and count the frequency of the genres.

# In[18]:


# check which rows have |
df[df['genres'].str.contains('|')].sum()


# In[19]:


# count the genre frequency.
list1 = [] # list of genre for each movie
for i in df.genres:
    temp_genre = i.split('|')
    for j in temp_genre:
        list1.append(j)


# In[20]:


# import the package and count the frequency of each genre:
import collections
counter=collections.Counter(list1)
counter


# In[54]:


# import the wordcloud package and visualize the package.
from wordcloud import WordCloud

wordcloud = WordCloud(width=800, height=400)

wordcloud.generate_from_frequencies(frequencies=counter)
plt.figure(figsize=(20,10) )
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# > **Tip**: Now that you've trimmed and cleaned your data, you're ready to move on to exploration. Compute statistics and create visualizations with the goal of addressing the research questions that you posed in the Introduction section. It is recommended that you be systematic with your approach. Look at one variable at a time, and then follow it up by looking at relationships between variables.
# 
# ### Research Question 1: Which genres are most popular from year to year? 

# In[64]:


# Use this, and more code cells, to explore your data. Don't forget to add
#   Markdown cells to document your observations and findings.
df_clean = pd.read_csv('imbd_clean.csv')
df_clean.head(1)


# In[82]:


# count the genre frequency w.r.t each year.
list1 = {} # list of genre for each movie
for i in sorted(df_clean.release_year):
    list1[i] = {}


# In[ ]:


# assign the genres to each 'release_year' key.
for i in sorted(df_clean.release_year):
    for j in df_clean.genres:
        print(i)
        print(j.split('|'))
    
        


# ### Research Question 2: What kinds of properties are associated with movies that have high revenues?

# In[ ]:


# Continue to explore the data to address your additional research
#   questions. Add more headers as needed if you have more questions to
#   investigate.


# <a id='conclusions'></a>
# ## Conclusions
# 
# > **Tip**: Finally, summarize your findings and the results that have been performed. Make sure that you are clear with regards to the limitations of your exploration. If you haven't done any statistical tests, do not imply any statistical conclusions. And make sure you avoid implying causation from correlation!
# 
# > **Tip**: Once you are satisfied with your work, you should save a copy of the report in HTML or PDF form via the **File** > **Download as** submenu. Before exporting your report, check over it to make sure that the flow of the report is complete. You should probably remove all of the "Tip" quotes like this one so that the presentation is as tidy as possible. Congratulations!
