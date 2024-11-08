import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 加载数据
data = pd.read_csv(r'C:\Users\25106\Desktop\countries.csv')

# 更新 MBTI 列名
mbti_columns = ['ESTJ-A', 'ESFJ-A', 'INFP-T', 'ENFP-T', 'INTJ-T',
                'ESTJ-T', 'ESFJ-T', 'ENFP-A', 'ISFJ-T', 'ENFJ-A',
                'ESTP-A', 'ISTJ-A', 'INTP-T', 'INFJ-T', 'ISFP-T',
                'ENTJ-A', 'ESTP-T', 'ISTJ-T', 'ESFP-T', 'ENTP-A',
                'ESFP-A', 'INTJ-T', 'ISFJ-A', 'INTP-A', 'ENTP-T',
                'ISTP-T', 'ENTJ-T', 'ISTP-A', 'INFP-A', 'ENFJ-T',
                'INTJ-A', 'ISFP-A', 'INFJ-A']

# 大洲映射字典
continent_mapping = {
    'United States': 'North America',
    'Canada': 'North America',
    'Brazil': 'South America',
    'Argentina': 'South America',
    'United Kingdom': 'Europe',
    'Germany': 'Europe',
    'China': 'Asia',
    'India': 'Asia',
    'Australia': 'Australia',
    'South Africa': 'Africa',
    # 添加其他国家和对应的大洲
}

# 添加大洲信息
data['Continent'] = data['Country'].map(continent_mapping)

# 合并 -A 和 -T MBTI 类型
combined_mbti_columns = ['ESTJ', 'ESFJ', 'INFP', 'ENFP', 
                         'INTJ', 'ISFJ', 'ENFJ', 
                         'ESTP',  'ISTJ','INTP','INFJ','ISFP','ENTJ','ESFP','ENTP','ISTP']

for mbti in combined_mbti_columns:
    data[mbti] = data[mbti + '-A'] + data[mbti + '-T']

# 准备热图数据
continent_data = data.groupby('Continent')[combined_mbti_columns].sum()

# 绘制热图
plt.figure(figsize=(20, 15))
sns.heatmap(continent_data.T, cmap="YlGnBu", cbar=True)

plt.title('MBTI Type Distribution Heatmap by Continent')
plt.xlabel('Continent')
plt.ylabel('MBTI Types')
plt.savefig('mbti_heatmap_by_continent.png')
plt.show()
