import uuid
import random
import abc
import queue
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
import threading
from typing import Literal
from threading import Lock

# Constant to avoid "magic numbers" in archive logic
ARCHIVE_THRESHOLD_SECONDS = 60  # Maximum archive retention time in seconds

# Infrastructure storage
STORAGE = {
    "users": [],
    "dishes": [
        {"id": 1, "name": "pizza", "price": 1099, "restaurant": "Bueno"},
        {"id": 2, "name": "soda", "price": 199, "restaurant": "Melange"},
        {"id": 3, "name": "salad", "price": 599, "restaurant": "Melange"},
    ],
    "delivery": {},  # UUID: DeliveryRecord
}

# Thread-safe storage lock
storage_lock = Lock()

# Typing definitions
OrderRequestBody = tuple[str, datetime]
DeliveryProvider = Literal["uber", "uklon"]


# Blocking process simulation
def blocking_process(delay: int):
    time.sleep(delay)


# Data class to represent delivery records in STORAGE
@dataclass
class DeliveryRecord:
    provider: DeliveryProvider
    status: str  # Possible values: "ongoing", "finished", "Archived"
    updated_at: datetime | None


# DeliveryOrder represents an order to be shipped
@dataclass
class DeliveryOrder:
    order_name: str
    number: uuid.UUID | None = None


# Function to archive expired orders based on retention time
def archive_expired_orders(delivery_items: dict[uuid.UUID, DeliveryRecord]):
    """Removes records from storage that have been 'Archived' for a time exceeding the threshold."""
    now = datetime.now()
    orders_to_remove = [
        key for key, value in delivery_items.items()
        if value.status == "Archived" and value.updated_at and (
                now - value.updated_at).total_seconds() > ARCHIVE_THRESHOLD_SECONDS
    ]
    for order_id in orders_to_remove:
        del delivery_items[order_id]
        print(f"\t🧹 Order {order_id} removed from STORAGE (archived for > {ARCHIVE_THRESHOLD_SECONDS} seconds)")


# Abstract DeliveryService class representing common shipping logic for providers
class DeliveryService(abc.ABC):
    def __init__(self, order: DeliveryOrder) -> None:
        self._order: DeliveryOrder = order

    @classmethod
    def process_delivery(cls) -> None:
        """Processes the delivery status of orders periodically."""
        print("DELIVERY PROCESSING...")
        while True:
            with storage_lock:
                has_pending = cls.process_delivery_queue(STORAGE["delivery"])
            if not has_pending:
                time.sleep(1)  # Release GIL if no pending items to process

    @staticmethod
    def process_delivery_queue(delivery_items: dict[uuid.UUID, DeliveryRecord]) -> bool:
        """Checks and updates delivery status for delivered orders."""
        has_pending = False
        for key, value in delivery_items.items():
            if value.status == "finished":
                print(f"\n\t🚚 Order {key} is delivered by {value.provider}")
                value.status, value.updated_at = "Archived", datetime.now()
                print(f"\n\t🚚 Order {key} is Archived at {value.updated_at}")
            else:
                has_pending = True
        return has_pending

    @classmethod
    def clean_archived_orders(cls) -> None:
        """Cleans up orders that have been archived for too long."""
        print("ARCHIVE CLEANER STARTED...")
        while True:
            with storage_lock:
                archive_expired_orders(STORAGE["delivery"])
            time.sleep(0.5)

    def _ship(self, delay: int):
        """Starts the shipping process for the order, updating the status upon completion."""

        def callback():
            blocking_process(delay)
            with storage_lock:
                STORAGE["delivery"][self._order.number].status = "finished"
            print(f"\nUPDATED STORAGE: {self._order.number} is finished")

        thread = threading.Thread(target=callback)
        thread.start()

    @abc.abstractmethod
    def ship(self):
        """Abstract method for concrete provider implementations (e.g., Uber, Uklon)."""


# Concrete delivery service for Uklon
class Uklon(DeliveryService):
    def ship(self):
        self._order.number = uuid.uuid4()
        STORAGE["delivery"][self._order.number] = DeliveryRecord("uklon", "ongoing", None)
        delay: int = random.randint(4, 8)
        print(f"\n🚚 Shipping [{self._order}] with Uklon. Time to wait: {delay}")
        self._ship(delay)


# Concrete delivery service for Uber
class Uber(DeliveryService):
    def ship(self):
        self._order.number = uuid.uuid4()
        STORAGE["delivery"][self._order.number] = DeliveryRecord("uber", "ongoing", None)
        delay: int = random.randint(1, 3)
        print(f"\n🚚 Shipping [{self._order}] with Uber. Time to wait: {delay}")
        self._ship(delay)


# Scheduler manages and dispatches orders to appropriate delivery services
class Scheduler:
    def __init__(self):
        self.orders: queue.Queue[OrderRequestBody] = queue.Queue()

    def add_order(self, order: OrderRequestBody):
        self.orders.put(order)
        print(f"ORDER {order[0]} IS SCHEDULED")

    def _delivery_service_dispatcher(self) -> type[DeliveryService]:
        """Randomly selects a delivery provider (Uber or Uklon)."""
        random_provider: DeliveryProvider = random.choice(("uklon", "uber"))
        match random_provider:
            case "uklon":
                return Uklon
            case "uber":
                return Uber
            case _:
                raise Exception("Unknown delivery provider!")

    def ship_order(self, order_name: str) -> None:
        """Dispatches the order to a randomly chosen delivery service."""
        service_class: type[DeliveryService] = self._delivery_service_dispatcher()
        service_class(order=DeliveryOrder(order_name=order_name)).ship()

    def process_orders(self):
        """Continuously processes orders from the queue."""
        print("SCHEDULER PROCESSING...")
        while True:
            order = self.orders.get(True)  # Block until an order is available
            time_to_wait = order[1] - datetime.now()
            if time_to_wait.total_seconds() > 0:
                self.orders.put(order)  # Requeue the order if not ready
                time.sleep(0.5)
            else:
                self.ship_order(order[0])


# Entry point for the application
def main():
    scheduler = Scheduler()
    threading.Thread(target=scheduler.process_orders, daemon=True).start()
    threading.Thread(target=DeliveryService.process_delivery, daemon=True).start()
    threading.Thread(target=DeliveryService.clean_archived_orders, daemon=True).start()

    # Sample input: "A 5" (where 'A' is the order name and '5' is the delay in seconds)
    while True:
        if order_details := input("Enter order details: "):
            data = order_details.split(" ")
            order_name, delay = data[0], int(data[1])
            scheduler.add_order(
                (
                    order_name,
                    datetime.now() + timedelta(seconds=delay),
                )
            )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        raise SystemExit(0)