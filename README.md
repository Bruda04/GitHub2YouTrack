# GitHub2YouTrack

Automatically synchronize GitHub issues to YouTrack tasks, including updates.

## Features

- ✅ Create YouTrack tasks from GitHub issues
- 🔄 Sync updates (title, description, state, labels, assignees)

## Demo

[Demo Video](doc/demo/demo.mp4)

## Prerequisites

- Python 3.12+
- GitHub Personal Access Token
- YouTrack Permanent Token

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Bruda04/GitHub2YouTrack
cd GitHub2YouTrack
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:

Copy the example environment file:
```bash
cp .env.local .env
```

Edit `.env` with your credentials:
```bash
GITHUB_TOKEN=your_github_token_here
GITHUB_REPOSITORY_NAME=your_github_repo_name_here
GITHUB_REPOSITORY_OWNER=your_github_repo_owner_here

YOUTRACK_URL=your_youtrack_url_here
YOUTRACK_TOKEN=your_youtrack_token_here
YOUTRACK_PROJECT_SHORT_NAME=your_youtrack_project_short_name_here

SYNC_INTERVAL_MINUTES=1
```

4. [Run the program](#usage)

## Getting Tokens

### GitHub Token
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new Fine-grained token
3. Select repository access and set permissions to read and write issues

### YouTrack Token
1. Go to YouTrack → Profile → Account Security → Permanent Tokens
2. New token → Permanent token
3. Copy the token

## Usage

Run the sync:
```bash
python -m src.main
```

The program will:
1. Fetch all issues from GitHub
2. Create new tasks
3. Display a summary of actions taken
4. Start tracking changes and sync them

