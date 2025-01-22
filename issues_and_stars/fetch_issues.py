import requests
import pandas as pd

# 设置 GitHub 个人访问令牌
ACCESS_TOKEN = "token"  # 替换为你的 GitHub 访问令牌

def fetch_github_issues(repo_owner, repo_name):
    """
    获取 GitHub 仓库的 Issue 信息
    """
    print("开始获取 Issues 数据...")
    issues = []
    page = 1
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues"
    headers = {
        "Authorization": f"token {ACCESS_TOKEN}"  # 添加授权头
    }
    
    while True:
        # 分页获取 Issues
        params = {"state": "all", "per_page": 100, "page": page}
        print(f"请求第 {page} 页数据...")
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            batch = response.json()
            if not batch:
                print("没有更多数据，获取完成。")
                break
            print(f"获取到 {len(batch)} 条 Issue 数据")
            issues.extend(batch)
            page += 1
        elif response.status_code == 403:
            print("API 速率限制已达到，等待后重试...")
            break
        else:
            print(f"请求失败，状态码：{response.status_code}, 响应：{response.text}")
            break
    
    print(f"共获取到 {len(issues)} 条 Issue 数据")
    return issues

def process_issues_data(issues):
    """
    解析 Issue 数据
    """
    print("开始解析 Issues 数据...")
    processed_data = []
    headers = {
        "Authorization": f"token {ACCESS_TOKEN}"  # 添加授权头
    }
    
    total_issues = len(issues)
    for idx, issue in enumerate(issues):
        # 每处理 100 条输出进度
        if idx % 100 == 0:
            print(f"正在解析第 {idx + 1}/{total_issues} 条 Issue 数据...")
        
        # 跳过 Pull Request，因为它们也是 Issue 的一种形式
        if "pull_request" in issue:
            continue
        
        created_at = pd.to_datetime(issue.get("created_at"))
        comments = issue.get("comments", 0)
        first_reply_time = None
        response_time = None
        
        # 如果有评论，获取第一条评论的时间
        if comments > 0:
            comments_url = issue.get("comments_url")
            comments_response = requests.get(comments_url, headers=headers)
            if comments_response.status_code == 200:
                comments_data = comments_response.json()
                if comments_data:
                    first_reply_time = pd.to_datetime(comments_data[0].get("created_at"))
                    response_time = (first_reply_time - created_at).total_seconds() / 3600  # 转换为小时
        
        # 记录 Issue 的关键信息
        processed_data.append({
            "issue_number": issue.get("number"),
            "created_at": created_at,
            "is_replied": comments > 0,
            "first_reply_time": first_reply_time,
            "response_time_hours": response_time
        })
    
    print(f"解析完成，共处理 {len(processed_data)} 条 Issue 数据")
    return processed_data


def save_issues_to_csv(issues_data, filename):
    """
    将 Issue 数据保存为 CSV 文件
    """
    try:
        print(f"正在保存数据到 {filename}...")
        df = pd.DataFrame(issues_data)
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"Issue 数据已保存到 {filename}")
    except Exception as e:
        print(f"保存 CSV 文件时出错: {e}")

def main():
    # GitHub 仓库信息
    repo_owner = "Significant-Gravitas"  # 仓库所有者
    repo_name = "AutoGPT"  # 仓库名称
    
    # 获取 Issue 数据
    issues = fetch_github_issues(repo_owner, repo_name)
    
    if issues:
        print("数据获取成功，开始处理...")
        # 解析数据
        issues_data = process_issues_data(issues)
        
        if issues_data:
            # 保存数据到 CSV 文件
            save_issues_to_csv(issues_data, "AutoGPT_issues.csv")
        else:
            print("未处理到有效的 Issue 数据")
    else:
        print("未能获取到 Issue 数据，请检查配置或重试。")

if __name__ == "__main__":
    main()
