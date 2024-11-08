import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# 从CSV文件中加载数据
df = pd.read_csv(r'C:\Users\25106\Desktop\countries.csv')

# 计算 I/E 比例
df['I_distribution'] = df[['INFP-T', 'INTP-T', 'INFJ-T', 'ISFP-T', 'INTJ-T', 'ISFJ-T', 'ISTJ-T', 'ISTP-T',
                           'INFP-A', 'INTP-A', 'INFJ-A', 'ISFP-A', 'ISFJ-A', 'ISTJ-A', 'INTJ-A', 'ISTP-A']].sum(axis=1)
df['E_distribution'] = df[['ENFP-T', 'ENTP-T', 'ENFJ-T', 'ESFP-T', 'ENTJ-T', 'ESFJ-T', 'ESTJ-T',
                           'ESTP-T', 'ENFP-A', 'ENTP-A', 'ENFJ-A', 'ESFP-A', 'ESFJ-A', 'ESTJ-A',
                           'ENTJ-A', 'ESTP-A']].sum(axis=1)
df['IE_ratio'] = df['I_distribution'] / (df['I_distribution'] + df['E_distribution'])

# 移除 IE_ratio 或 Country 名称缺失的行
df = df.dropna(subset=['IE_ratio', 'Country'])
df = df[df['IE_ratio'].notna() & (df['IE_ratio'] > 0)]


# 假设CSV文件包含国家名称和各个MBTI类型的百分比，这里需要预处理数据
def prepare_mbti_data(row):
    mbti_columns = ['ESTJ', 'ESFJ', 'INFP', 'ENFP', 'INTJ', 'ISFJ', 'ENFJ', 'ESTP',
                    'ISTJ', 'INTP', 'INFJ', 'ISFP', 'ENTJ', 'ESFP', 'ENTP', 'ISTP']

    mbti_data = []
    for mbti in mbti_columns:
        a_percent = row.get(f'{mbti}-A', 0)
        t_percent = row.get(f'{mbti}-T', 0)
        total_percent = a_percent + t_percent
        if total_percent > 0:  # 只保留总百分比大于0的MBTI类型
            mbti_data.append((mbti, total_percent))

    return mbti_data


# 应用上述函数到DataFrame的每一行，生成新的'MBTI_Data'列
df['MBTI_Data'] = df.apply(prepare_mbti_data, axis=1)

# 定义颜色调色板
color_discrete_map = {
    'ENFP': '#8CD0C3', 'ESFP': '#FAF5B5', 'INTP': '#BCB9D8', 'INFP': '#F18072',
    'ENFJ': '#80B1D2', 'ENTP': '#F9B063', 'ESTP': '#B3D46B', 'ISTP': '#F7CBDF',
    'INTJ': '#D7D7D5', 'INFJ': '#BA7FB5', 'ISFP': '#1D78B5', 'ENTJ': '#32A02C',
    'ESFJ': '#FEDFB8', 'ISFJ': '#C24A7A', 'ISTJ': '#748EBB', 'ESTJ': '#83c297'
}

# Dash应用设置
app = dash.Dash(__name__)

# 创建动态地图，显示 I/E 比例分布
choropleth_fig = px.choropleth(
    df,
    locations="Country",
    locationmode='country names',
    color="IE_ratio",
    color_continuous_scale='RdBu',
    labels={'IE_ratio': 'I/E Ratio'},
    title='Dynamic I/E Ratio Distribution by Country'
)
choropleth_fig.update_layout(
    title={
        'text': 'Dynamic I/E Ratio Distribution by Country',
        'x': 0.5,  # Center the title
        'xanchor': 'center'
    }
)
# 应用布局
app.layout = html.Div([
    dcc.Graph(id='choropleth-map', figure=choropleth_fig),
    dcc.Graph(id='pie-chart', figure={})  # 初始时饼图为空
])


# 定义回调函数，当choropleth地图被点击时更新饼图
@app.callback(
    Output('pie-chart', 'figure'),
    [Input('choropleth-map', 'clickData')]
)
def update_pie_chart(clickData):
    if clickData is None:
        return {}

    # 使用clickData中的location来获取被点击的国家名称
    country = clickData['points'][0]['location']
    # 查询DataFrame以获取该国家的MBTI数据
    country_data = df[df['Country'] == country].iloc[0]['MBTI_Data']

    # 解包MBTI数据和百分比
    labels, values = zip(*country_data)

    return {
        'data': [
            go.Pie(labels=labels, values=values,
                   marker=dict(colors=[color_discrete_map[label] for label in labels]))  # 使用定义的颜色调色板
        ],
        'layout': go.Layout(title=f'MBTItype Distribution - {country}')
    }


# 运行Dash应用
if __name__ == '__main__':
    app.run_server(debug=True)
