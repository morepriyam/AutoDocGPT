import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def retry_with_backoff(func, retries=5, backoff_in_seconds=1):
    import time
    import random
    for attempt in range(retries):
        try:
            return func()
        except Exception as e:
            if attempt < retries - 1:
                sleep_time = backoff_in_seconds * (2 ** attempt) + random.uniform(0, 1)
                time.sleep(sleep_time)
            else:
                raise e

def parse_package_json():
    with open("package.json", "r") as f:
        package_data = json.load(f)
    project_name = package_data.get("name", "Unnamed Project").capitalize()
    description = package_data.get("description", "A financial management platform.")
    dependencies = package_data.get("dependencies", {})
    scripts = package_data.get("scripts", {})
    return project_name, description, dependencies, scripts

def detect_router_type(file_paths):
    if any("/app/" in path for path in file_paths):
        return "app-router"
    elif any("/pages/" in path for path in file_paths):
        return "pages-router"
    return "react"

def generate_section(prompt):
    def make_request():
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=700
        )
        return response

    response = retry_with_backoff(make_request)
    return response.choices[0].message.content.strip()

def generate_readme(project_name, description, dependencies, scripts, file_paths, router_type):
    dependencies_list = "\n".join([f"- **{lib}**: {version}" for lib, version in dependencies.items()])
    file_structure = "\n".join([f"- `{file}`" for file in file_paths])
    scripts_list = "\n".join([f"- **{name}**: `{command}`" for name, command in scripts.items()])

    readme_content = f"""
<div align="center">
  <h1>{project_name}</h1>
</div>

# About the Project
{description}

## Technologies and Libraries
{dependencies_list}

## File Structure
{file_structure}

## Getting Started
### Scripts
{scripts_list}
    """
    return readme_content.strip()

def main():
    with open("file_structure.txt", "r") as f:
        file_paths = [line.strip() for line in f.readlines()]

    project_name, description, dependencies, scripts = parse_package_json()
    router_type = detect_router_type(file_paths)
    readme_content = generate_readme(project_name, description, dependencies, scripts, file_paths, router_type)

    with open("README.md", "w") as f:
        f.write(readme_content)
    print("README.md generated successfully.")

if __name__ == "__main__":
    main()
