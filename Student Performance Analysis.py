import pandas as pd
import missingno as msno
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
# Load the data
df = pd.read_csv('exams.csv')
# Display shape and info of the dataframe
print(df.shape)
df.info()
# Display the first few rows of the dataframe
print(df.head())
# Display column names
print(df.columns)
# Visualize missing data
msno.matrix(df)
plt.show()
# Check for missing values
print(df.isna().sum())
# Convert relevant columns to numeric (if not already numeric)
numeric_columns = ['math score', 'reading score', 'writing score']
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')
# Check for any non-numeric values that were coerced to NaN
print(df[numeric_columns].isna().sum())
# Drop rows with NaN values in numeric columns
df.dropna(subset=numeric_columns, inplace=True)
# Recheck for missing values
print(df.isna().sum())
# Set pass mark
passmark = 35
# Calculate percentage
df['Percentage'] = (df['math score'] + df['reading score'] + df['writing score']) / 3
# Define grading function
def Grade(Percentage):
    if Percentage >= 95:
        return 'O'
    elif Percentage >= 81:
        return 'A'
    elif Percentage >= 71:
        return 'B'
    elif Percentage >= 61:
        return 'C'
    elif Percentage >= 51:
        return 'D'
    elif Percentage >= 41:
        return 'E'
    else:
        return 'F'
# Apply grading function
df["grade"] = df.apply(lambda x: Grade(x["Percentage"]), axis=1)
# Display the first 10 rows
print(df.head(10))
# Describe the dataframe
print(df.describe())
# Gender distribution pie chart
sns.set(style='whitegrid')
plt.figure(figsize=(14, 7))
labels = df['gender'].value_counts().index
plt.pie(df['gender'].value_counts(), labels=labels, explode=[0.1, 0.1],
        autopct='%1.2f%%', colors=['#E37383', '#FFC0CB'], startangle=90)
plt.title('Gender')
plt.axis('equal')
plt.show()
# Gender vs Grades count plot
plt.figure(figsize=(10, 5))
sns.set_context("talk", font_scale=1)
sns.set_palette("pastel")
ax = sns.countplot(y="grade", hue="gender", data=df, order=["O", "A", "B", "C", "D", "E", "F"])
ax.bar_label(ax.containers[0])
ax.bar_label(ax.containers[1])
ax.legend(loc='upper right', frameon=True)
plt.title('Gender vs Grades', fontsize=18, fontweight='bold')
ax.set(xlabel='COUNT', ylabel='GRADE')
plt.show()
sns.boxplot(data = df,x="math score")
plt.show()
sns.boxplot(data = df,x="reading score")
plt.show()
sns.boxplot(data = df,x="writing score")
plt.show()
# Correlation heatmap
plt.figure(figsize=(8, 8))
plt.title('Correlation Analysis', color='Red', fontsize=20, pad=40)
# Select only numeric columns for the correlation matrix
numeric_df = df.select_dtypes(include=[np.number])
corr = numeric_df.corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, linewidths=.5)
plt.xticks(rotation=60)
plt.yticks(rotation=60)
plt.show()
race = ['Group A', 'Group B ', 'Group C',  
        'Group D', 'Group E']  
data = [79, 198, 323, 257, 143]  
# Creating explode data 
explode = ( 0.1, 0,0.2, 0.1, 0)   
# Creating color parameters 
colors = (  "#ffd11a", "#b463cf", 
          "#DC143C", "#6699ff", "#ff66b3" ) 
# Wedge properties 
wp = { 'linewidth' : 1, 'edgecolor' : "#cccccc" }   
# Creating autocpt arguments 
def func(pct, allvalues): 
    absolute = int(pct / 100.*np.sum(allvalues)) 
    return "{:.1f}%\n({:d} )".format(pct, absolute)   
# Creating plot 
fig, ax = plt.subplots(figsize =(10, 7)) 
wedges, texts, autotexts = ax.pie(data,  
                                  autopct = lambda pct: func(pct, data), 
                                  explode = explode,  
                                  labels = race, 
                                  shadow = True, 
                                  colors = colors, 
                                  startangle = 90, 
                                  wedgeprops = wp, 
                                  textprops = dict(color ="#000000"))   
# Adding legend 
ax.legend(wedges, race, 
          title ="Race/Ethnicity", 
          loc ="center left", 
          bbox_to_anchor =(1.25, 0, 0, 1.25))  
plt.setp(autotexts, size = 8, weight ="bold") 
ax.set_title("Race/Ethnicity Distribution", fontsize=15, fontweight='bold') 
# show plot 
plt.show()
ax=sns.countplot(data=df,x='race/ethnicity')
ax.bar_label(ax.containers[0])
plt.figure(figsize=(5,5))
labels=['Math Score', 'Reading Score', 'Writing Score']
colors=['#ff6666','orchid','#66b3ff']
explode=[0,0.1,0]
values=[df["math score"].mean(),df["reading score"].mean(),df["writing score"].mean()]
plt.pie(values,labels=labels,colors=colors,explode=explode,autopct='%1.1f%%',shadow=True,startangle=180,pctdistance=0.5)
plt.legend(['Math Score', 'Reading Score', 'Writing Score'],loc='lower right')
plt.axis('equal')
plt.title(' Overall Mean Score  ',fontsize=15, fontweight='bold')
plt.tight_layout()
plt.show()