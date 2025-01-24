import requests
import matplotlib.pyplot as plt
from datetime import datetime

# GitHub GraphQL API 配置
TOKEN = "token"  
HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}
GRAPHQL_URL = "https://api.github.com/graphql"

def fetch_stars_graphql(repo_owner, repo_name):
    """
    使用 GitHub GraphQL API 获取仓库的 stars 数据
    """
    query = """
    query($owner: String!, $name: String!, $cursor: String) {
      repository(owner: $owner, name: $name) {
        stargazers(first: 100, after: $cursor) {
          edges {
            starredAt
          }
          pageInfo {
            endCursor
            hasNextPage
          }
        }
      }
    }
    """
    variables = {"owner": repo_owner, "name": repo_name, "cursor": None}
    stars_data = []
    print("开始获取 stars 数据...")
    
    while True:
        response = requests.post(
            GRAPHQL_URL, 
            headers=HEADERS, 
            json={"query": query, "variables": variables}
        )
        if response.status_code != 200:
            print(f"错误：无法获取数据（状态码: {response.status_code}）")
            break

        data = response.json()
        stargazers = data["data"]["repository"]["stargazers"]
        for edge in stargazers["edges"]:
            starred_at = edge["starredAt"]
            stars_data.append(datetime.strptime(starred_at, "%Y-%m-%dT%H:%M:%SZ"))

        # 输出日志
        print(f"已获取 {len(stars_data)} 条 stars 数据...")
        
        # 判断是否还有下一页
        page_info = stargazers["pageInfo"]
        if page_info["hasNextPage"]:
            variables["cursor"] = page_info["endCursor"]
        else:
            break

    print(f"完成 stars 数据获取，共计获取 {len(stars_data)} 条数据。")
    return stars_data

def plot_stars_trend_daily(stars_data, output_file="stars_trend_daily.png"):
    """
    按日绘制 stars 随时间变化的折线图
    """
    print("开始绘制按日的 stars 趋势图...")
    stars_data.sort()
    daily_counts = {}
    for star_time in stars_data:
        day = star_time.strftime("%Y-%m-%d")
        daily_counts[day] = daily_counts.get(day, 0) + 1

    days = sorted(daily_counts.keys())
    cumulative_stars = [sum([daily_counts[d] for d in days[:i+1]]) for i in range(len(days))]

    plt.figure(figsize=(16, 8))
    plt.plot(days, cumulative_stars, marker="o", color="blue", linewidth=1)
    plt.title("Stars Growth Over Time (Daily)", fontsize=16)
    plt.xlabel("Time (Day)", fontsize=12)
    plt.ylabel("Cumulative Stars", fontsize=12)
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(alpha=0.5)
    plt.tight_layout()
    plt.savefig(output_file)
    print(f"趋势图已保存到 {output_file} 文件中。")
    plt.show()

def main():
    # 配置目标仓库
    REPO_OWNER = "Significant-Gravitas"
    REPO_NAME = "AutoGPT"

    # 获取 stars 数据
    stars_data = fetch_stars_graphql(REPO_OWNER, REPO_NAME)

    # 绘制按日统计的 stars 趋势图
    if stars_data:
        plot_stars_trend_daily(stars_data)
    else:
        print("没有获取到任何 stars 数据，无法绘制趋势图。")

if __name__ == "__main__":
    main()
