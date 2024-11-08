import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the CSV file
df = pd.read_csv(r'C:\Users\25106\Desktop\km.csv')

# Define job categories
it_jobs = ["IT Director", "IT Manager", "System Administrator", "System Architect", "Programmer",  "Head (engineering manufacturing)","Analyst", "Tester", "Operator (electrical appliances mechanisms)"]
hr_jobs = ["HR Manager", "HR Director", "Recruiter", "Training Manager", "Assistant Secretary","Foreman (manufacturing)"]
finance_jobs = ["CFO", "Financial Analyst", "Chief Accountant", "Accountant", "Head of Financial Department",  "Head of Commercial Department","Economist"]
marketing_jobs = ["Marketing Director",  "Head (trade mediation)","Brand Manager", "Marketing Research Specialist", "Shop Seller", "Sales Agent (real estate insurance)", "Sales Manager"]
design_jobs = ["Designer", "Advertising Manager", "Head (culture art)"]
management_jobs = ["General Director", "Regional Manager", "Head of Department",
                   "Head of the Organization",
                   "Head (medicine education)", "Head (power units security service)",
                   "Head (personnel public administration)"]

# Create a new column to store categories
def classify_job(title):
    if title in it_jobs:
        return 'Technical'
    elif title in hr_jobs:
        return 'HR'
    elif title in finance_jobs:
        return 'Finance'
    elif title in marketing_jobs:
        return 'Marketing'
    elif title in design_jobs:
        return 'Design'
    elif title in management_jobs:
        return 'Management'
    else:
        return 'Unrelated'

df['Category'] = df['jobtitle'].apply(classify_job)

# Remove unrelated jobs
df_filtered = df[df['Category'] != 'Unrelated']

# Define MBTI type classification
def classify_mbti(mbti):
    if mbti[1] == 'N' and mbti[2] == 'T':
        return 'NT'
    elif mbti[1] == 'S' and mbti[2] == 'T':
        return 'ST'
    elif mbti[1] == 'N' and mbti[2] == 'F':
        return 'NF'
    elif mbti[1] == 'S' and mbti[2] == 'F':
        return 'SF'

df_filtered['MBTI_Type'] = df_filtered['psychotype'].apply(classify_mbti)

# Generate pie charts and stacked bar chart for each MBTI type's job category distribution
mbti_groups = df_filtered.groupby('MBTI_Type')['Category'].value_counts().unstack().fillna(0)

# Set pastel color palette
colors = ['#E63946', '#F1FAEE', '#A8DADC', '#457B9D', '#F1C40F', '#F77F00']

# Plot pie charts
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

for i, mbti_type in enumerate(mbti_groups.index):
    axes[i].pie(mbti_groups.loc[mbti_type], labels=mbti_groups.columns, autopct='%1.1f%%', colors=colors)
    axes[i].set_title(f'Job Category Distribution for MBTI Type {mbti_type}')

plt.tight_layout()
plt.savefig('mbti_pie_charts.png')
plt.show()

# Plot stacked bar chart
mbti_groups.plot(kind='bar', stacked=True, color=colors, figsize=(14, 8))
plt.title('Job Category Distribution by MBTI Type')
plt.xlabel('MBTI Type')
plt.ylabel('Count')
plt.legend(title='Job Category')
plt.savefig('mbti_stacked_bar_chart.png')
plt.show()
