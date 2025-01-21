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
    commit_data.columns = ['ID', 'author','date', 'commit_type']
    commit_data['date'] = pd.to_datetime(commit_data['date'], errors='coerce')
    
    # 加载 release 数据
    release_data = pd.read_csv(release_file, encoding='latin1')
    release_data['published_at'] = pd.to_datetime(release_data['published_at'], errors='coerce')

    # 去除时间部分，仅保留日期
    release_data['published_at'] = release_data['published_at'].dt.date

    return commit_data, release_data

def plot_commit_and_releases(commit_data, release_data):
    """
    绘制按日提交数量的折线图，并在版本发布点上添加竖直虚线
    :param commit_data: 提交历史数据
    :param release_data: release 数据
    """
    # 按日统计提交数量
    daily_commits = commit_data.groupby('date').size()

    # 绘制折线图
    plt.figure(figsize=(45, 6))  # 增加图像宽度
    daily_commits.plot(kind='line', color='skyblue', label="Commits", lw=2)
    
    # 在每个版本发布的日期上添加竖直虚线
    for release in release_data.itertuples():
        release_date = release.published_at
            # 在发布版本的时间点添加竖直虚线
        plt.axvline(x=release_date, color='red', linestyle='--', lw=2)
            # 在虚线旁边标注版本号
        plt.text(release_date, daily_commits.max() * 0.05, release.tag_name, color='red', rotation=90)

    # 设置图表的标题和标签
    plt.title("Daily Commits with Release Versions")
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
    plt.legend()
    plt.savefig("daily_commits_with_releases.png")  # 保存为图片
    plt.show()

def main():
    # 文件路径
    commit_file = "release_analysis/commit_history.csv"  # 提交历史 CSV 文件路径
    release_file = "release_analysis/AutoGPT_releases.csv"  # release CSV 文件路径

    # 加载数据
    commit_data, release_data = load_data(commit_file, release_file)

    # 绘制提交折线图并标注版本发布
    plot_commit_and_releases(commit_data, release_data)

if __name__ == "__main__":
    main()
