import queue
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
import threading

ORDER_INPUT_ERROR = "Invalid input. Please use the format: <order_name> <delay_in_seconds>"


@dataclass(order=True)
class Order:
    scheduled_time: datetime
    name: str


class Scheduler:
    def __init__(self):
        self.orders: queue.PriorityQueue[Order] = queue.PriorityQueue()

    def schedule_order(self, order: Order):
        """Adds an order to the scheduling queue."""
        self.orders.put(order)
        print(f"ORDER {order.name} IS SCHEDULED")

    def _process_order(self, order: Order):
        """Handles whether an order is ready for processing or needs to wait."""
        time_to_wait = (order.scheduled_time - datetime.now()).total_seconds()
        if time_to_wait > 0:
            self.orders.put(order)
            time.sleep(0.5)
        else:
            print(f"\n{order.name} SENT TO SHIPPING DEPARTMENT")

    def process_orders(self):
        """Processes orders from the queue."""
        print("SCHEDULER PROCESSING...")
        while True:
            try:
                order = self.orders.get(timeout=0.5)
                self._process_order(order)
            except queue.Empty:
                continue


def parse_order_input(order_details: str) -> Order:
    """Parses user input and creates an Order object."""
    data = order_details.split(" ")
    order_name, delay = data[0], int(data[1])
    return Order(
        scheduled_time=datetime.now() + timedelta(seconds=delay),
        name=order_name,
    )


def main():
    scheduler = Scheduler()
    thread = threading.Thread(target=scheduler.process_orders, daemon=True)
    thread.start()
    try:
        while True:
            if order_details := input("Enter order details: "):
                try:
                    order = parse_order_input(order_details)
                    scheduler.schedule_order(order)
                except (ValueError, IndexError):
                    print(ORDER_INPUT_ERROR)
    except KeyboardInterrupt:
        print("\nExiting...")
        raise SystemExit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        raise SystemExit(0)
