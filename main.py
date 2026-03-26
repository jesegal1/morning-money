from scraper import fetch_all_articles, mark_as_seen
from educator import generate_education
from emailer import send_digest

def main():
    print("=" * 50)
    print("MORNING MONEY — Starting pipeline")
    print("=" * 50)

    articles = fetch_all_articles(days_back=7)

    if not articles:
        print("No fresh articles found.")
        articles = []

    print("\nGenerating finance concept and tip of the day...")
    education = generate_education()

    print("\nPicking top article...")
    top_article = pick_top_article(articles)

    success = send_digest(top_article, education)

    if success and top_article:
        mark_as_seen([top_article])
        print("Marked article as seen.")

    print("\nPipeline complete.")


def pick_top_article(articles):
    if not articles:
        return None

    import os
    import json
    import anthropic
    from dotenv import load_dotenv
    load_dotenv()

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    titles_list = "\n".join(
        [f"{i+1}. {a['title']}" for i, a in enumerate(articles[:40])]
    )

    prompt = f"""You are a financial advisor for a physician who just became an attending cardiologist. They have large student loans, a young family, and want to be smarter with money.

Pick the ONE most relevant and actionable article from this list. Prefer articles about:
- Physician-specific finance (student loans, PSLF, disability insurance, contracts)
- Investing fundamentals (index funds, retirement accounts, tax strategy)
- Personal finance for high earners
- Market news that actually affects a young physician's decisions

Avoid: crypto hype, day trading, clickbait, articles not relevant to a physician's financial life.

Articles:
{titles_list}

Respond with ONLY a JSON object, no other text:
{{"pick": 3, "reason": "one sentence why"}}"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=100,
            messages=[{"role": "user", "content": prompt}]
        )
        result = json.loads(response.content[0].text)
        idx = result.get("pick", 1) - 1
        if 0 <= idx < len(articles):
            chosen = articles[idx]
            chosen["pick_reason"] = result.get("reason", "")
            return chosen
    except Exception as e:
        print(f"  Error picking article: {e}")

    return articles[0] if articles else None


if __name__ == "__main__":
    main()
