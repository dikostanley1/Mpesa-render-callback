import os
import requests
import sys

def setup_webhook():
    # 1. Get Token from environment
    bot_token = os.environ.get("BOT_TOKEN")
    if not bot_token:
        print("ERROR: BOT_TOKEN environment variable is not set.")
        sys.exit(1)

    base_url = f"https://api.telegram.org/bot{bot_token}"
    webhook_url = "https://mpesa-render-callback-sd8x.onrender.com/telegram"

    print(f"--- Telegram Webhook Setup ---")
    
    # 2. Validate Bot Token using getMe
    try:
        response = requests.get(f"{base_url}/getMe")
        res_data = response.json()
        
        if not res_data.get("ok"):
            print(f"ERROR: Invalid Bot Token. Telegram API returned: {res_data.get('description')}")
            sys.exit(1)
        
        bot_info = res_data.get("result")
        print(f"SUCCESS: Connected to bot @{bot_info.get('username')} ({bot_info.get('first_name')})")

    except Exception as e:
        print(f"ERROR: Failed to connect to Telegram API: {e}")
        sys.exit(1)

    # 3. Check current Webhook Info
    try:
        wh_info_res = requests.get(f"{base_url}/getWebhookInfo")
        wh_data = wh_info_res.json()
        
        if wh_data.get("ok"):
            current_url = wh_data.get("result", {}).get("url")
            print(f"INFO: Current Webhook URL: '{current_url}'")
            
            if current_url == webhook_url:
                print("SUCCESS: Webhook is already correctly set.")
                return
        else:
            print(f"WARNING: Could not retrieve webhook info: {wh_data.get('description')}")

    except Exception as e:
        print(f"WARNING: error checking webhook info: {e}")

    # 4. Set the Webhook
    print(f"ACTION: Setting webhook to {webhook_url}...")
    try:
        set_wh_res = requests.post(f"{base_url}/setWebhook", json={"url": webhook_url})
        set_data = set_wh_res.json()
        
        if set_data.get("ok"):
            print("SUCCESS: Webhook set successfully!")
        else:
            print(f"ERROR: Failed to set webhook. Telegram API returned: {set_data.get('description')}")
            sys.exit(1)

    except Exception as e:
        print(f"ERROR: Failed to call setWebhook: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_webhook()
