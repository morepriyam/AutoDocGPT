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
    description = package_data.get("description", "")
    dependencies = package_data.get("dependencies", {})
    scripts = package_data.get("scripts", {})
    return project_name, description, dependencies, scripts

def read_and_filter_files(file_paths):
    return [file_path for file_path in file_paths if not file_path.endswith((".css", ".json"))]

def detect_router_type(file_paths):
    if any("/app/" in path for path in file_paths):
        return "app-router"
    elif any("/pages/" in path for path in file_paths):
        return "pages-router"
    return "react"

def generate_section(prompt):
    def make_request():
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600
        )
        return response

    response = retry_with_backoff(make_request)
    return response.choices[0].message.content.strip()

def generate_readme(project_name, description, dependencies, scripts, file_paths, router_type):
    dependencies_list = "\n".join([f"- **{lib}**: {version}" for lib, version in dependencies.items()])
    file_structure = "\n".join([f"- `{file}`" for file in file_paths])
    scripts_list = "\n".join([f"- **{name}**: `{command}`" for name, command in scripts.items()])

    about_project = generate_section(f"""
Create a project-specific description for "{project_name}" detailing its purpose, unique features, and structure.
Router type: {router_type}
Dependencies: {dependencies_list}
File structure: {file_structure}
""")

    technologies = generate_section(f"""
Analyze the specific dependencies of "{project_name}" and explain their roles and contributions to the project.
Dependencies:
{dependencies_list}
""")

    features = generate_section(f"""
List the key, project-specific features of "{project_name}" derived from its file structure and purpose.
File structure:
{file_structure}
""")

    file_structure_overview = generate_section(f"""
Provide a project-specific explanation of the file structure of "{project_name}" and its significance.
File structure:
{file_structure}
""")

    getting_started = generate_section(f"""
Write a project-specific 'Getting Started' guide for "{project_name}" with detailed steps to set up and run the project.
Dependencies:
{dependencies_list}
""")

    scripts_section = generate_section(f"""
Summarize the scripts available in "{project_name}" with specific and actionable descriptions of their purpose.
Scripts:
{scripts_list}
""")

    readme_content = f"""
<div align="center">
  <h1>{project_name}</h1>
  <p>{description}</p>
</div>

---

# About the Project

{about_project}

---

# Technologies and Libraries

{technologies}

---

# Key Features

{features}

---

# File Structure

{file_structure_overview}

---

# Getting Started

{getting_started}

---

# Scripts and Commands

{scripts_section}
"""
    return "\n".join(readme_content.splitlines()[:200])

def main():
    with open("file_structure.txt", "r") as f:
        file_paths = [line.strip() for line in f.readlines()]

    project_name, description, dependencies, scripts = parse_package_json()
    filtered_files = read_and_filter_files(file_paths)
    router_type = detect_router_type(filtered_files)

    readme_content = generate_readme(project_name, description, dependencies, scripts, filtered_files, router_type)

    with open("README.md", "w") as f:
        f.write(readme_content)
    print("README.md generated successfully.")

if __name__ == "__main__":
    main()
