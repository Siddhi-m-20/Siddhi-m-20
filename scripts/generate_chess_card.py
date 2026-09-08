import html
import json
import urllib.request
from pathlib import Path


USERNAME = "siddhim76"
API_URL = f"https://api.chess.com/pub/player/{USERNAME}/stats"

OUTPUT = Path("assets/chess-stats.svg")


def fetch_stats():
    request = urllib.request.Request(
        API_URL,
        headers={
            "User-Agent": "Siddhi-Manjarekar-GitHub-Profile/1.0"
        },
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def value(data, *keys, default="—"):
    current = data

    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]

    return current


def fmt(value_):
    if value_ is None:
        return "—"
    return str(value_)


def game_stats(stats, game_type):
    return stats.get(f"chess_{game_type}", {})


def rating(stats, game_type):
    return fmt(
        value(
            game_stats(stats, game_type),
            "last",
            "rating",
            default="—",
        )
    )


def best_rating(stats, game_type):
    return fmt(
        value(
            game_stats(stats, game_type),
            "best",
            "rating",
            default="—",
        )
    )


def collect_games(stats):
    total = wins = losses = draws = 0

    for game_type in ["rapid", "blitz", "bullet", "daily"]:
        record = game_stats(stats, game_type).get("record", {})

        wins += int(record.get("win", 0) or 0)
        losses += int(record.get("loss", 0) or 0)
        draws += int(record.get("draw", 0) or 0)

    total = wins + losses + draws

    return total, wins, losses, draws


def text(value_):
    return html.escape(str(value_))


