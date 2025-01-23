import pandas as pd
import matplotlib.pyplot as plt

# 读取CSV文件
data = pd.read_csv("issues_and_stars/AutoGPT_issues.csv")

# 确保时间列是时间格式
data['created_at'] = pd.to_datetime(data['created_at'])

# 饼状图：展现已回复和未回复issue的比例
def plot_pie_chart(data):
    replied_counts = data['is_replied'].value_counts()
    labels = ['Replied', 'Not Replied']
    plt.figure(figsize=(6, 6))
    plt.pie(replied_counts, labels=labels, autopct='%1.1f%%', startangle=90, colors=['skyblue', 'orange'])
    plt.title('Proportion of Replied vs Not Replied Issues')
    plt.savefig('pie_chart_replied_issues.png')  # 保存图片
    plt.close()

# 条形图：展示各时间段的issue数量
def plot_bar_chart(data):
    # 将未回复的 issue 的 response_time_hours 设置为 -1，便于分组
    data['response_time_hours'] = data['response_time_hours'].fillna(-1)

    # 定义时间段和标签
    bins = [-2, 0, 1, 10, 50, 200, 1000, float('inf')]
    labels = ['Unreplied', '<1h', '1-10h', '10-50h', '50-200h', '200-1000h', '>1000h']

    # 将 response_time_hours 分为对应区间
    data['response_time_category'] = pd.cut(data['response_time_hours'], bins=bins, labels=labels, right=False)
    
    # 统计每个时间段的数量
    category_counts = data['response_time_category'].value_counts(sort=False)

    # 绘制条形图
    plt.figure(figsize=(10, 6))
    plt.bar(labels, category_counts, color='lightgreen')
    plt.xlabel('Response Time Categories')
    plt.ylabel('Number of Issues')
    plt.title('Issues Distribution by Response Time')
    plt.xticks(rotation=45)
    plt.savefig('bar_chart_response_time.png')  # 保存图片
    plt.close()

# 折线图：展示issue提交随时间变化的趋势
def plot_line_chart(data):
    monthly_data = data['created_at'].dt.to_period('M').value_counts().sort_index()
    plt.figure(figsize=(12, 6))
    plt.plot(monthly_data.index.astype(str), monthly_data.values, marker='o', linestyle='-', color='purple')
    plt.xlabel('Month')
    plt.ylabel('Number of Issues')
    plt.title('Trend of Issues Over Time')
    plt.xticks(rotation=45)
    plt.grid(alpha=0.3)
    plt.savefig('line_chart_issues_trend.png')  # 保存图片
    plt.close()

# 调用函数生成图表
plot_pie_chart(data)
plot_bar_chart(data)
plot_line_chart(data)

print("图表已保存为：'pie_chart_replied_issues.png', 'bar_chart_response_time.png', 'line_chart_issues_trend.png'")

