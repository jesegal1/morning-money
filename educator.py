import os
import json
import random
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SEEN_TOPICS_FILE = "seen_topics.json"

def load_seen_topics():
    if os.path.exists(SEEN_TOPICS_FILE):
        with open(SEEN_TOPICS_FILE, "r") as f:
            return json.load(f)
    return []

def save_seen_topics(topics):
    with open(SEEN_TOPICS_FILE, "w") as f:
        json.dump(topics, f, indent=2)

# ── Physician Finance Blueprint (~60 topics) ──────────────────────────
FINANCE_TOPICS = [
    # Student Loans (you have lots — this section is heavy)
    ("PSLF - Public Service Loan Forgiveness Explained", "Student Loans"),
    ("Income-Driven Repayment Plans Compared (SAVE, PAYE, IBR)", "Student Loans"),
    ("Should You Refinance Your Student Loans or Stay on PSLF?", "Student Loans"),
    ("The IDR Tax Bomb - What Happens When Loans Are Forgiven", "Student Loans"),
    ("Employer Student Loan Repayment Benefits (Section 127)", "Student Loans"),
    ("Certifying Employment for PSLF - Common Mistakes", "Student Loans"),
    ("Spousal Income and Student Loan Strategy (Filing Separately vs Jointly)", "Student Loans"),

    # Retirement Accounts
    ("403(b) vs 401(k) - What Physicians Need to Know", "Retirement"),
    ("The 457(b) - The Physician Secret Weapon", "Retirement"),
    ("Backdoor Roth IRA Step by Step", "Retirement"),
    ("Mega Backdoor Roth - Advanced Retirement Strategy", "Retirement"),
    ("Traditional vs Roth - Which Is Better for a High Earner?", "Retirement"),
    ("SEP IRA and Solo 401(k) for Moonlighting Income", "Retirement"),
    ("Target Date Funds vs Three-Fund Portfolio", "Retirement"),
    ("How Much to Save for Retirement as a New Attending", "Retirement"),
    ("HSA - The Triple Tax Advantage Account", "Retirement"),

    # Insurance (critical for new attendings)
    ("Own-Occupation Disability Insurance - Why Physicians Need It", "Insurance"),
    ("Term vs Whole Life Insurance - The Physician Answer", "Insurance"),
    ("Umbrella Insurance - Cheap Protection for High Earners", "Insurance"),
    ("Malpractice Insurance - Claims-Made vs Occurrence", "Insurance"),
    ("When and How Much Life Insurance to Buy", "Insurance"),
    ("Long-Term Care Insurance - Too Early to Think About?", "Insurance"),

    # Investing Fundamentals
    ("Index Fund Investing - The Physician's Best Friend", "Investing"),
    ("Asset Allocation - How to Split Stocks, Bonds, and Cash", "Investing"),
    ("Tax-Loss Harvesting Explained Simply", "Investing"),
    ("Dollar Cost Averaging vs Lump Sum Investing", "Investing"),
    ("Bond Basics - Why You Need Them Even Though They're Boring", "Investing"),
    ("International vs US Stocks - How Much Diversification?", "Investing"),
    ("Why You Should Never Pick Individual Stocks", "Investing"),
    ("Vanguard vs Fidelity vs Schwab - Choosing a Brokerage", "Investing"),
    ("Emergency Fund - How Much Cash to Keep and Where", "Investing"),
    ("I Bonds and TIPS - Inflation-Protected Investing", "Investing"),

    # Tax Strategy
    ("Marginal vs Effective Tax Rate - Know the Difference", "Tax Strategy"),
    ("Tax-Advantaged Accounts Priority Order (What to Fund First)", "Tax Strategy"),
    ("W-2 vs 1099 Physician - Tax Implications", "Tax Strategy"),
    ("S-Corp Election for Moonlighting Income", "Tax Strategy"),
    ("Quarterly Estimated Taxes If You Moonlight", "Tax Strategy"),
    ("Charitable Giving - Donor Advised Funds for Physicians", "Tax Strategy"),
    ("State Income Tax - Does It Matter Where You Practice?", "Tax Strategy"),
    ("Tax Deductions New Attendings Miss", "Tax Strategy"),

    # Real Estate
    ("Rent vs Buy as a New Attending - The Real Math", "Real Estate"),
    ("Physician Mortgage Loans - No PMI, No Problem?", "Real Estate"),
    ("How Much House Can You Actually Afford?", "Real Estate"),
    ("15-Year vs 30-Year Mortgage for High Earners", "Real Estate"),
    ("Real Estate Investing (REITs) Without Being a Landlord", "Real Estate"),

    # Career and Contract
    ("Reading Your First Attending Employment Contract", "Career"),
    ("RVU-Based Compensation Explained", "Career"),
    ("Negotiating Salary, Sign-On Bonus, and Benefits", "Career"),
    ("Partnership Track - What to Look For", "Career"),
    ("Moonlighting as an Attending - Is It Worth It?", "Career"),
    ("Non-Compete Clauses - What They Actually Mean", "Career"),

    # Budgeting and Lifestyle
    ("The Live Like a Resident Rule (and When to Stop)", "Budgeting"),
    ("Your First Attending Budget - A Template", "Budgeting"),
    ("Automating Your Finances - Set It and Forget It", "Budgeting"),
    ("Lifestyle Inflation - The Silent Wealth Killer", "Budgeting"),
    ("Credit Score Optimization for Physicians", "Budgeting"),

    # Estate Planning and Family
    ("529 Plans - Saving for Your Son's College", "Family Finance"),
    ("Will and Trust Basics for New Attendings", "Family Finance"),
    ("Beneficiary Designations - The Most Overlooked Task", "Family Finance"),
    ("Power of Attorney and Healthcare Proxy", "Family Finance"),
    ("Life Insurance Needs with a Young Family", "Family Finance"),

    # Physician-Specific Traps
    ("Why Financial Advisors Target Physicians (and Red Flags)", "Physician Traps"),
    ("Whole Life Insurance Sold to Residents - What to Do Now", "Physician Traps"),
    ("The Doctor Car and Doctor House Trap", "Physician Traps"),
    ("AUM vs Fee-Only Financial Advisors", "Physician Traps"),
]

