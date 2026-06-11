def classify_email(email):
    sender = email.sender.lower()
    subject = email.subject.lower()
    snippet = email.snippet.lower()

    text = f"{sender} {subject} {snippet}"

    # 财务：必须非常严格
    if any(word in sender for word in ["cibc", "rbc", "td bank", "scotiabank", "bmo", "paypal", "google payments"]):
        return "财务", 5

    if any(word in text for word in ["bank statement", "credit card", "payment due", "账单", "付款", "发票", "租金", "房租"]):
        return "财务", 5

    # 学校
    if any(word in sender for word in ["university", "college", "carleton", "brightspace"]):
        return "学校", 5

    if any(word in text for word in ["assignment", "exam", "deadline", "due date", "midterm", "final exam", "作业", "考试", "截止"]):
        return "学校", 5

    # 安全：只认真正账号安全相关
    if any(word in sender for word in ["accounts.google.com", "no-reply@accounts.google.com", "security"]):
        return "安全", 5

    if any(word in text for word in ["password", "verification", "login", "sign-in", "two-step", "2-step", "privacy policy", "账号", "验证", "密码", "登录", "两步验证", "隐私政策"]):
        return "安全", 4

    # 学习/技术
    if any(word in sender for word in ["codecademy", "coursera", "ollama", "googleaistudio", "openai", "github"]):
        return "学习", 3

    if any(word in text for word in ["course", "learn", "tutorial", "model", "api", "python", "ai studio", "gemini", "学习", "课程"]):
        return "学习", 3

    # 广告/促销
    if any(word in sender for word in ["kfc", "stubhub", "lyft", "armani", "temu", "instagram", "bitget"]):
        return "广告", 1

    if any(word in text for word in ["sale", "off", "deal", "offer", "discount", "promo", "coupon", "优惠", "折扣", "促销", "幸运用户"]):
        return "广告", 1

    return "其他", 2