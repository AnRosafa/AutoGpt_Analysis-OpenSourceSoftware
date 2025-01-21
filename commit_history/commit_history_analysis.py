import os
import pandas as pd
import matplotlib.pyplot as plt
import re

def load_commit_history(file_path):
    # 加载提交历史数据
    print("正在加载提交记录")
    try:
        df = pd.read_csv(file_path, names=["hash", "author", "date", "message"], sep="##", on_bad_lines='skip')
        print("数据加载成功！")
        return df
    except Exception as e:
        print(f"加载文件时发生错误：{e}")
        return None

def author_analysis(df):
    """
    按作者统计提交次数，过滤提交次数少于30次的作者，并将其合并为 'Others'
    """
    print("\n统计每个作者的提交次数...")
    commit_counts = df['author'].value_counts()
    
    # 将提交次数小于30次的作者合并为 'Others'
    commit_counts_others = commit_counts[commit_counts >= 30]
    others_count = commit_counts[commit_counts < 30].sum()
    
    if others_count > 0:
        commit_counts_others['Others'] = others_count
    
    print(commit_counts_others)
    
    # 绘制提交作者的饼状图
    plt.figure(figsize=(8, 8))
    commit_counts_others.plot.pie(autopct='%1.1f%%', startangle=90, cmap='Set3')
    plt.title("Commit Counts by Author")
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig("commit_by_author_pie.png")  # 保存饼状图
    plt.show()

    # 绘制提交作者的柱状图
    plt.figure(figsize=(10, 6))
    commit_counts_others.plot(kind='bar', color='skyblue')
    plt.title("Commit Counts by Author (Bar Chart)")
    plt.xlabel("Author")
    plt.ylabel("Number of Commits")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("commit_by_author_bar.png")  # 保存柱状图
    plt.show()

    return commit_counts

def commit_date_analysis(df):
    # 按日期统计提交数量，并绘制折线图（按日）
    print("\n分析提交频率（按日期）...")

    # 将日期转换为标准 datetime 格式
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    daily_commits = df['date'].dt.date.value_counts().sort_index()

    print("提交频率（按日期）：")
    print(daily_commits)

    # 绘制按日提交频率的折线图
    plt.figure(figsize=(10, 6))
    daily_commits.plot(kind='line', marker='o', linestyle='-')
    plt.title("Commit Frequency Over Time (Daily)")
    plt.xlabel("Date")
    plt.ylabel("Number of Commits")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("commit_frequency.png")  # 保存图像
    plt.show()

def commit_month_analysis(df):
    # 按月统计提交数量，并绘制折线图（按月）
    print("\n分析提交频率（按月）...")

    # 将日期转换为月份
    df['month'] = df['date'].dt.to_period('M')
    monthly_commits = df['month'].value_counts().sort_index()

    print("提交频率（按月）：")
    print(monthly_commits)

    # 绘制按月提交频率的折线图
    plt.figure(figsize=(10, 6))
    monthly_commits.plot(kind='line', marker='o', linestyle='-')
    plt.title("Commit Frequency Over Time (Monthly)")
    plt.xlabel("Month")
    plt.ylabel("Number of Commits")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("commit_frequency_month.png")  # 保存图像
    plt.show()

