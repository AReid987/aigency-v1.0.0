---
type: Page
title: Infrastructure and Deployment Overview
description: null
icon: null
createdAt: '2025-07-11T08:53:41.791Z'
creationDate: 2025-07-11 03:53
modificationDate: 2025-07-11 03:53
tags: []
coverImage: null
---

# Infrastructure and Deployment Overview

- **Cloud Provider(s):** AWS

- **Core Services Used:** AWS Lambda (for stateless services), AWS S3 (static assets), AWS EC2 (for services requiring dedicated instances, e.g., browser automation might run on EC2 or Fargate), AWS RDS (if relational DB considered later), AWS DynamoDB (for specific NoSQL needs), AWS ECS/Fargate (for containerized services).

- **Infrastructure as Code (IaC):** AWS CDK - Location: `infra/` directory within the monorepo.

- **Deployment Strategy:** CI/CD pipeline with automated promotions (e.g., `dev` -> `staging` -> `production`). Blue/Green deployment or Canary releases for critical updates will be considered where appropriate to minimize downtime.

- **Tools:** GitHub Actions for CI/CD automation. Docker for containerization of all services.

- **Environments:** Development (local), Staging (AWS), Production (AWS).

- **Environment Promotion:** Automated after tests pass for `dev` to `staging`. Manual approval after `staging` tests pass, then automated to `production` after passing production readiness checks.

- **Rollback Strategy:** Automated rollback to previous stable version on health check failure post-deployment, or manual trigger via CI/CD job. Docker containerization and IaC state management support efficient rollbacks.

