import requests, os, base64
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

headers = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"}


def get_github_link(package_name: str) -> str:
    api_url = f"https://api.github.com/search/repositories?q={package_name}"
    response = requests.get(api_url, headers=headers)

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
    # TODO: check if I already have the package info, if not - call the get_link func
    is_package_in_db = False
    github_link = "" if is_package_in_db else get_github_link(package_name)

    number_of_contributors = get_contributors_count_from_html(github_link)
    CONTRIBUTORS_PER_PAGE = 30
    all_contributors = []
    all_packages = []

    current_packages = get_all_requirements(github_link)
    # TODO: recursively get all the contributors of the repository
    with ThreadPoolExecutor() as executor:
        packages_futures = [
            executor.submit(get_contributors, package_name)
            for package_name in current_packages
        ]
    for package_future in packages_futures:
        res = package_future.result()
        if res is None:
            break

    owner, repo = github_link.split("/")[-2:]

    api_url = f"https://api.github.com/repos/{owner}/{repo}/contributors"

    def fetch_contributors(page: int) -> int:
        nonlocal all_contributors

        params = {"page": page}
        response = requests.get(api_url, params=params, headers=headers)

        if response.status_code == 200:
            contributors = response.json()
            if not contributors:
                return None
            all_contributors.extend(contributors)
            return page + 1
        else:
            print(f"Error: {response.status_code}")
            return None

    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(fetch_contributors, page)
            for page in range(1, number_of_contributors // CONTRIBUTORS_PER_PAGE + 2)
        ]

    for future in futures:
        result = future.result()
        if result is None:
            break

    # TODO: return list of my entities, check if already existing and update it if necessary
    return all_contributors, all_packages


def get_contributors_count_from_html(github_link: str) -> int:
    owner, repo = github_link.split("/")[-2:]
    try:
        response = requests.get(github_link, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        a_element = soup.find("a", href=f"/{owner}/{repo}/graphs/contributors")
        contributor_element = a_element.find("span", class_="Counter ml-1")
        if contributor_element:
            contributor_count = contributor_element.text.strip()
            return int(contributor_count.replace(",", ""))
        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching HTML content: {e}")
        return None


def get_requirements_file_names(github_link: str) -> list[str]:
    owner, repo = github_link.split("/")[-2:]

    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents"

    response = requests.get(api_url)

    if response.status_code == 200:
        contents = response.json()

        requirements_files = [
            content["name"]
            for content in contents
            if content["type"] == "file"
            and content["name"].endswith(".txt")
            and "requirements" in content["name"]
        ]

        return requirements_files
    else:
        print(f"Error: {response.status_code}")
        return []


def get_requirements_from_file(github_link: str, filename: str) -> str:
    owner, repo = github_link.split("/")[-2:]

    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{filename}"

    response = requests.get(api_url)

    if response.status_code == 200:
        file_info = response.json()

        if "content" in file_info:
            content = base64.b64decode(file_info["content"])

            return content.decode("utf-8")
        else:
            print(f"{filename} not found in {github_link}")
    else:
        print(f"Error: {response.status_code}")


def get_all_requirements(github_link: str):
    requirements_files = get_requirements_file_names(github_link)

    all_dependencies = set()

    for filename in requirements_files:
        content = get_requirements_from_file(github_link, filename)
        dependencies = set(
            line.strip().split()[0]
            for line in content.split("\n")
            if line.strip() and not (line.startswith("#") or line.startswith("-"))
        )
        all_dependencies.update(dependencies)

    print("\n".join(sorted(all_dependencies)))
