import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

CONCEPT_LABELS = [
    "WHY IT MATTERS", "HOW IT WORKS", "WHAT TO DO",
    "WATCH OUT FOR", "BOTTOM LINE"
]

def get_header():
    today = datetime.now().strftime("%b %d, %Y")
    return f'''
    <div style="background:#0a1628;border-radius:12px;margin-bottom:24px;overflow:hidden">
      <div style="height:4px;background:#10b981"></div>
      <table width="100%" cellpadding="0" cellspacing="0" style="padding:20px 28px">
        <tr>
          <td width="56" valign="middle">
            <table cellpadding="0" cellspacing="0">
              <tr>
                <td align="center" valign="middle" width="52" height="52"
                    style="background:#1a2540;border-radius:50%;border:2px solid #10b981">
                  <span style="font-size:22px;line-height:1">&#128176;</span>
                </td>
              </tr>
            </table>
          </td>
          <td width="16"></td>
          <td valign="middle" style="padding-right:20px;border-right:1px solid rgba(16,185,129,0.2)">
            <div style="font-family:-apple-system,BlinkMacSystemFont,sans-serif;
                        font-size:10px;font-weight:600;color:#10b981;letter-spacing:4px;
                        line-height:1;margin-bottom:4px">MORNING</div>
            <div style="font-family:-apple-system,BlinkMacSystemFont,sans-serif;
                        font-size:28px;font-weight:700;color:#ffffff;line-height:1">Money</div>
          </td>
          <td width="20"></td>
          <td valign="middle">
            <div style="font-family:-apple-system,sans-serif;font-size:11px;
                        color:#94a3b8;margin-bottom:8px">
              Physician finance &middot; Daily concept &middot; Actionable tips
            </div>
          </td>
          <td width="16"></td>
          <td valign="middle" align="right" style="white-space:nowrap">
            <span style="font-family:-apple-system,sans-serif;font-size:10px;
                         color:#64748b;background:#1a2540;padding:4px 12px;
                         border-radius:10px">{today}</span>
          </td>
        </tr>
      </table>
    </div>'''


def build_concept_html(concept_text):
    lines = concept_text.strip().split("\n")
    body = ""
    title = "Finance Concept"
    category = ""

    for line in lines:
        line = line.strip()
        if not line:
            body += '<div style="margin:5px 0"></div>'
            continue
        if line.startswith("TOPIC:"):
            title = line.replace("TOPIC:", "").strip()
        elif line.startswith("CATEGORY:"):
            category = line.replace("CATEGORY:", "").strip()
        elif line.startswith("BOTTOM LINE:"):
            rest = line.replace("BOTTOM LINE:", "").strip()
            body += f'<p style="margin:14px 0 0;font-size:14px;color:#065f46;font-weight:600;background:#d1fae5;padding:10px 12px;border-radius:6px">&#128161; BOTTOM LINE: {rest}</p>'
        else:
            matched = False
            for label in CONCEPT_LABELS:
                if line.startswith(f"{label}:"):
                    rest = line.replace(f"{label}:", "").strip()
                    body += f'<p style="margin:14px 0 4px;font-size:12px;font-weight:700;color:#059669;text-transform:uppercase;letter-spacing:0.08em;border-bottom:1px solid #e5e7eb;padding-bottom:4px">{label}</p>'
                    if rest:
                        body += f'<p style="margin:4px 0 8px;font-size:14px;color:#374151;line-height:1.7">{rest}</p>'
                    matched = True
                    break
            if not matched:
                body += f'<p style="margin:2px 0;font-size:14px;color:#374151;line-height:1.7">{line}</p>'

    category_badge = ""
    if category:
        category_badge = f'<span style="background:#dbeafe;color:#1e40af;font-size:11px;font-weight:600;padding:3px 10px;border-radius:20px;margin-left:8px">{category}</span>'

    return f"""
    <div style="background:#ffffff;border:1px solid #e5e7eb;border-radius:10px;
                padding:20px 24px;margin-bottom:20px">
      <div style="margin-bottom:12px">
        <span style="background:#d1fae5;color:#065f46;font-size:12px;font-weight:600;
                     padding:3px 10px;border-radius:20px">&#128218; Concept of the Day</span>
        {category_badge}
      </div>
      <h2 style="margin:0 0 16px;font-size:17px;color:#111827;line-height:1.4">{title}</h2>
      <div style="background:#f9fafb;border-radius:8px;padding:16px 18px">
        {body}
      </div>
    </div>"""


