def generate_report(categories):
    print("\n" + "=" * 50)
    print("📬 今日重要邮件报告")
    print("=" * 50)

    important_categories = ["学校", "财务", "安全"]

    important_count = 0

    for category in important_categories:
        important_count += len(categories.get(category, []))

    print(f"\n🔥 重要邮件：{important_count} 封")

    if important_count == 0:
        print("今天暂时没有重要邮件。")
    else:
        for category in important_categories:
            emails = categories.get(category, [])

            if emails:
                print(f"\n【{category}】")
                for email in emails:
                    print(f"- {email.subject}")
                    print(f"  From: {email.sender}")
                    print(f"  Snippet: {email.snippet[:100]}")

    low_priority_count = 0

    for category, emails in categories.items():
        if category not in important_categories:
            low_priority_count += len(emails)

    print(f"\n🟢 低优先级邮件：{low_priority_count} 封")

    print("\n" + "=" * 50)