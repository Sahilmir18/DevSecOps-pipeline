# DevSecOps-pipeline

The rapid adoption of DevOps and CI/CD (Continuous Integration/Continuous Deployment) methodologies has dramatically accelerated software delivery cycles. However, this velocity often leaves traditional, manual security practices behind, creating a significant risk of deploying vulnerable code and misconfigured cloud infrastructure. This project addresses this critical gap by designing and implementing a comprehensive DevSecOps pipeline that embeds automated security validation directly into the development workflow, a practice known as "Shifting Left."


The core of this project is a robust CI/CD pipeline built using GitHub Actions. This pipeline does not merely build and test code; it acts as an intelligent security gatekeeper. It integrates a suite of custom-built, policy-driven security scanners developed in Python. These scanners perform Static Application Security Testing (SAST) to find vulnerabilities in source code, Software Composition Analysis (SCA) to detect insecure third-party dependencies, and Infrastructure as Code (IaC) analysis to identify misconfigurations in Terraform code for Microsoft Azure.

<img width="576" height="400" alt="secdevops" src="https://github.com/user-attachments/assets/69195d13-2645-4c2f-a5bb-1213267faa8c" />

The system is designed around a Policy-as-Code model, where security rules are defined in simple JSON files, allowing for easy updates without altering the scanner logic. When a developer pushes code, the pipeline automatically triggers, running all security scans in parallel. If any high-severity vulnerability is detected by any scanner, the pipeline fails. This failure signal is enforced by GitHub's branch protection rules, which physically block the merging of non-compliant code into the main branch.




The outcome is a proactive, preventative security control system that provides developers with immediate feedback and ensures a baseline of security is maintained automatically. This project successfully demonstrates how to transform a standard CI/CD pipeline into a powerful, automated security enforcement mechanism, making security an integral and frictionless part of the software development lifecycle.



# DevSecOps Pipeline Template 🛡️


A ready-to-use GitHub repository template that provides a complete, polyglot DevSecOps CI/CD pipeline. This project acts as an automated security gate, preventing insecure code from being merged into your main branch.

This template includes custom-built, policy-driven scanners for:
*   **SAST (Static Application Security Testing)** for Python/Django and JavaScript/React.
*   **SCA (Software Composition Analysis)** for Python (pip) and JavaScript (npm).
*   **IaC (Infrastructure as Code) Security** for Azure Terraform.

## ✨ Key Features

-   **Automated Security Gate:** Uses GitHub Actions and Branch Protection Rules to automatically block PRs with high-severity vulnerabilities.
-   **Policy as Code:** Security rules are defined in simple `.json` files, making them easy to view, edit, and version control.
-   **Polyglot Support:** Includes scanners for both Python/Django and JavaScript/React applications out of the box.
-   **Infrastructure Security:** Scans Terraform code to find common cloud misconfigurations before they are deployed.
-   **Easy to Use:** Get started in minutes by using this repository as a template.

## 🏛️ System Architecture

This pipeline is triggered on every pull request. It runs a series of security scans in parallel. If any scanner finds a high-severity issue, the workflow fails, and the pull request is blocked from merging until the issues are fixed.

<img width="881" height="467" alt="System architecture of devsecops pipeline" src="https://github.com/user-attachments/assets/0e19ddb5-0567-4f13-ba1f-c9168c412047" />


## 🚀 Getting Started


You can have this pipeline running on your own project in just a few minutes.

1.  **Create a New Repository:** Click the green **"Use this template"** button at the top of this page. This will create a new repository in your own GitHub account with a perfect copy of this entire project.

2.  **Open in a Codespace:** In your newly created repository, click the **`<> Code`** button, select the **Codespaces** tab, and click **"Create codespace on main"**. This will give you a ready-to-use development environment in your browser.

3.  **Add Your Code:**
    *   Delete the example applications (`/vulnerable_project` and `/vulnerable-react-app`).
    *   Add your own application code to the repository.
    *   Add your Terraform files to the `/infrastructure` directory.

4.  **Configure the Pipeline:**
    *   Open `.github/workflows/main.yml`.
    *   Update the paths and directory names in each job to point to your application's source files (e.g., update the path to your `requirements.txt` or `package.json`).

5.  **Customize Your Security Policies:**
    *   Go into the scanner directories (e.g., `/sast-scanner`, `/js-sca-scanner`, etc.).
    *   Edit the `rules.json` and `vulnerability_db.json` files to match the vulnerabilities you want to find in your own project.

6.  **Enable Branch Protection:**
    *   In your repository settings, go to **Branches** and add a protection rule for your `main` branch.
    *   Check **"Require status checks to pass before merging"**.
    *   Add the names of all the scanner jobs (e.g., `Python SAST Scan`, `JavaScript SCA Scan`, etc.) as required checks.

That's it! Now, when you create a pull request with your code, your new DevSecOps pipeline will automatically scan it for vulnerabilities.

---

## 🛠️ Integrating with an Existing Repository (Manual Setup)

If you already have a project and want to integrate these security scanners, you can follow these manual steps.

**Step 1: Copy the Scanner Directories**

First, clone this template repository to your local machine. Then, copy the following directories into the root of your own project:

-   `/sast-scanner/`
-   `/sca-scanner/`
-   `/js-sast-scanner/`
-   `/js-sca-scanner/`
-   `/iac-scanner/`

**Step 2: Copy the GitHub Actions Workflow**

Copy the `.github/workflows/main.yml` file from this template into your project's `.github/workflows/` directory. If you already have an existing workflow, you will need to merge the jobs from this file into your own.

**Step 3: Customize the Workflow**

Open the `.github/workflows/main.yml` file and adjust the paths and configurations to match your project's structure. For example, you might need to change:

-   The path to your Python `requirements.txt` file in the `python-sca-scan` job.
-   The path to your `package.json` file in the `js-sca-scan` job.
-   The directory scanned by the SAST scanners to point to your source code folder.

**Step 4: Customize the Security Rules**

Review and edit the `.json` files inside each scanner directory to fit your project's security requirements.

-   Update the `vulnerability_db.json` files with dependencies relevant to your project.
-   Update the `rules.json` files with coding patterns you want to allow or deny.

**Step 5: Commit and Push**

Commit all the new scanner directories and the updated workflow file to your repository. The DevSecOps pipeline will now run on your next pull request.

**Note:** This is a manual setup. If this template is updated with improved scanners, you will need to manually copy the new files to receive the updates.
