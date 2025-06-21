import requests
import time
from datetime import datetime, timedelta

WEBHOOK_URL = "https://discord.com/api/webhooks/1385853687913775167/l2VFooeLlmaVmwpjZASipJRt03JAdoAk0HMZe9HwTcx2r-179FAjNgJ38nu1ay9mQ9Ws"



def fetch_stock():
                                    url = "https://growagardenapi.vercel.app/api/stock/GetStock"
                                    resp = requests.get(url)
                                    resp.raise_for_status()
                                    data = resp.json()
                                    print(f"DEBUG: API Response: {data}")
                                    return data

def build_stock_message(stock):
                                gear_lines = []
                                seed_lines = []

                                # Extract the actual data from the API response
                                data = stock.get("Data", {})
                                gear_list = data.get("gear", [])
                                seed_list = data.get("seeds", [])

                                print(f"DEBUG: Processing gear_list: {gear_list}")
                                print(f"DEBUG: Processing seed_list: {seed_list}")

                                # Process gear items
                                for item in gear_list:
                                    name = item.get("name")
                                    amount = int(item.get("stock", 0))  # Convert string to int
                                    print(f"DEBUG: Gear - Name: '{name}', Amount: {amount}")

                                    if amount > 0:
                                        gear_lines.append(f"[{amount}] {name}")
                                        print(f"DEBUG: Added gear: {name}")

                                # Process seed items
                                for item in seed_list:
                                    name = item.get("name")
                                    amount = int(item.get("stock", 0))  # Convert string to int
                                    print(f"DEBUG: Seed - Name: '{name}', Amount: {amount}")

                                    if amount > 0:
                                        seed_lines.append(f"[{amount}] {name}")
                                        print(f"DEBUG: Added seed: {name}")

                                msg = "__**GEAR STOCK**__\n"
                                msg += "\n".join(gear_lines) if gear_lines else "No gear in stock."
                                msg += "\n__**SEED STOCK**__\n"
                                msg += "\n".join(seed_lines) if seed_lines else "No seeds in stock."
                                return msg

def send_webhook(message):
                                    data = {"content": message}
                                    resp = requests.post(WEBHOOK_URL, json=data)
                                    resp.raise_for_status()

def wait_until_next_5min():
                                    now = datetime.now()
                                    # Calculate minutes to next 5-minute mark
                                    next_minute = (now.minute // 5 + 1) * 5
                                    if next_minute == 60:
                                        next_time = now.replace(hour=(now.hour + 1) % 24, minute=0, second=0, microsecond=0)
                                    else:
                                        next_time = now.replace(minute=next_minute, second=0, microsecond=0)
                                    wait_seconds = (next_time - now).total_seconds()
                                    if wait_seconds < 0:
                                        wait_seconds += 300  # fallback
                                    time.sleep(wait_seconds)

def main_loop():
                                    while True:
                                        try:
                                            stock = fetch_stock()
                                            message = build_stock_message(stock)
                                            print(f"[{datetime.now().strftime('%H:%M:%S')}] Sent stock update.")
                                            print(message)
                                            send_webhook(message)
                                        except Exception as e:
                                            print(f"Error: {e}")
                                        wait_until_next_5min()

if __name__ == '__main__':
                                main_loop()