def pick_fresh_topic(seen_list):
    unseen = [t for t in FINANCE_TOPICS if t[0] not in seen_list]
    if not unseen:
        seen_list.clear()
        unseen = FINANCE_TOPICS
    return random.choice(unseen)


def generate_concept():
    seen = load_seen_topics()
    topic, category = pick_fresh_topic(seen)
    seen.append(topic)
    save_seen_topics(seen)

    prompt = f"""You are a financial advisor who specializes in physician finances. Your client is a brand-new attending cardiologist (just finished fellowship). He has:
- Large medical school student loans
- A wife and a 21-month-old son
- Just started earning an attending salary for the first time
- No prior financial education

Today's topic is: {topic} (Category: {category})

Write a clear, practical teaching note. No jargon without explanation. Use specific numbers and examples where possible. Assume he's smart but has never thought about this before.

Respond in exactly this format:

TOPIC: {topic}
CATEGORY: {category}

WHY IT MATTERS:
[2-3 sentences on why a new attending cardiologist should care about this RIGHT NOW]

HOW IT WORKS:
[Clear explanation in 4-6 sentences. Use a concrete example with real numbers where possible. If there are specific dollar amounts, thresholds, or deadlines, include them.]

WHAT TO DO:
[2-3 specific action steps. Be concrete — "log into X and do Y" not "consider reviewing your options"]

WATCH OUT FOR:
[1-2 common mistakes or traps related to this topic]

BOTTOM LINE:
[One sentence summary — the single most important takeaway]"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text


def generate_tip():
    prompt = """You are a financial advisor for a new attending physician with student loans and a young family.

Give ONE quick, specific, actionable financial tip he can do today or this week. Not a concept — an action. Something that takes less than 15 minutes.

Examples of good tips:
- "Log into studentaid.gov and check your PSLF qualifying payment count"
- "Check if your employer offers a 457(b) — call HR and ask"
- "Set up automatic transfers of $500/month to a high-yield savings account for your emergency fund"
- "Review your latest pay stub — make sure your 403(b) contribution is at least getting the full employer match"

Respond in exactly this format:

TIP: [The specific action in one sentence]
WHY: [One sentence on why this matters]
HOW LONG: [Time estimate, e.g. "5 minutes"]"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text


def generate_education():
    concept = generate_concept()
    tip = generate_tip()
    return {"concept": concept, "tip": tip}
