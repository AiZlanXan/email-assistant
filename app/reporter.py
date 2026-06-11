from datetime import datetime


def generate_report(categories):
    lines = []

    lines.append("=" * 50)
    lines.append("📬 今日重要邮件报告")
    lines.append("=" * 50)

    important_categories = ["学校", "财务", "安全"]
    important_count = 0

    for category in important_categories:
        important_count += len(categories.get(category, []))

    lines.append("")
    lines.append(f"🔥 重要邮件：{important_count} 封")

    if important_count == 0:
        lines.append("今天暂时没有重要邮件。")
    else:
        for category in important_categories:
            emails = categories.get(category, [])

            if emails:
                lines.append("")
                lines.append(f"【{category}】")

                for email in emails:
                    lines.append(f"- {email.subject}")
                    lines.append(f"  From: {email.sender}")
                    lines.append(f"  Snippet: {email.snippet[:100]}")

    low_priority_count = 0

    for category, emails in categories.items():
        if category not in important_categories:
            low_priority_count += len(emails)

    lines.append("")
    lines.append(f"🟢 低优先级邮件：{low_priority_count} 封")
    lines.append("")
    lines.append("=" * 50)

    report_text = "\n".join(lines)

    print(report_text)

    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"report_{now}.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(report_text)

    print(f"\n报告已保存：{filename}")