def commit_type_classify(message):
    message = str(message).lower()  # 确保消息是小写的

    # 功能增加或改进
    if 'feature' in message or 'add' in message or 'new' in message or 'implement' in message or 'enhance' in message:
        return 'Feature'  # 功能/新特性
    # Bug 修复
    elif 'fix' in message or 'bug' in message or 'patch' in message or 'error' in message or 'hotfix' in message:
        return 'Bug Fix'  # Bug 修复
    # 性能优化或重构
    elif 'performance' in message or 'optimize' in message or 'refactor' in message or 'improve' in message:
        return 'Performance/Refactor'  # 性能优化或重构
    # 文档更新
    elif 'doc' in message or 'documentation' in message or 'readme' in message or 'update docs' in message or 'docs' in message:
        return 'Documentation'  # 文档更新
    # 测试
    elif 'test' in message or 'tests' in message or 'unittest' in message or 'integration' in message:
        return 'Test'  # 测试
    # 配置或环境更新
    elif 'config' in message or 'environment' in message or 'docker' in message or 'ci' in message or 'ci/cd' in message:
        return 'Configuration/Environment'  # 配置/环境
    # 安全更新
    elif 'security' in message or 'vulnerability' in message or 'exploit' in message or 'fix security' in message:
        return 'Security'  # 安全更新
    # 其他类型（无法明确分类的）
    else:
        return 'Other'

def commit_types_analysis(df):
    # 分析提交类型
    print("\n分析提交类型...")

    # 将每条提交的消息按规则分类
    df['type'] = df['message'].apply(commit_type_classify)

    # 统计每种类型的提交次数
    commit_types = df['type'].value_counts()

    print("提交类型分布：")
    print(commit_types)

    # 绘制提交类型的分布柱状图
    plt.figure(figsize=(10, 6))
    commit_types.plot(kind='bar', color='skyblue')
    plt.title("Commit Types Distribution")
    plt.xlabel("Commit Type")
    plt.ylabel("Number of Commits")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("commit_types.png")  # 保存图像
    plt.show()

    # 绘制提交类型的饼状图
    plt.figure(figsize=(8, 8))
    commit_types.plot.pie(autopct='%1.1f%%', startangle=90, cmap='Set2')
    plt.title("Commit Types Distribution (Pie Chart)")
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig("commit_types_pie.png")  # 保存饼状图
    plt.show()

    # 返回提交类型统计信息
    return commit_types


def commit_counts_over_time_by_top_authors(df):
    """
    绘制提交量前十名作者的提交数随时间（月度）变化的折线图
    """
    print("\n分析提交量前十名作者的提交数随时间变化...")

    # 选取提交次数前10的作者
    top_authors = df['author'].value_counts().head(10).index

    # 创建一个DataFrame来存储每个作者每月的提交次数
    df['month'] = df['date'].dt.to_period('M')
    
    # 按月和作者统计提交次数
    monthly_commit_counts = df[df['author'].isin(top_authors)].groupby(['month', 'author']).size().unstack(fill_value=0)

    print("提交量前十名作者的提交数随时间变化：")
    print(monthly_commit_counts)

    # 绘制折线图
    plt.figure(figsize=(12, 8))
    for author in top_authors:
        monthly_commit_counts[author].plot(label=author)

    plt.title("Commit Counts by Top 10 Authors Over Time (Monthly)")
    plt.xlabel("Month")
    plt.ylabel("Number of Commits")
    plt.legend(title="Authors", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("top_10_authors_commit_over_time.png")  # 保存图像
    plt.show()

def save_results(commit_counts, commit_types):
    # 保存统计结果到文件
    print("\n保存分析结果到文件...")
    commit_counts.to_csv("commit_counts_by_author.csv", header=True)
    commit_types.to_csv("commit_types.csv", header=True)
    print("结果已保存到 'commit_counts_by_author.csv', 'commit_types.csv'")

def main():
    # 定义文件路径
    file_path = "commit_history/commit_history.csv"
    
    # 加载数据
    df = load_commit_history(file_path)
    if df is None:
        print("无法加载数据，程序退出。")
        return
    
    # 分析提交者统计
    commit_counts = author_analysis(df)
    
    # 提交频率分析（按日）
    commit_date_analysis(df)
    
    # 提交频率分析（按月）
    commit_month_analysis(df)
    
    # 提交类型分析
    commit_types = commit_types_analysis(df)
    
    #前十名提交者提交趋势
    commit_counts_over_time_by_top_authors(df)

    # 保存结果
    save_results(commit_counts, commit_types)

if __name__ == "__main__":
    main()
