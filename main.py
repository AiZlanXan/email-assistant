import schedule
import time

from app.sync_service import sync_emails, full_sync
from app.database import init_db, has_emails


def main():
    init_db()

    if has_emails():
        print("检测到数据库已有历史邮件，执行增量同步...")
        sync_emails(max_results=20)
    else:
        print("数据库为空，第一次启动，执行全量同步...")
        full_sync(max_results=3000)

    schedule.every(10).minutes.do(sync_emails, max_results=20)

    print("Email Assistant 正在后台运行...")
    print("每 10 分钟自动同步一次。")
    print("每次同步后会自动更新日报、月报、半年报和年报。")
    print("按 Ctrl + C 停止程序。")

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()