def build_tip_html(tip_text):
    lines = tip_text.strip().split("\n")
    tip = ""
    why = ""
    how_long = ""

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("TIP:"):
            tip = line.replace("TIP:", "").strip()
        elif line.startswith("WHY:"):
            why = line.replace("WHY:", "").strip()
        elif line.startswith("HOW LONG:"):
            how_long = line.replace("HOW LONG:", "").strip()

    time_badge = ""
    if how_long:
        time_badge = f'<span style="background:#fef3c7;color:#92400e;font-size:11px;font-weight:600;padding:3px 10px;border-radius:20px;margin-left:8px">{how_long}</span>'

    return f"""
    <div style="background:#ffffff;border:1px solid #e5e7eb;border-radius:10px;
                padding:20px 24px;margin-bottom:20px">
      <div style="margin-bottom:12px">
        <span style="background:#fef3c7;color:#92400e;font-size:12px;font-weight:600;
                     padding:3px 10px;border-radius:20px">&#9889; Quick Action</span>
        {time_badge}
      </div>
      <p style="margin:0 0 8px;font-size:15px;color:#111827;font-weight:600;line-height:1.5">{tip}</p>
      <p style="margin:0;font-size:13px;color:#6b7280;line-height:1.5">{why}</p>
    </div>"""


def build_article_html(article):
    if not article:
        return ""

    summary = article.get("abstract", "")
    if len(summary) > 300:
        summary = summary[:300].rsplit(" ", 1)[0] + "..."

    return f"""
    <div style="background:#ffffff;border:1px solid #e5e7eb;border-radius:10px;
                padding:20px 24px;margin-bottom:20px">
      <div style="margin-bottom:12px">
        <span style="background:#ede9fe;color:#5b21b6;font-size:12px;font-weight:600;
                     padding:3px 10px;border-radius:20px">&#128240; Top Read</span>
        <span style="background:#f0fdf4;color:#166534;font-size:11px;
                     padding:3px 10px;border-radius:20px;margin-left:6px">{article.get('source', '')}</span>
      </div>
      <h2 style="margin:0 0 8px;font-size:16px;color:#111827;line-height:1.4">
        {article['title']}
      </h2>
      <p style="margin:0 0 14px;font-size:13px;color:#6b7280;line-height:1.5">{summary}</p>
      <a href="{article['url']}"
         style="display:inline-block;font-size:13px;color:#059669;
                text-decoration:none;font-weight:500">
        Read full article &#8594;
      </a>
    </div>"""


def build_html_email(article, education):
    header = get_header()
    concept_html = build_concept_html(education.get("concept", ""))
    tip_html = build_tip_html(education.get("tip", ""))
    article_html = build_article_html(article)

    html = f"""
    <!DOCTYPE html>
    <html>
    <body style="margin:0;padding:0;background:#f3f4f6;font-family:-apple-system,sans-serif">
      <div style="max-width:640px;margin:0 auto;padding:24px 16px">
        {header}
        {concept_html}
        {tip_html}
        {article_html}
        <div style="text-align:center;padding:20px;color:#9ca3af;font-size:12px">
          <p style="margin:0">Morning Money &mdash; Physician finance, one day at a time</p>
          <p style="margin:4px 0 0">AI-generated &mdash; not financial advice, always consult a professional</p>
        </div>
      </div>
    </body>
    </html>"""

    return html


def send_digest(article, education):
    html_content = build_html_email(article, education)
    today = datetime.now().strftime("%B %d, %Y")

    sender = os.getenv("SENDER_EMAIL")
    recipient = os.getenv("RECIPIENT_EMAIL")
    app_password = os.getenv("GMAIL_APP_PASSWORD")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Morning Money \u2014 {today}"
    msg["From"] = f"Morning Money <{sender}>"
    msg["To"] = recipient
    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, app_password)
            server.sendmail(sender, recipient, msg.as_string())
        print("Email sent successfully via Gmail!")
        return True
    except Exception as e:
        print(f"Email failed: {e}")
        return False
