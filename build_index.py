#!/usr/bin/env python3
"""Builds index.html from index.template.html by scanning the week folders.
Runs automatically on GitHub after every upload. No installs needed."""
import json, re, html, pathlib, sys

ROOT = pathlib.Path(__file__).parent

WEEKS = [
    ("week-01-intro-and-data-cleaning", "Sessions 1-2", "Introduction and data cleaning", ["Data cleaning", "Feature engineering"]),
    ("week-02-workforce-planning-and-branding", "Sessions 3-4", "Workforce planning and employer branding", ["Forecasting", "Clustering", "Text mining"]),
    ("week-03-attraction-and-acquisition", "Sessions 5-6", "Talent attraction and acquisition", ["Regression", "Logistic regression", "Bagging and boosting"]),
    ("week-04-onboarding-and-ld", "Sessions 7-8", "Onboarding and learning and development", ["Decision trees", "Random forests", "Clustering"]),
    ("week-05-engagement-and-performance", "Sessions 9-10", "Engagement and performance management", ["Regression", "Boosting"]),
    ("week-06-mobility-and-succession", "Sessions 11-12", "Internal mobility and succession planning", ["Social network analysis", "Survival analysis"]),
    ("week-07-compensation-and-attrition-i", "Sessions 13-14", "Compensation and attrition prediction", ["Factor analysis", "Classification", "Ensembles"]),
    ("week-08-attrition-ii-and-alumni", "Sessions 15-16", "Attrition diagnosis and alumni rehiring", ["Attrition patterns", "Social network analysis"]),
    ("week-09-dei-and-ethics", "Sessions 17-18", "DEI, pay equity and ethics", ["Adverse impact", "Statistical parity", "Governance"]),
    ("week-10-genai-and-project", "Sessions 19-20", "Generative AI and the group project", ["GenAI", "Agentic AI", "Neural networks"]),
]
EXTRAS = "extras"

def read_meta(path):
    text = path.read_text(encoding="utf-8", errors="ignore")[:20000]
    t = re.search(r"<title[^>]*>(.*?)</title>", text, re.I | re.S)
    d = re.search(r'<meta[^>]+name=["\']description["\'][^>]*>', text, re.I)
    desc = ""
    if d:
        c = re.search(r'content=["\'](.*?)["\']', d.group(0), re.I | re.S)
        desc = c.group(1) if c else ""
    title = html.unescape(t.group(1)).strip() if t else ""
    if not title:
        title = path.stem.replace("-", " ").replace("_", " ").strip().title()
    return title, html.unescape(desc).strip()

def scan(folder):
    base = ROOT / folder
    if not base.is_dir():
        return []
    files = sorted(p for p in base.glob("*.html"))
    files += sorted(p for p in base.glob("*/index.html"))
    sims = []
    for p in files:
        title, desc = read_meta(p)
        sims.append({"path": p.relative_to(ROOT).as_posix(), "title": title, "desc": desc})
    return sims

if "--init" in sys.argv:
    # Creates any missing week folders (each with a small README so Git keeps them).
    for folder in [w[0] for w in WEEKS] + [EXTRAS]:
        d = ROOT / folder
        d.mkdir(exist_ok=True)
        if not (d / "README.md").exists():
            (d / "README.md").write_text("Upload simulations for this week here (.html files).\n", encoding="utf-8")
    print("Week folders ready")
    sys.exit(0)

data = {
    "weeks": [
        {"n": i + 1, "folder": f, "sessions": s, "title": t, "tags": tags, "sims": scan(f)}
        for i, (f, s, t, tags) in enumerate(WEEKS)
    ],
    "extras": scan(EXTRAS),
}
tpl = (ROOT / "index.template.html").read_text(encoding="utf-8")
payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
(ROOT / "index.html").write_text(tpl.replace("/*__DATA__*/null", payload), encoding="utf-8")
live = sum(1 for w in data["weeks"] if w["sims"])
print(f"index.html built: {live} of {len(WEEKS)} weeks live, {len(data['extras'])} extras")
