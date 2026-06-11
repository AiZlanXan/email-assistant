from collections import Counter

from app.classifier import classify_email


def generate_email_profile(emails):
    category_counter = Counter()
    sender_counter = Counter()

    for email in emails:
        category, importance = classify_email(email)
        category_counter[category] += 1
        sender_counter[email.sender] += 1

    print("\n📊 邮箱画像")
    print("=" * 50)

    print("\n分类分布：")
    for category, count in category_counter.most_common():
        print(f"- {category}: {count} 封")

    print("\n最常见发件人：")
    for sender, count in sender_counter.most_common(10):
        print(f"- {sender}: {count} 封")

    print("=" * 50)