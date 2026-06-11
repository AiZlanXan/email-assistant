import schedule
import time
from datetime import datetime

from app.sync_service import sync_emails, full_sync
from app.database import init_db, has_emails, get_emails_by_month
from app.monthly_reporter import generate_monthly_summary


def generate_current_month_summary():
    now = datetime.now()
    emails = get_emails_by_month(now.year, now.month)
    generate_monthly_summary(emails, now.year, now.month)


def main():
    init_db()

    if has_emails():
        print("检测到数据库已有历史邮件，执行增量同步...")
        sync_emails(max_results=20)
    else:
        print("数据库为空，第一次启动，执行全量同步...")
        full_sync(max_results=500)

    generate_current_month_summary()

    schedule.every(10).minutes.do(sync_emails, max_results=20)
    schedule.every().day.at("23:59").do(generate_current_month_summary)

    print("Email Assistant 正在后台运行...")
    print("每 10 分钟自动同步一次。")
    print("每天 23:59 自动生成月度总结。")
    print("按 Ctrl + C 停止程序。")

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()