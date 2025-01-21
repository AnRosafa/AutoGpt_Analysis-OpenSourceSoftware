import requests
import pandas as pd

def fetch_github_releases(repo_owner, repo_name):
    """
    获取 GitHub 仓库的 Release 信息
    :param repo_owner: 仓库的所有者
    :param repo_name: 仓库名称
    :return: Release 数据的列表
    """
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases"
    
    # 发送请求并获取返回的 JSON 数据
    response = requests.get(url)
    
    if response.status_code == 200:
        releases = response.json()
        return releases
    else:
        print(f"请求失败，状态码：{response.status_code}")
        return []

def save_releases_to_csv(releases, filename):
    """
    将 Release 数据保存为 CSV 文件
    :param releases: Release 数据的列表
    :param filename: CSV 文件名
    """
    # 解析需要的字段：发布版本、发布日期、发布说明、资产链接等
    release_data = []
    for release in releases:
        release_info = {
            "tag_name": release.get("tag_name"),
            "name": release.get("name"),
            "published_at": release.get("published_at"),
            "body": release.get("body"),  # 发布说明
            "assets_count": len(release.get("assets", []))  # 关联的资源数量
        }
        release_data.append(release_info)
    
    # 使用 pandas 将数据保存为 CSV 文件
    df = pd.DataFrame(release_data)
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"Release 数据已保存到 {filename}")

def main():
    # GitHub 仓库信息
    repo_owner = "Significant-Gravitas"  # 仓库所有者
    repo_name = "AutoGPT"  # 仓库名称
    
    # 获取 releases 数据
    releases = fetch_github_releases(repo_owner, repo_name)
    
    if releases:
        # 保存数据到 CSV 文件
        save_releases_to_csv(releases, "AutoGPT_releases.csv")

if __name__ == "__main__":
    main()
