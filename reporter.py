def generate_report(categories):
    print("\n" + "=" * 50)
    print("📬 今日邮件总结")
    print("=" * 50)

    important_categories = ["学校", "财务", "安全"]

    important_count = 0
    for category in important_categories:
        important_count += len(categories.get(category, []))

    print(f"\n🔥 重要邮件：{important_count} 封")

    for category in important_categories:
        emails = categories.get(category, [])

        if emails:
            print(f"\n【{category}】")
            for email in emails:
                print(f"- {email.subject}")

    other_count = 0
    for category, emails in categories.items():
        if category not in important_categories:
            other_count += len(emails)

    print(f"\n🟢 普通/低优先级邮件：{other_count} 封")

    for category, emails in categories.items():
        if category not in important_categories:
            print(f"\n【{category}】")
            for email in emails:
                print(f"- {email.subject}")

    print("\n" + "=" * 50)