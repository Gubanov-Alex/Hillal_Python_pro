import queue
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
import threading



OrderRequestBody = tuple[str, datetime]


class Scheduler:
    def __init__(self):
        self.orders: queue.PriorityQueue = queue.PriorityQueue()

    def add_order(self, order: OrderRequestBody):
        self.orders.put((order[1], order))
        print(f"ORDER {order[0]} IS SCHEDULED")

    def process_orders(self):
        print("SCHEDULER PROCESSING...")
        while True:
            try:
                priority, order = self.orders.get(timeout=0.5)
                time_to_wait = (priority - datetime.now()).total_seconds()

                if time_to_wait > 0:
                    self.orders.put((priority, order))
                    time.sleep(0.5)
                else:
                    print(f"\n{order[0]} SENT TO SHIPPING DEPARTMENT")
            except queue.Empty:
                continue

def main():
    scheduler = Scheduler()
    thread = threading.Thread(target=scheduler.process_orders, daemon=True)
    thread.start()

    try:
        while True:
            if order_details := input("Enter order details: "):
                try:
                    # Разбираем входные данные.
                    data = order_details.split(" ")
                    order_name, delay = data[0], int(data[1])

                    # Добавляем заказ с вычисленным временем выполнения.
                    scheduler.add_order(
                        (
                            order_name,  # Строка с именем заказа.
                            datetime.now() + timedelta(seconds=delay),  # Время выполнения.
                        )
                    )
                except (ValueError, IndexError):
                    print("Invalid input. Please use the format: <order_name> <delay_in_seconds>")
    except KeyboardInterrupt:
        print("\nExiting...")
        raise SystemExit(0)



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        raise SystemExit(0)
