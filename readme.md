# AutoDocGPT

**AutoDocGPT** is a GitHub Action designed to automatically generate a tailored, professional `README.md` file for your Next.js and React projects. Powered by OpenAI's GPT technology, AutoDocGPT scans your project files, detects structures like routers and `src` folders, and produces meaningful, concise documentation with minimal API calls.

---

## **Features**

- **Automated README Generation**: Creates or updates your `README.md` file effortlessly.
- **Dynamic Project Support**:
  - Supports Next.js (`app-router` and `pages-router`) and React projects.
  - Adapts to projects with or without a `src` folder.
- **Key Insights Extraction**:
  - Summarizes your project's structure, key components, and features.
  - Extracts and documents scripts from `package.json`.
- **Efficient API Usage**: Batch processing minimizes OpenAI API calls, optimizing token usage and cost.
- **Router Type Detection**: Automatically detects if the project uses `app-router`, `pages-router`, or standard React configurations.

---

## **How It Works**

1. **Analyze Project Files**: AutoDocGPT scans files in the `src` folder (if it exists) or the entire project.
2. **Identify Project Details**:
   - Detects router type (`app-router`, `pages-router`, or React).
   - Extracts and processes scripts, key files, and folder structures.
3. **Generate Tailored Content**:
   - Uses OpenAI's GPT API to create concise descriptions for your files and components.
   - Dynamically adapts content to your project's structure.
4. **Update README**:
   - Writes or updates the `README.md` file in your repository with the latest details.

---

## **Usage**

### **Prerequisites**

1. **GitHub Actions Enabled**: Ensure GitHub Actions are enabled for your repository.
2. **OpenAI API Key**: Obtain an OpenAI API key and store it in your repository secrets as `OPENAI_API_KEY`.

---

### **Workflow Setup**

Create a workflow file (e.g., `.github/workflows/autodocgpt.yml`) with the following content:

```yaml
name: AutoDocGPT

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  generate-readme:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Use AutoDocGPT
        uses: morepriyam/autodocgpt@v1.0
        with:
          email: ${{ github.actor }}@users.noreply.github.com
          name: ${{ github.actor }}
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

## **Changelog**

### **v1.0**

- Initial release of AutoDocGPT.
- Supports Next.js (`app-router`, `pages-router`) and React projects.
- Automatically adapts to projects with or without a `src` folder.
- Generates summaries for files, components, and scripts.
- Efficient API usage with batch processing.
  Contributing
  markdown
  Copy code

## **Contributing**

We welcome contributions! To contribute:

1. **Fork this repository**.
2. Create a feature branch:
   ```bash
   git checkout -b feature/new-feature
   Commit your changes:
   bash
   Copy code
   git commit -m "Add new feature"
   Push to the branch:
   bash
   Copy code
   git push origin feature/new-feature
   Open a pull request.
   yaml
   Copy code
   ```

---

## **Acknowledgements**

- **[OpenAI](https://openai.com/)**: For providing the GPT API that powers this action.
- **[GitHub Actions](https://github.com/features/actions)**: For enabling seamless CI/CD workflows.
  License
  markdown
  Copy code

## **License**

This project is licensed under the [MIT License](LICENSE).
