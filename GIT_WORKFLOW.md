# 🧪 Git Team Workflow: Feature Branch Strategy

## 📌 Overview

This workflow ensures all team members:
- Start from the latest `dev` branch
- Work on isolated features
- Keep feature branches in sync with `dev`
- Cleanly merge back to `dev` after review

---

## Branch Flow Diagram

```mermaid
gitGraph
   commit id: "Initial Commit"
   branch dev
   checkout dev
   commit id: "Dev setup"

   branch feature-A
   checkout feature-A
   commit id: "Work A1"
   commit id: "Work A2"

   checkout dev
   branch feature-B
   checkout feature-B
   commit id: "Work B1"
   commit id: "Work B2"

   checkout dev
   merge feature-B id: "Merge feature-B into dev"

   checkout feature-A
   merge dev id: "Sync feature-A with dev"
   commit id: "Work A3"

   checkout dev
   merge feature-A id: "Merge feature-A into dev"
```

## Team should follow

- Create a new feature branch
```bash
git checkout dev
git pull origin dev
git checkout -b feature/my-feature
```
- Work on your feature branch
```bash
git add .
git commit -m "Implemented part of feature"
```
- Keep your feature branch updated with latest dev

Do this regularly and before merging:

```bash
git checkout dev
git pull origin dev
git checkout feature/my-feature
git merge dev
```
- Merge your feature branch into dev
```bash
git checkout dev
git pull origin dev
git merge feature/my-feature
git push origin dev
```

- Continue working on your feature branch
```bash
git checkout dev
git pull origin dev
git checkout feature/my-feature
git merge dev
```
