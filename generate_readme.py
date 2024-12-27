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

def read_and_filter_files(file_paths):
    selected_files = [
        file_path for file_path in file_paths
        if not file_path.endswith((".css", ".json"))
    ]
    return selected_files

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
            max_tokens=700
        )
        return response

    response = retry_with_backoff(make_request)
    return response.choices[0].message.content.strip()

def generate_readme(project_name, description, dependencies, scripts, file_paths, router_type):
    dependencies_list = "\n".join([f"- **{lib}**: {version}" for lib, version in dependencies.items()])
    file_structure = "\n".join([f"- `{file}`" for file in file_paths])
    scripts_list = "\n".join([f"- **{name}**: `{command}`" for name, command in scripts.items()])

    description_prompt = f"""
Create a tailored, high-quality description for the project "{project_name}" based on its file structure, router type ({router_type}), and dependencies. Ensure it is concise and clear, highlighting purpose, features, and user benefits.

### Dependencies
{dependencies_list}

### File Structure
{file_structure}
"""
    about_project = generate_section(description_prompt)

    technologies_prompt = f"""
Analyze the following dependencies for the project "{project_name}" and explain the key libraries used and their contributions to the project. Be specific and avoid redundancy.

### Dependencies
{dependencies_list}
"""
    technologies = generate_section(technologies_prompt)

    features_prompt = f"""
Generate a list of tailored, high-impact features for the project "{project_name}" based on the file structure and its intended purpose.

### File Structure
{file_structure}
"""
    features = generate_section(features_prompt)

    file_structure_prompt = f"""
Provide a concise and organized overview of the file structure for the project "{project_name}". Focus only on key files and directories.

### File Structure
{file_structure}
"""
    file_structure_overview = generate_section(file_structure_prompt)

    getting_started_prompt = f"""
Generate a concise 'Getting Started' section for the project "{project_name}" that includes installation steps, environment setup, and how to run the project.

### Dependencies
{dependencies_list}

### File Structure
{file_structure}
"""
    getting_started = generate_section(getting_started_prompt)

    scripts_prompt = f"""
Generate a concise 'Scripts and Commands' section for the project "{project_name}". Summarize the purpose of each command from the list.

### Scripts
{scripts_list}
"""
    scripts_section = generate_section(scripts_prompt)

    faq_prompt = f"""
Generate a concise FAQ section for the project "{project_name}". Focus on common setup issues, feature usage, and configuration tips.

### Dependencies
{dependencies_list}

### File Structure
{file_structure}
"""
    faq = generate_section(faq_prompt)

    contribution_prompt = f"""
Generate a concise 'Contributing' section for the project "{project_name}" with clear and actionable steps for collaboration.

### Dependencies
{dependencies_list}

### File Structure
{file_structure}
"""
    contributing = generate_section(contribution_prompt)

    acknowledgements_prompt = f"""
Generate a concise acknowledgements section for the project "{project_name}" that highlights key libraries, tools, and contributors.

### Dependencies
{dependencies_list}

### File Structure
{file_structure}
"""
    acknowledgements = generate_section(acknowledgements_prompt)

    readme_content = f"""
<div align="center">
  <h1>{project_name}</h1>
  <p>{description}</p>
</div>

---

# Table of Contents
- [About the Project](#about-the-project)
- [Technologies and Libraries](#technologies-and-libraries)
- [Key Features](#key-features)
- [File Structure](#file-structure)
- [Getting Started](#getting-started)
- [Scripts and Commands](#scripts-and-commands)
- [FAQ](#faq)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)

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

---

# FAQ

{faq}

---

# Contributing

{contributing}

---

# Acknowledgements

{acknowledgements}
    """
    return readme_content.strip()

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
