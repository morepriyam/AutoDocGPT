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
    description = package_data.get("description", None)
    dependencies = package_data.get("dependencies", {})
    scripts = package_data.get("scripts", {})
    return project_name, description, dependencies, scripts

def read_and_filter_files(file_paths):
    filtered_files = [
        file_path for file_path in file_paths
        if not file_path.endswith((".css", ".json"))
    ]
    return filtered_files

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
            max_tokens=500  # Reduced to fit concise content
        )
        return response

    response = retry_with_backoff(make_request)
    return response.choices[0].message.content.strip()

def generate_readme(project_name, description, dependencies, scripts, file_paths, router_type):
    dependencies_list = "\n".join([f"- **{lib}**: {version}" for lib, version in dependencies.items()])
    file_structure = "\n".join([f"- `{file}`" for file in file_paths[:10]])  # Limit file list to top 10
    scripts_list = "\n".join([f"- **{name}**: `{command}`" for name, command in scripts.items()])

    # Generate description if missing
    if not description:
        description_prompt = f"""
Generate a concise, project-specific description for "{project_name}" based on its file structure, router type ({router_type}), and dependencies.

### Dependencies
{dependencies_list}

### File Structure
{file_structure}
"""
        description = generate_section(description_prompt)

    about_project_prompt = f"""
Create a tailored 'About the Project' section for "{project_name}" based on its file structure, router type ({router_type}), and dependencies. Include purpose, features, and benefits.

### Dependencies
{dependencies_list}

### File Structure
{file_structure}
"""
    about_project = generate_section(about_project_prompt)

    technologies_prompt = f"""
Analyze the dependencies for "{project_name}" and identify the key libraries. Explain their importance and how they contribute to the application.

### Dependencies
{dependencies_list}
"""
    technologies = generate_section(technologies_prompt)

    features_prompt = f"""
Based on the project "{project_name}" and its file structure, list key features that highlight the project's purpose and capabilities.

### File Structure
{file_structure}
"""
    features = generate_section(features_prompt)

    getting_started_prompt = f"""
Generate a tailored 'Getting Started' section for the project "{project_name}". Include setup steps, installation instructions, and running the project.

### Dependencies
{dependencies_list}

### File Structure
{file_structure}
"""
    getting_started = generate_section(getting_started_prompt)

    faq_prompt = f"""
Generate a concise FAQ section for "{project_name}". Include key troubleshooting tips, common questions, and quick solutions.

### Dependencies
{dependencies_list}

### File Structure
{file_structure}
"""
    faq = generate_section(faq_prompt)

    contributing_prompt = f"""
Generate a concise 'Contributing' section for "{project_name}" with clear steps for submitting contributions and engaging with the community.

### Dependencies
{dependencies_list}

### File Structure
{file_structure}
"""
    contributing = generate_section(contributing_prompt)

    acknowledgements_prompt = f"""
Generate a short acknowledgements section for "{project_name}" that highlights key tools, libraries, and contributors.

### Dependencies
{dependencies_list}
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

**Highlighted Files**:
{file_structure}

For a full list, refer to the repository.

---

# Getting Started

{getting_started}

---

# Scripts and Commands

**Scripts Overview**:
{scripts_list}

For additional commands, see `package.json`.

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
