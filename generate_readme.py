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
    if not description or "application" in description.lower() or "modern" in description.lower():
        description = f"{project_name} is a dynamic project offering tailored functionality for its users."
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

def validate_content(content, default_message):
    if not content.strip() or "cutting-edge" in content.lower() or "modern" in content.lower():
        return default_message
    return content

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
Create a tailored, high-quality description for the project "{project_name}" based on its file structure, router type ({router_type}), and dependencies. Highlight purpose, features, and user benefits without generic phrases.

### Dependencies
{dependencies_list}

### File Structure
{file_structure}
"""
    about_project = validate_content(
        generate_section(description_prompt),
        f"{project_name} is a comprehensive project designed to simplify workflows and enhance user productivity."
    )

    technologies_prompt = f"""
Analyze the following dependencies for the project "{project_name}" and explain the key libraries used and their contributions to the project. Be specific and avoid redundancy.

### Dependencies
{dependencies_list}
"""
    technologies = validate_content(
        generate_section(technologies_prompt),
        f"The project employs a modern tech stack, ensuring efficiency, scalability, and optimal user experience."
    )

    features_prompt = f"""
Generate a list of tailored, high-impact features for the project "{project_name}" based on the file structure and its intended purpose.

### File Structure
{file_structure}
"""
    features = validate_content(
        generate_section(features_prompt),
        f"{project_name} offers intuitive features to enhance user workflows."
    )

    file_structure_prompt = f"""
Provide a concise and organized overview of the file structure for the project "{project_name}". Focus on key files and their purposes.

### File Structure
{file_structure}
"""
    file_structure_overview = validate_content(
        generate_section(file_structure_prompt),
        f"The file structure of {project_name} is organized for maintainability and scalability."
    )

    getting_started_prompt = f"""
Generate a concise 'Getting Started' section for the project "{project_name}" that includes installation steps, environment setup, and how to run the project.

### Dependencies
{dependencies_list}

### File Structure
{file_structure}
"""
    getting_started = validate_content(
        generate_section(getting_started_prompt),
        f"To get started with {project_name}, clone the repository, install dependencies, and run the development server."
    )

    scripts_prompt = f"""
Generate a concise 'Scripts and Commands' section for the project "{project_name}". Summarize the purpose of each command from the list.

### Scripts
{scripts_list}
"""
    scripts_section = validate_content(
        generate_section(scripts_prompt),
        "The project includes essential scripts for development, testing, and deployment."
    )

    faq_prompt = f"""
Generate a concise FAQ section for the project "{project_name}". Focus on common setup issues, feature usage, and configuration tips.

### Dependencies
{dependencies_list}

### File Structure
{file_structure}
"""
    faq = validate_content(
        generate_section(faq_prompt),
        "For common questions, refer to the documentation or contact the support team."
    )

    contribution_prompt = f"""
Generate a concise 'Contributing' section for the project "{project_name}" with clear and actionable steps for collaboration.

### Dependencies
{dependencies_list}

### File Structure
{file_structure}
"""
    contributing = validate_content(
        generate_section(contribution_prompt),
        "We welcome contributions! Fork the repository, make changes, and submit a pull request."
    )

    acknowledgements_prompt = f"""
Generate a concise acknowledgements section for the project "{project_name}" that highlights key libraries, tools, and contributors.

### Dependencies
{dependencies_list}

### File Structure
{file_structure}
"""
    acknowledgements = validate_content(
        generate_section(acknowledgements_prompt),
        "This project was made possible thanks to open-source libraries and the contributions of our team."
    )

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
