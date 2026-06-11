import os
from datetime import datetime

from app.classifier import classify_email


def generate_monthly_summary(emails, year, month):
    categories = {}

    for email in emails:
        category, importance = classify_email(email)

        if category not in categories:
            categories[category] = []

        categories[category].append(email)

    lines = []

    lines.append(f"# {year}-{month:02d} 月度邮件总结")
    lines.append("")
    lines.append(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append(f"本月邮件总数：{len(emails)}")
    lines.append("")

    lines.append("## 分类统计")
    lines.append("")

    for category, items in categories.items():
        lines.append(f"- {category}: {len(items)} 封")

    lines.append("")
    lines.append("## 重要邮件")
    lines.append("")

    important_categories = ["学校", "财务", "安全"]

    has_important = False

    for category in important_categories:
        items = categories.get(category, [])

        if items:
            has_important = True
            lines.append(f"### {category}")
            lines.append("")

            for email in items:
                lines.append(f"- **{email.subject}**")
                lines.append(f"  - From: {email.sender}")
                lines.append(f"  - Date: {email.date}")
                lines.append("")

    if not has_important:
        lines.append("本月暂无重要邮件。")

    report_text = "\n".join(lines)

    folder_path = os.path.join("reports", str(year), f"{month:02d}")
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, "monthly_summary.md")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(report_text)

    print(f"月度总结已保存：{file_path}")