def card(stats):
    rapid = rating(stats, "rapid")
    blitz = rating(stats, "blitz")
    bullet = rating(stats, "bullet")

    rapid_best = best_rating(stats, "rapid")
    blitz_best = best_rating(stats, "blitz")
    bullet_best = best_rating(stats, "bullet")

    tactics = stats.get("tactics", {})
    lessons = stats.get("lessons", {})
    puzzle_rush = stats.get("puzzle_rush", {})

    puzzle_best = fmt(
        value(tactics, "highest", "rating", default="—")
    )

    lesson_best = fmt(
        value(lessons, "highest", "rating", default="—")
    )

    rush_score = fmt(
        value(puzzle_rush, "best", "score", default="—")
    )

    rush_attempts = fmt(
        value(puzzle_rush, "best", "total_attempts", default="—")
    )

    total_games, wins, losses, draws = collect_games(stats)

    win_rate = "—"

    if total_games:
        win_rate = f"{(wins / total_games) * 100:.1f}%"

    return f"""<svg xmlns="http://www.w3.org/2000/svg"
    width="820"
    height="500"
    viewBox="0 0 820 500">

  <rect
    x="1"
    y="1"
    width="818"
    height="498"
    rx="24"
    fill="#f8fafc"
    stroke="#d1d5db"
    stroke-width="2"/>

  <!-- Header -->
  <text x="42" y="55"
        font-family="Arial, Helvetica, sans-serif"
        font-size="25"
        font-weight="700"
        fill="#111827">
    ♟ Chess.com
  </text>

  <text x="42" y="82"
        font-family="Arial, Helvetica, sans-serif"
        font-size="15"
        fill="#6b7280">
    Chess activity &amp; progress
  </text>

  <text x="778" y="55"
        text-anchor="end"
        font-family="Arial, Helvetica, sans-serif"
        font-size="18"
        font-weight="600"
        fill="#374151">
    {text(USERNAME)}
  </text>

  <!-- Ratings -->
  <text x="42" y="130"
        font-family="Arial, Helvetica, sans-serif"
        font-size="13"
        font-weight="700"
        fill="#6b7280">
    RAPID
  </text>

  <text x="42" y="166"
        font-family="Arial, Helvetica, sans-serif"
        font-size="32"
        font-weight="700"
        fill="#111827">
    {text(rapid)}
  </text>

  <text x="42" y="190"
        font-family="Arial, Helvetica, sans-serif"
        font-size="13"
        fill="#6b7280">
    Best {text(rapid_best)}
  </text>


  <text x="310" y="130"
        font-family="Arial, Helvetica, sans-serif"
        font-size="13"
        font-weight="700"
        fill="#6b7280">
    BLITZ
  </text>

  <text x="310" y="166"
        font-family="Arial, Helvetica, sans-serif"
        font-size="32"
        font-weight="700"
        fill="#111827">
    {text(blitz)}
  </text>

  <text x="310" y="190"
        font-family="Arial, Helvetica, sans-serif"
        font-size="13"
        fill="#6b7280">
    Best {text(blitz_best)}
  </text>


  <text x="578" y="130"
        font-family="Arial, Helvetica, sans-serif"
        font-size="13"
        font-weight="700"
        fill="#6b7280">
    BULLET
  </text>

  <text x="578" y="166"
        font-family="Arial, Helvetica, sans-serif"
        font-size="32"
        font-weight="700"
        fill="#111827">
    {text(bullet)}
  </text>

  <text x="578" y="190"
        font-family="Arial, Helvetica, sans-serif"
        font-size="13"
        fill="#6b7280">
    Best {text(bullet_best)}
  </text>

  <!-- Divider -->
  <line
    x1="42" y1="220"
    x2="778" y2="220"
    stroke="#e5e7eb"
    stroke-width="2"/>

  <!-- Puzzles -->
  <text x="42" y="260"
        font-family="Arial, Helvetica, sans-serif"
        font-size="13"
        font-weight="700"
        fill="#6b7280">
    PUZZLES
  </text>

  <text x="42" y="292"
        font-family="Arial, Helvetica, sans-serif"
        font-size="25"
        font-weight="700"
        fill="#111827">
    {text(puzzle_best)}
  </text>

  <text x="42" y="315"
        font-family="Arial, Helvetica, sans-serif"
        font-size="13"
        fill="#6b7280">
    Best puzzle rating
  </text>

  <!-- Puzzle Rush -->
  <text x="310" y="260"
        font-family="Arial, Helvetica, sans-serif"
        font-size="13"
        font-weight="700"
        fill="#6b7280">
    PUZZLE RUSH
  </text>

  <text x="310" y="292"
        font-family="Arial, Helvetica, sans-serif"
        font-size="25"
        font-weight="700"
        fill="#111827">
    {text(rush_score)}
  </text>

  <text x="310" y="315"
        font-family="Arial, Helvetica, sans-serif"
        font-size="13"
        fill="#6b7280">
    Best score · {text(rush_attempts)} attempts
  </text>

  <!-- Lessons -->
  <text x="578" y="260"
        font-family="Arial, Helvetica, sans-serif"
        font-size="13"
        font-weight="700"
        fill="#6b7280">
    LESSONS
  </text>

  <text x="578" y="292"
        font-family="Arial, Helvetica, sans-serif"
        font-size="25"
        font-weight="700"
        fill="#111827">
    {text(lesson_best)}
  </text>

  <text x="578" y="315"
        font-family="Arial, Helvetica, sans-serif"
        font-size="13"
        fill="#6b7280">
    Best lesson rating
  </text>

  <!-- Games -->
  <line
    x1="42" y1="345"
    x2="778" y2="345"
    stroke="#e5e7eb"
    stroke-width="2"/>

  <text x="42" y="385"
        font-family="Arial, Helvetica, sans-serif"
        font-size="13"
        font-weight="700"
        fill="#6b7280">
    GAMES
  </text>

  <text x="42" y="417"
        font-family="Arial, Helvetica, sans-serif"
        font-size="24"
        font-weight="700"
        fill="#111827">
    {total_games}
  </text>

  <text x="42" y="440"
        font-family="Arial, Helvetica, sans-serif"
        font-size="13"
        fill="#6b7280">
    {wins}W · {losses}L · {draws}D
  </text>

  <!-- Win rate -->
  <text x="310" y="385"
        font-family="Arial, Helvetica, sans-serif"
        font-size="13"
        font-weight="700"
        fill="#6b7280">
    WIN RATE
  </text>

  <text x="310" y="417"
        font-family="Arial, Helvetica, sans-serif"
        font-size="24"
        font-weight="700"
        fill="#111827">
    {text(win_rate)}
  </text>

  <text x="310" y="440"
        font-family="Arial, Helvetica, sans-serif"
        font-size="13"
        fill="#6b7280">
    Wins ÷ rated games
  </text>

  <!-- Footer -->
  <text x="778" y="455"
        text-anchor="end"
        font-family="Arial, Helvetica, sans-serif"
        font-size="11"
        fill="#9ca3af">
    Data from Chess.com Public API
  </text>

</svg>
"""


def main():
    stats = fetch_stats()

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(card(stats), encoding="utf-8")

    print(f"Updated {OUTPUT}")


if __name__ == "__main__":
    main()
