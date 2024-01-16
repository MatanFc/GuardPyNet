import requests


def get_github_link(package_name: str) -> str:
    api_url = f"https://api.github.com/search/repositories?q={package_name}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()

        if data["total_count"] > 0:
            # Extract the URL of the first repository (assuming the most relevant result)
            github_link = data["items"][0]["html_url"]
            return github_link
        else:
            print(f"No GitHub repository found for {package_name}")
    else:
        print(f"Error: {response.status_code}")


def get_contributors(package_name: str) -> dict:
    github_link = get_github_link(package_name)
    owner, repo = github_link.split("/")[-2:]

    api_url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
    all_contributors = []

    page = 1
    while True:
        params = {"page": page}
        response = requests.get(api_url, params=params)

        if response.status_code == 200:
            contributors = response.json()
            if not contributors:
                break
            all_contributors.extend(contributors)
            page += 1
        else:
            print(f"Error: {response.status_code}")
            break

    for contributor in all_contributors:
        id = contributor["id"]
        login = contributor["login"]
        contributions = contributor["contributions"]
        print(f"ID: {id}, Contributor: {login}, Contributions: {contributions}")
