# DevSecOps-pipeline

The rapid adoption of DevOps and CI/CD (Continuous Integration/Continuous Deployment) methodologies has dramatically accelerated software delivery cycles. However, this velocity often leaves traditional, manual security practices behind, creating a significant risk of deploying vulnerable code and misconfigured cloud infrastructure. This project addresses this critical gap by designing and implementing a comprehensive DevSecOps pipeline that embeds automated security validation directly into the development workflow, a practice known as "Shifting Left."


The core of this project is a robust CI/CD pipeline built using GitHub Actions. This pipeline does not merely build and test code; it acts as an intelligent security gatekeeper. It integrates a suite of custom-built, policy-driven security scanners developed in Python. These scanners perform Static Application Security Testing (SAST) to find vulnerabilities in source code, Software Composition Analysis (SCA) to detect insecure third-party dependencies, and Infrastructure as Code (IaC) analysis to identify misconfigurations in Terraform code for Microsoft Azure.

<img width="576" height="400" alt="secdevops" src="https://github.com/user-attachments/assets/69195d13-2645-4c2f-a5bb-1213267faa8c" />

The system is designed around a Policy-as-Code model, where security rules are defined in simple JSON files, allowing for easy updates without altering the scanner logic. When a developer pushes code, the pipeline automatically triggers, running all security scans in parallel. If any high-severity vulnerability is detected by any scanner, the pipeline fails. This failure signal is enforced by GitHub's branch protection rules, which physically block the merging of non-compliant code into the main branch.




The outcome is a proactive, preventative security control system that provides developers with immediate feedback and ensures a baseline of security is maintained automatically. This project successfully demonstrates how to transform a standard CI/CD pipeline into a powerful, automated security enforcement mechanism, making security an integral and frictionless part of the software development lifecycle.


