import asyncio
from dataclasses import dataclass
from datetime import datetime, timedelta

import aioconsole

ORDER_INPUT_ERROR = "Invalid input. Please use the format: <order_name> <delay_in_seconds>"


@dataclass(order=True)
class Order:
    scheduled_time: datetime  # When the order is supposed to be sent
    name: str  # The name of the order


class AsyncScheduler:
    def __init__(self):
        self.orders = []  # List to hold scheduled orders
        self.task = None  # Reference to the processing task

    async def schedule_order(self, order: Order):
        """Add an order to the queue and sort the list by scheduled time."""
        self.orders.append(order)
        # Sort based on the scheduled time
        self.orders.sort(key=lambda o: o.scheduled_time)
        print(f"ORDER {order.name} IS SCHEDULED")

    async def _process_order(self, order: Order):
        """Process a specific order."""
        time_to_wait = (order.scheduled_time - datetime.now()).total_seconds()
        if time_to_wait <= 0:
            print(f"Order `{order.name}` is already overdue, processing immediately!")
        else:
            await asyncio.sleep(time_to_wait)
        print(f"\n{order.name} SENT TO SHIPPING DEPARTMENT")

    async def process_orders(self):
        """Process orders from the queue asynchronously."""
        print("SCHEDULER STARTED PROCESSING...")
        try:
            while True:
                if not self.orders:
                    # print("No orders in the queue. Waiting...")
                    await asyncio.sleep(0.5)
                    continue
                order = self.orders[0]
                now = datetime.now()
                # print(f"Current time: {now}, next order time: {order.scheduled_time}")
                if order.scheduled_time <= now:
                    self.orders.pop(0)
                    await self._process_order(order)
                else:
                    time_to_next_order = (order.scheduled_time - now).total_seconds()
                    # print(f"Next order in: {time_to_next_order} seconds")
                    await asyncio.sleep(min(0.5, time_to_next_order))
        except asyncio.CancelledError:
            print("Processing task canceled...")
        except Exception as e:
            print(f"Error in processing orders: {str(e)}")

    async def stop_scheduler(self):
        """Stop the order processing task."""
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                print("Task has been cancelled.")


def parse_order_input(order_details: str) -> Order:
    """Parse user input and create an Order object."""
    data = order_details.split(" ")
    if len(data) != 2 or not data[1].isdigit():
        raise ValueError("Invalid input format")
    order_name, delay = data[0], int(data[1])
    scheduled_time = datetime.now() + timedelta(seconds=delay)
    print(f"Order scheduled at: {scheduled_time}")
    return Order(scheduled_time=scheduled_time, name=order_name)


async def main():
    scheduler = AsyncScheduler()
    # Start the processing task
    scheduler.task = asyncio.create_task(scheduler.process_orders())
    try:
        while True:
            order_details = await aioconsole.ainput("Enter order details: ")
            try:
                order = parse_order_input(order_details)
                await scheduler.schedule_order(order)
            except ValueError:
                print(ORDER_INPUT_ERROR)

    except KeyboardInterrupt:
        print("\nExiting...")
        await scheduler.stop_scheduler()
        raise SystemExit(0)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting...")
        raise SystemExit(0)