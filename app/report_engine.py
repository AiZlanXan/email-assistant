import os
from collections import defaultdict
from datetime import datetime

from app.database import get_all_emails
from app.classifier import classify_email


def group_emails_by_date(emails):
    grouped = defaultdict(list)

    for email in emails:
        if not email.received_at:
            continue

        date_key = email.received_at[:10]
        grouped[date_key].append(email)

    return grouped


def group_emails_by_month(emails):
    grouped = defaultdict(list)

    for email in emails:
        if not email.received_at:
            continue

        month_key = email.received_at[:7]
        grouped[month_key].append(email)

    return grouped


def group_emails_by_year(emails):
    grouped = defaultdict(list)

    for email in emails:
        if not email.received_at:
            continue

        year_key = email.received_at[:4]
        grouped[year_key].append(email)

    return grouped


def build_category_stats(emails):
    stats = defaultdict(int)

    for email in emails:
        category, importance = classify_email(email)
        stats[category] += 1

    return stats


def write_file(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        file.write(text)


def generate_daily_report(date_key, emails):
    year = date_key[:4]
    month = date_key[5:7]

    stats = build_category_stats(emails)

    lines = []
    lines.append(f"# {date_key} 日报")
    lines.append("")
    lines.append(f"邮件总数：{len(emails)}")
    lines.append("")
    lines.append("## 分类统计")
    lines.append("")

    for category, count in sorted(stats.items()):
        lines.append(f"- {category}: {count} 封")

    lines.append("")
    lines.append("## 重要邮件")
    lines.append("")

    important_categories = ["学校", "财务", "安全"]
    has_important = False

    for email in emails:
        category, importance = classify_email(email)

        if category in important_categories:
            has_important = True
            lines.append(f"- **{email.subject}**")
            lines.append(f"  - From: {email.sender}")
            lines.append(f"  - Time: {email.received_at}")
            lines.append(f"  - Category: {category}")
            lines.append("")

    if not has_important:
        lines.append("今日暂无重要邮件。")

    path = os.path.join("reports", year, month, f"{date_key}.md")
    write_file(path, "\n".join(lines))


def generate_monthly_report(month_key, emails):
    year = month_key[:4]
    month = month_key[5:7]

    stats = build_category_stats(emails)

    lines = []
    lines.append(f"# {month_key} 月度邮件总结")
    lines.append("")
    lines.append(f"邮件总数：{len(emails)}")
    lines.append("")
    lines.append("## 分类统计")
    lines.append("")

    for category, count in sorted(stats.items()):
        lines.append(f"- {category}: {count} 封")

    lines.append("")
    lines.append("## 重要邮件摘要")
    lines.append("")

    important_categories = ["学校", "财务", "安全"]
    has_important = False

    for email in emails:
        category, importance = classify_email(email)

        if category in important_categories:
            has_important = True
            lines.append(f"- **{email.subject}**")
            lines.append(f"  - From: {email.sender}")
            lines.append(f"  - Date: {email.received_at}")
            lines.append(f"  - Category: {category}")
            lines.append("")

    if not has_important:
        lines.append("本月暂无重要邮件。")

    path = os.path.join("reports", year, month, "monthly_summary.md")
    write_file(path, "\n".join(lines))


def generate_half_year_report(year, half_name, emails):
    stats = build_category_stats(emails)

    lines = []
    lines.append(f"# {year} {half_name} 半年邮件总结")
    lines.append("")
    lines.append(f"邮件总数：{len(emails)}")
    lines.append("")
    lines.append("## 分类统计")
    lines.append("")

    for category, count in sorted(stats.items()):
        lines.append(f"- {category}: {count} 封")

    path = os.path.join("reports", year, "half_year", f"{year}_{half_name}.md")
    write_file(path, "\n".join(lines))


def generate_yearly_report(year, emails):
    stats = build_category_stats(emails)

    lines = []
    lines.append(f"# {year} 年度邮件总结")
    lines.append("")
    lines.append(f"邮件总数：{len(emails)}")
    lines.append("")
    lines.append("## 分类统计")
    lines.append("")

    for category, count in sorted(stats.items()):
        lines.append(f"- {category}: {count} 封")

    path = os.path.join("reports", year, "yearly", f"{year}.md")
    write_file(path, "\n".join(lines))


def generate_all_reports():
    emails = get_all_emails()

    print(f"开始生成历史报告，共 {len(emails)} 封邮件...")

    by_date = group_emails_by_date(emails)
    by_month = group_emails_by_month(emails)
    by_year = group_emails_by_year(emails)

    for date_key, items in by_date.items():
        generate_daily_report(date_key, items)

    for month_key, items in by_month.items():
        generate_monthly_report(month_key, items)

    for year, items in by_year.items():
        h1 = []
        h2 = []

        for email in items:
            month = int(email.received_at[5:7])

            if month <= 6:
                h1.append(email)
            else:
                h2.append(email)

        if h1:
            generate_half_year_report(year, "H1", h1)

        if h2:
            generate_half_year_report(year, "H2", h2)

        generate_yearly_report(year, items)

    print("所有历史报告生成完成。")


def update_current_reports():
    emails = get_all_emails()

    now = datetime.now()
    today_key = now.strftime("%Y-%m-%d")
    month_key = now.strftime("%Y-%m")
    year_key = now.strftime("%Y")

    today_emails = []
    month_emails = []
    year_emails = []
    half_year_emails = []

    current_month = now.month

    if current_month <= 6:
        half_name = "H1"
        half_months = [1, 2, 3, 4, 5, 6]
    else:
        half_name = "H2"
        half_months = [7, 8, 9, 10, 11, 12]

    for email in emails:
        if not email.received_at:
            continue

        email_date = email.received_at[:10]
        email_month = email.received_at[:7]
        email_year = email.received_at[:4]
        email_month_number = int(email.received_at[5:7])

        if email_date == today_key:
            today_emails.append(email)

        if email_month == month_key:
            month_emails.append(email)

        if email_year == year_key:
            year_emails.append(email)

        if email_year == year_key and email_month_number in half_months:
            half_year_emails.append(email)

    generate_daily_report(today_key, today_emails)
    generate_monthly_report(month_key, month_emails)
    generate_half_year_report(year_key, half_name, half_year_emails)
    generate_yearly_report(year_key, year_emails)

    print("当前日报、月报、半年报、年报已更新。")