import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def load_data(commit_file, release_file):
    """
    加载提交历史和 release 数据
    :param commit_file: 提交历史 CSV 文件路径
    :param release_file: release CSV 文件路径
    :return: 提交历史 DataFrame, release DataFrame
    """
    # 加载 commit_history 数据
    commit_data = pd.read_csv(commit_file, sep="##", header=None, engine='python', encoding='latin1')
    commit_data.columns = ['ID', 'author','date', 'message']
    commit_data['date'] = pd.to_datetime(commit_data['date'], errors='coerce')
    
    # 加载 release 数据
    release_data = pd.read_csv(release_file, encoding='latin1')
    release_data['published_at'] = pd.to_datetime(release_data['published_at'], errors='coerce')

    # 去除时间部分，仅保留日期
    release_data['published_at'] = release_data['published_at'].dt.date

    return commit_data, release_data

def classify_commit_types(commit_data):
    """
    根据提交信息的类型分类提交
    :param commit_data: 提交历史数据
    :return: 分类后的提交数据
    """
    # 定义提交类型映射
    commit_data['commit_type'] = commit_data['message'].apply(lambda x: classify_commit_type(x))
    
    return commit_data

def classify_commit_type(message):
    """
    根据提交信息中的内容分类提交
    :param message: 提交的消息
    :return: 提交类型
    """
    if pd.isna(message):
        return 'Others'
    
    message = message.lower()
    if 'bug fix' in message:
        return 'Bug Fix'
    elif 'feature' in message:
        return 'Feature'
    elif 'documentation' in message:
        return 'Documentation'
    elif 'configuration' in message or 'environment' in message:
        return 'Configuration/Environment'
    elif 'performance' in message or 'refactor' in message:
        return 'Performance/Refactor'
    elif 'test' in message:
        return 'Test'
    elif 'security' in message:
        return 'Security'
    else:
        return 'Others'

def plot_commit_types_with_releases(commit_data, release_data):
    """
    绘制每种提交类型随时间变化的折线图，并在版本发布点上添加竖直虚线
    :param commit_data: 提交历史数据
    :param release_data: release 数据
    """
    plt.figure(figsize=(45, 6)) 
    # 按日统计每种提交类型的数量
    daily_commit_types = commit_data.groupby([commit_data['date'], 'commit_type']).size().unstack(fill_value=0)
    
    # 为每种提交类型绘制一条折线
    daily_commit_types.plot(kind='line', lw=2, colormap='tab10')
    
    # 在每个版本发布的日期上添加竖直虚线
    for release in release_data.itertuples():
        release_date = release.published_at
        # 在发布版本的时间点添加竖直虚线
        plt.axvline(x=release_date, color='red', linestyle='--', lw=2)
        # 在虚线旁边标注版本号
        plt.text(release_date, daily_commit_types.max().max() * 0.05, release.tag_name, color='red', rotation=90)

    # 设置图表的标题和标签
    plt.title("Commit Types Over Time with Release Versions")
    plt.xlabel("Date")
    plt.ylabel("Number of Commits")
    
    # 格式化X轴为日期，并设置适当的日期显示间隔
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_minor_locator(mdates.WeekdayLocator())
    plt.xticks(rotation=45)
    
    # 自动调整布局
    plt.tight_layout()
    
    # 显示图表
    plt.legend(title="Commit Types")
    
    # 保存图形并显示
    plt.savefig("commit_types_over_time_with_releases.png")  # 保存为图片
    plt.show()

def main():
    # 文件路径
    commit_file = "release_analysis/commit_history.csv"  # 提交历史 CSV 文件路径
    release_file = "release_analysis/AutoGPT_releases.csv"  # release CSV 文件路径

    # 加载数据
    commit_data, release_data = load_data(commit_file, release_file)

    # 分类提交类型
    commit_data = classify_commit_types(commit_data)

    # 绘制提交类型随时间变化的折线图并标注版本发布
    plot_commit_types_with_releases(commit_data, release_data)

if __name__ == "__main__":
    main()

