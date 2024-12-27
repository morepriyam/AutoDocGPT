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

def validate_content(content, default_message):
    invalid_phrases = ["cutting-edge", "modern application", "dynamic app"]
    if not content.strip() or any(phrase in content.lower() for phrase in invalid_phrases):
        return default_message
    return content

def parse_package_json():
    with open("package.json", "r") as f:
        package_data = json.load(f)
    project_name = package_data.get("name", "Unnamed Project").capitalize()
    description = package_data.get("description", "")
    if not description.strip() or "application" in description.lower():
        description = f"{project_name} is a tailored platform for enhancing workflows and user productivity."
    return project_name, description, package_data.get("dependencies", {}), package_data.get("scripts", {})

def generate_section(prompt):
    def make_request():
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        return response
    response = retry_with_backoff(make_request)
    return response.choices[0].message.content.strip()

def generate_readme(project_name, description, dependencies, scripts):
    dependencies_list = "\n".join([f"- **{lib}**: {version}" for lib, version in dependencies.items()])
    scripts_list = "\n".join([f"- **{name}**: `{command}`" for name, command in scripts.items()])

    about_project = validate_content(
        generate_section(f"Write a concise description for the project '{project_name}'. Include its purpose, key features, and benefits to users in under 100 words."), 
        f"{project_name} is a platform designed to enhance workflows and simplify complex tasks."
    )

    technologies = validate_content(
        generate_section(f"List and briefly describe the key technologies and libraries used in '{project_name}'. Focus on their role in the project."),
        "Key technologies include React, Next.js, and Tailwind CSS for modern web development."
    )

    features = validate_content(
        generate_section(f"Provide a concise, bullet-point list of the top features of '{project_name}' based on its functionality."),
        "- User authentication\n- Data visualization\n- Responsive design"
    )

    setup = validate_content(
        generate_section(f"Provide concise installation and setup instructions for '{project_name}', focusing on essential steps."),
        "1. Clone the repository\n2. Install dependencies with `npm install`\n3. Run the development server with `npm run dev`"
    )

    usage = validate_content(
        generate_section(f"Write a concise usage guide for '{project_name}', focusing on running the application and key workflows."),
        "Start the application with `npm run dev`. Access it at `http://localhost:3000`."
    )

    acknowledgements = validate_content(
        generate_section(f"Write a concise acknowledgements section for '{project_name}', highlighting key libraries and contributors."),
        "This project uses React, Next.js, and Tailwind CSS. Thanks to the open-source community for their support."
    )

    return f"""
<div align="center">
  <h1>{project_name}</h1>
  <p>{description}</p>
</div>

---

## About the Project

{about_project}

---

## Technologies Used

{technologies}

---

## Features

{features}

---

## Setup and Installation

{setup}

---

## Usage

{usage}

---

## Acknowledgements

{acknowledgements}
    """.strip()

def main():
    with open("file_structure.txt", "r") as f:
        file_paths = [line.strip() for line in f.readlines()]

    project_name, description, dependencies, scripts = parse_package_json()
    readme_content = generate_readme(project_name, description, dependencies, scripts)

    with open("README.md", "w") as f:
        f.write(readme_content)
    print("README.md generated successfully.")

if __name__ == "__main__":
    main()
