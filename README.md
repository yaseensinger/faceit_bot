# Jagg_bot

A custom Discord bot for the Exedite CS2 community that displays a FACEIT leaderboard based on recent match performance.

## Features

- `/faceit` — Displays player rankings, match statistics, and support performance.
- **CI pipeline** — Automatically checks code quality and runs tests when changes are pushed or pull requests are opened.

## Requirements & Setup

Install dependencies:

```bash
pip install -r requirements.txt
pip install ruff pytest pytest-asyncio
```

Create a `.env` file in the project root:

```dotenv
DISCORD_TOKEN=your_discord_token
FACEIT_API_KEY=your_faceit_api_key
GUILD_IDS=your_discord_server_id
FACEIT_PLAYERS=discord_user_id:faceit_username
```

Add multiple server IDs or players separated by commas.

Run the bot:

```bash
python main.py
```

## Testing

Run the tests:

```bash
python -m pytest -v
```

Run linting:

```bash
python -m ruff check .
```

## CI

GitHub Actions automatically runs checks on pushes and pull requests:

- Python syntax checks
- Ruff linting
- Automated tests using pytest

These checks help catch errors before changes are merged.

## CD 

created and publeshed a docker image to docker hub   