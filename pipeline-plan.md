## CI/CD Automation

Automation is organized into **three pipelines**: **Release**, **Build**, and **Pull Request (PR)**.

### Release Pipeline

**Purpose:** Handle versioned releases and deployments.

**Triggers**
- Manual trigger  
- Git tag creation (semantic versioning) `vX.Y.Z`

**Categorization**
- Tags are categorized as **Major / Minor / Patch**.

**Pipeline matrix**
- Loops over a list of Docker registries or usernames to push images to multiple accounts.

**Typical tasks**
1. Build Docker image  
2. Tag image  
3. Push to DockerHub/ECR  
4. Deploy Terraform infra  
5. Notify stakeholders  

---

### Build Pipeline

**Purpose:** Validate and build the code on push or manual request.

**Triggers**
- Manual trigger  
- `git push` to main or feature branches

**Stages**
1. **Lint check** — PEP8 compliance  
2. **Static analysis** — SonarQube  
3. **Build** — Docker build  
4. **Unit tests** — pytest  
5. **Publish artifacts** — optional

**Example commands**
```bash
docker build -t image-service:latest .
pytest tests/
```

---

### PR Pipeline

**Purpose:** Validate PR quality and enforce review rules.

**Triggers**
- PR opened, updated, reopened, or commits pushed

**Stages**
1. **Code analysis** — lint, SonarQube preview  
2. **Unit tests** — pytest + coverage  
3. **Security scanning** — dependencies  
4. **Notifications** — Discord/Slack  
5. **Auto reviewer assignment** — CODEOWNERS/bot  

---

## Tech Stack

| Category         | Technology                             |
|------------------|----------------------------------------|
| Language         | Python                                 |
| Framework        | Flask                                  |
| Cloud            | AWS S3                                 |
| Infrastructure   | Terraform                              |
| CI/CD            | GitHub Actions / Azure DevOps / Jenkins|
| Security         | IAM (least privilege), S3 encryption   |
| Code Quality     | SonarQube, Flake8, black               |
| Containerization | Docker                                 |
| Testing          | pytest                                 |

---

## Example Workflow

1. Developer commits code → triggers **Build Pipeline**.  
2. Developer opens a PR → triggers **PR Pipeline**.  
3. After approvals and tagging (`vX.Y.Z`) → **Release Pipeline** deploys changes.

---

## Future Improvements

- Add **Redis** caching for frequent reads  
- Implement **image compression** pre-upload  
- Store metadata in **DynamoDB/Postgres**  
- Add **monitoring and alerts**  
- Harden **security and secrets management**  

---

