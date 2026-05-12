import os
import time
import threading
import browser_cookie3

COOKIE_FILE = "cookies.txt"

REFRESH_INTERVAL = 6 * 60 * 60  # 6 hours


class CookieManager:
    def __init__(self, cookie_file=COOKIE_FILE):
        self.cookie_file = cookie_file
        self.running = False

    def export_cookies(self):
        """
        Export YouTube cookies from browser into Netscape format
        """
        try:
            cj = browser_cookie3.chrome(domain_name="youtube.com")

            with open(self.cookie_file, "w", encoding="utf-8") as f:
                f.write("# Netscape HTTP Cookie File\n")

                for cookie in cj:
                    f.write(
                        f"{cookie.domain}\t"
                        f"TRUE\t"
                        f"{cookie.path}\t"
                        f"FALSE\t"
                        f"{int(cookie.expires) if cookie.expires else 0}\t"
                        f"{cookie.name}\t"
                        f"{cookie.value}\n"
                    )

            print("[CookieManager] ✅ Cookies updated successfully")

        except Exception as e:
            print("[CookieManager] ❌ Failed to export cookies:", e)

    def start_auto_refresh(self, interval=REFRESH_INTERVAL):
        """
        Runs cookie refresh in background thread
        """
        if self.running:
            return

        self.running = True

        def loop():
            while self.running:
                self.export_cookies()
                time.sleep(interval)

        thread = threading.Thread(target=loop, daemon=True)
        thread.start()

        print("[CookieManager] 🔁 Auto cookie refresh started")

    def stop(self):
        self.running = False
