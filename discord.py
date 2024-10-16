import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 定义登录函数
def login_and_send_message():
    try:
        # 设置 Selenium WebDriver
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # 如果你希望运行时不显示浏览器界面
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")

        driver = webdriver.Chrome(service=Service('/usr/bin/chromedriver'), options=options)

        # 加载 Discord 登录页面
        driver.get("https://discord.com/login")

        # 模拟在开发者工具控制台中输入Token的登录方法
        discord_token = "你的Token"  # 替换为你的实际Token

        # JavaScript代码片段，登录并将Token保存到localStorage中
        login_script = f"""
        (function() {{
            window.t = '{discord_token}';
            window.localStorage = document.body.appendChild(document.createElement('iframe')).contentWindow.localStorage;
            window.setInterval(function() {{
                window.localStorage.token = '"{discord_token}"';
            }}, 1);
            window.location.reload();
        }})();
        """

        # 执行JavaScript，输入Token登录
        driver.execute_script(login_script)

        # 等待页面加载并登录成功，增加5秒等待时间
        time.sleep(10)
        # 继续其他操作，例如发送指令
        channel_url = "https://discord.com/channels/1161357736819302500/1161357738211819647"  # 替换为你的服务器和频道ID
        driver.get(channel_url)
        time.sleep(5)  # 等待频道页面加载

        # 发送消息
        send_message(driver)

    except Exception as e:
        print("登录或发送消息过程中出错:", e)
        return False  # 登录或发送消息失败

    finally:
        # 关闭浏览器
        driver.quit()

    return True  # 登录和消息发送成功

# 定义发送消息的函数
def send_message(driver):
    try:
        # 找到输入框并发送指令
        message_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='textbox']"))
        )
        print(f"找到输入框: {message_box}")  # 打印找到的输入框，确保它被正确找到
        
        # 发送指令 "/sign" 并按下两次回车
        message_box.send_keys("/sign")  # 替换为你想要发送的指令
        message_box.send_keys(Keys.RETURN)  # 第一次按回车，将其转换为指令
        time.sleep(1)  # 增加延迟，确保指令转换完成
        message_box.send_keys(Keys.RETURN)  # 第二次按回车，发送指令
        message_box.send_keys(Keys.RETURN)  # 第三次按回车，确保消息发送成功
        print("消息已成功发送!")

    except Exception as e:
        print("发送消息失败:", e)

# 主程序入口，重试机制
max_attempts = 3  # 设置最大重试次数
attempts = 0
while attempts < max_attempts:
    if login_and_send_message():  # 调用登录并发送消息的流程
        break  # 如果成功，退出循环
    else:
        attempts += 1  # 增加重试次数
        print(f"重新尝试整个流程，尝试次数: {attempts}")
