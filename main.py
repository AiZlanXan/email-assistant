import schedule
import time

from app.sync_service import sync_emails


def main():
    sync_emails(max_results=10)

    schedule.every(10).minutes.do(sync_emails, max_results=10)

    print("Email Assistant 正在后台运行...")
    print("每 10 分钟自动同步一次。")
    print("按 Ctrl + C 停止程序。")

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()