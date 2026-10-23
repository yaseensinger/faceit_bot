
import os
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

# Provide dummy configuration so importing the bot doesn't need real secrets.
os.environ["DISCORD_TOKEN"] = "test-token"
os.environ["FACEIT_API_KEY"] = "test-api-key"
os.environ["GUILD_IDS"] = "123456789"
os.environ["FACEIT_PLAYERS"] = "111:Alice,222:Bob"

import main


def make_interaction():
    """Create a fake Discord interaction."""
    names = {111: "Alice", 222: "Bob"}

    return SimpleNamespace(
        response=SimpleNamespace(defer=AsyncMock()),
        followup=SimpleNamespace(send=AsyncMock()),
        guild=SimpleNamespace(
            get_member=lambda user_id: (
                SimpleNamespace(display_name=names[user_id])
                if user_id in names
                else None
            )
        ),
    )


@pytest.mark.asyncio
async def test_faceit_command_handles_no_data(monkeypatch):
    """The command should reply if no FACEIT players can be loaded."""
    monkeypatch.setattr(
        main, "get_faceit_player", AsyncMock(return_value=None)
    )

    interaction = make_interaction()

    await main.faceit_leaderboard.callback(interaction)

    interaction.response.defer.assert_awaited_once()
    interaction.followup.send.assert_awaited_once_with(
        "No faceit data man."
    )


@pytest.mark.asyncio
async def test_faceit_command_builds_leaderboard(monkeypatch):
    """The command should produce a leaderboard embed from player data."""
    async def fake_get_player(username):
        return {
            "player_id": f"id-{username}",
        }

    performances = {
        "id-Alice": {
            "match_count": 5,
            "wins": 4,
            "losses": 1,
            "kr": 0.8,
            "adr": 90.0,
            "entry_success_rate": 0.6,
            "total_clutches": 4,
            "win_rate": 80.0,
            "kd": 1.5,
            "util_dmg_per_match": 40.0,
            "enemies_flashed_per_match": 3.0,
            "utility_success_rate": 0.7,
        },
        "id-Bob": {
            "match_count": 5,
            "wins": 2,
            "losses": 3,
            "kr": 0.5,
            "adr": 60.0,
            "entry_success_rate": 0.3,
            "total_clutches": 1,
            "win_rate": 40.0,
            "kd": 0.8,
            "util_dmg_per_match": 20.0,
            "enemies_flashed_per_match": 1.0,
            "utility_success_rate": 0.4,
        },
    }

    async def fake_get_performance(player_id, limit=5):
        return performances[player_id]

    monkeypatch.setattr(
        main, "get_faceit_player", fake_get_player
    )
    monkeypatch.setattr(
        main, "get_faceit_recent_performance", fake_get_performance
    )

    interaction = make_interaction()

    await main.faceit_leaderboard.callback(interaction)

    interaction.response.defer.assert_awaited_once()
    interaction.followup.send.assert_awaited_once()

    embed = interaction.followup.send.await_args.kwargs["embed"]

    assert embed.title == "Exedite FACEIT Leaderboard"
    assert "Alice" in embed.description
    assert "Bob" in embed.description

    field_names = [field.name for field in embed.fields]

    assert field_names == [
        "Current GOAT",
        "Server Shitter",
        "Grenade Geezer",
        "Utility Unloader",
    ]

    assert "<@111>" in embed.fields[0].value
    assert "<@222>" in embed.fields[1].value
