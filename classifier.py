def classify_email(email):
    text = f"{email.sender} {email.subject} {email.snippet}".lower()

    if any(word in text for word in ["google", "security", "verification", "privacy", "password", "账号", "验证", "隐私"]):
        return "安全"

    if any(word in text for word in ["codecademy", "ollama", "course", "learn", "pro", "学习", "课程"]):
        return "学习"

    if any(word in text for word in ["kfc", "sale", "off", "deal", "offer", "discount", "promo", "优惠"]):
        return "广告"

    if any(word in text for word in ["bank", "cibc", "payment", "bill", "rent", "invoice", "账单", "付款", "房租"]):
        return "财务"

    if any(word in text for word in ["assignment", "exam", "university", "college", "deadline", "due", "作业", "考试", "截止"]):
        return "学校"

    return "其他"