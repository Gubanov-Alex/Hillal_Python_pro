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
        self.lock = threading.Lock()  # Lock for thread-safe access to the queue
        self.order_event = threading.Event()  # Event to notify when a new order is added
        self.running = True  # Flag to control the scheduler's running state

    def schedule_order(self, order: Order):
        """Add an order to the queue and notify the handler."""
        with self.lock:
            self.orders.put(order)
        print(f"ORDER {order.name} IS SCHEDULED")
        self.order_event.set()  # Notify the thread about a new order

    def _process_order(self, order: Order):
        """
        Process an order: if the time has not come yet, wait;
        otherwise, send the order to the shipping department.
        """
        time_to_wait = (order.scheduled_time - datetime.now()).total_seconds()
        if time_to_wait > 0:
            # Wait before processing the order
            time.sleep(min(time_to_wait, 0.5))  # Sleep for up to 0.5 seconds
            with self.lock:
                self.orders.put(order)  # Return the order to the queue
        else:
            print(f"\n{order.name} SENT TO SHIPPING DEPARTMENT")

    def process_orders(self):
        """Process orders from the queue."""
        print("SCHEDULER STARTED PROCESSING...")
        while self.running:
            self.order_event.wait()  # Wait for a signal about a new order
            try:
                while not self.orders.empty():  # Process all available orders
                    with self.lock:
                        order = self.orders.get(block=False)
                    self._process_order(order)
            except queue.Empty:
                continue
            finally:
                if self.orders.empty():  # Clear the event if the queue is empty
                    self.order_event.clear()

    def stop_scheduler(self):
        """Stop the order processing thread."""
        self.running = False
        self.order_event.set()  # Signal to exit the wait


def parse_order_input(order_details: str) -> Order:
    """Parse user input and create an Order object."""
    data = order_details.split(" ")
    if len(data) != 2 or not data[1].isdigit():
        raise ValueError("Invalid input format")
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
        scheduler.stop_scheduler()
        thread.join()  # Wait for the thread to finish
        raise SystemExit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        raise SystemExit(0)
