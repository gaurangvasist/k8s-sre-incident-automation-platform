# Kubernetes SRE Incident Automation Platform

A production-style DevOps/SRE portfolio project that deploys a demo microservice to Kubernetes using Helm and Argo CD, monitors workload health with Prometheus and Grafana, simulates common Kubernetes failure scenarios, and generates automated Markdown incident reports from real cluster evidence.

## What this project demonstrates

- Containerized microservice deployment
- Helm-based Kubernetes packaging
- GitOps deployment with Argo CD
- Kubernetes health checks, probes, resources, and services
- Prometheus/Grafana observability
- Failure simulation for ImagePullBackOff, CrashLoopBackOff, readiness failures, and resource pressure
- Automated triage using Bash/Python scripts
- Incident reports, runbooks, and postmortem documentation
- Optional AWS EKS/Terraform extension
