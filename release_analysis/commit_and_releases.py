import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def load_data(commit_file, release_file):
    """
    加载提交历史和release数据
    :param commit_file: 提交历史 CSV 文件路径
    :param release_file: release CSV 文件路径
    :return: 提交历史 DataFrame, release DataFrame
    """
    # 加载 commit_history 数据
    commit_data = pd.read_csv(commit_file,sep="##",)
    commit_data['date'] = pd.to_datetime(commit_data['date'], errors='coerce')
    
    # 加载 release 数据
    release_data = pd.read_csv(release_file)
    release_data['published_at'] = pd.to_datetime(release_data['published_at'], errors='coerce')

    return commit_data, release_data

def plot_commit_and_releases(commit_data, release_data):
    """
    绘制按月提交数量的条形图，并在版本发布点上添加竖直虚线
    :param commit_data: 提交历史数据
    :param release_data: release 数据
    """
    # 按月统计提交数量
    commit_data['month'] = commit_data['date'].dt.to_period('M')
    monthly_commits = commit_data.groupby('month').size()

    # 绘制条形图
    plt.figure(figsize=(10, 6))
    monthly_commits.plot(kind='bar', color='skyblue', width=0.8, label="Commits")
    
    # 在每个月的对应位置上添加竖直虚线
    for release in release_data.itertuples():
        release_date = release.published_at
        if release_date in monthly_commits.index:
            # 在发布版本的时间点添加竖直虚线
            plt.axvline(x=monthly_commits.index.get_loc(release_date.to_period('M')), color='red', linestyle='--', lw=2)
            # 在虚线旁边标注版本号
            plt.text(monthly_commits.index.get_loc(release_date.to_period('M')) + 0.1, 
                     max(monthly_commits) * 0.05, release.tag_name, color='red', rotation=90)

    # 设置图表的标题和标签
    plt.title("Monthly Commits with Release Versions")
    plt.xlabel("Time (Month)")
    plt.ylabel("Number of Commits")
    
    # 格式化X轴为年月
    plt.xticks(ticks=range(len(monthly_commits.index)), labels=[str(date) for date in monthly_commits.index], rotation=45)
    plt.tight_layout()
    
    # 显示图表
    plt.legend()
    plt.savefig("commits_with_releases.png")  # 保存为图片
    plt.show()

def main():
    # 文件路径
    commit_file = "release_analysis/commit_history.csv"  # 提交历史 CSV 文件路径
    release_file = "release_analysis/AutoGPT_releases.csv"  # release CSV 文件路径

    # 加载数据
    commit_data, release_data = load_data(commit_file, release_file)

    # 绘制提交条形图并标注版本发布
    plot_commit_and_releases(commit_data, release_data)

if __name__ == "__main__":
    main()
