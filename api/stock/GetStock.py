import requests
import time
from datetime import datetime

WEBHOOK_URL = "https://discord.com/api/webhooks/1385901544368635924/ijZhDzqDtEfn_CSITawVYI2k7tGyWpue5xMVH3thYFwvtLAa4XzBIYHKL3ZVM3M59Zc2"

    # Lowercase role mapping for normalized matching
ROLE_PINGS = {
        # Gear
        "basic sprinkler": "<@&1385958249676800101>",
        "advanced sprinkler": "<@&1385958420125061130>",
        "godly sprinkler": "<@&1385958421358055465>",
        "master sprinkler": "<@&1385958422222082179>",
        "lightning rod": "<@&1385962333771268236>",
        # Seeds
        "bamboo": "<@&1385962627586330715>",
        "coconut": "<@&1385962669013598328>",
        "cactus": "<@&1385962669634486455>",
        "dragon fruit": "<@&1385962673518149732>",
        "mango": "<@&1385962673652371466>",
        "grape": "<@&1385962675116179526>",
        "mushroom": "<@&1385962678400454848>",
        "pepper": "<@&1385962679453093938>",
        "cacao": "<@&1385962680195481681>",
        "beanstalk": "<@&1385962680904585236>",
        "ember lily": "<@&1385962682066276525>",
        "sugar apple": "<@&1385962683249066115>",
        "carrot": "<@&1385964292742053898>",
        "strawberry": "<@&1385964292742053898>",
        "watermelon": "<@&1385964292742053898>",
        "blueberry": "<@&1385964292742053898>",
        "tomato": "<@&1385964292742053898>",
        "corn": "<@&1385964292742053898>",
        "orange tulip": "<@&1385964292742053898>",
        "daffodil": "<@&1385964292742053898>",
        "pumpkin": "<@&1385964292742053898>",
        "apple": "<@&1385964292742053898>"
    }

def fetch_stock():
        url = "https://grow-a-garden-api-6vnx.onrender.com/api/stock/GetStock"
        resp = requests.get(url)
        resp.raise_for_status()
        return resp.json()

def build_stock_message(stock):
        gear_lines = []
        seed_lines = []
        pings = []

        data = stock.get("Data", {})
        gear_list = data.get("gear", [])
        seed_list = data.get("seeds", [])

        print("DEBUG: Gear items:", [item.get("name") for item in gear_list])
        print("DEBUG: Seed items:", [item.get("name") for item in seed_list])

        for item in gear_list:
            name = item.get("name", "").strip()
            amount = int(item.get("stock", 0))
            normalized = name.lower()
            if amount > 0:
                gear_lines.append(f"[{amount}] {name}")
                if normalized in ROLE_PINGS:
                    pings.append(ROLE_PINGS[normalized])
                    print(f"DEBUG: Ping added for gear: {name}")

        for item in seed_list:
            name = item.get("name", "").strip()
            amount = int(item.get("stock", 0))
            normalized = name.lower()
            if amount > 0:
                seed_lines.append(f"[{amount}] {name}")
                if normalized in ROLE_PINGS:
                    pings.append(ROLE_PINGS[normalized])
                    print(f"DEBUG: Ping added for seed: {name}")

        embed = {
            "title": "GARDEN STOCKS UPDATE",
            "color": 0x00ff00,
            "fields": [
                {
                    "name": "⚙️ Gear Stock",
                    "value": "\n".join(gear_lines) if gear_lines else "No gear in stock.",
                    "inline": True
                },
                {
                    "name": "🌱 Seed Stock",
                    "value": "\n".join(seed_lines) if seed_lines else "No seeds in stock.",
                    "inline": True
                }
            ],
            "timestamp": datetime.now().isoformat(),
            "footer": {"text": "Last updated"}
        }

        payload = {"embeds": [embed]}
        if pings:
            payload["content"] = " ".join(sorted(set(pings)))

        return payload

def send_webhook(payload):
        resp = requests.post(WEBHOOK_URL, json=payload)
        resp.raise_for_status()

def wait_until_next_5min():
        now = datetime.now()
        next_minute = (now.minute // 5 + 1) * 5
        if next_minute == 60:
            next_time = now.replace(hour=(now.hour + 1) % 24, minute=0, second=0, microsecond=0)
        else:
            next_time = now.replace(minute=next_minute, second=0, microsecond=0)
        wait_seconds = (next_time - now).total_seconds()
        if wait_seconds < 0:
            wait_seconds += 300
        time.sleep(wait_seconds)

def main_loop():
        while True:
            try:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Waiting 30 seconds before fetching...")
                time.sleep(30)
                stock = fetch_stock()
                message = build_stock_message(stock)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Sending stock update...")
                send_webhook(message)
            except Exception as e:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Error: {e}")
            wait_until_next_5min()

if __name__ == '__main__':
        main_loop()
