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
        # Create three lists of orders:
        self.next_day_orders = []  # Orders for the next day
        self.more_than_two_hours = []  # Orders with more than 2 hours until execution
        self.current_orders = []  # Current orders (less than 2 hours)
        self.task = None  # Asynchronous task

    async def schedule_order(self, order: Order):
        """Add an order to the appropriate list."""
        now = datetime.now()
        time_diff = (order.scheduled_time - now).total_seconds()

        # Distribute the order into the proper list:
        if order.scheduled_time.date() > now.date():
            self.next_day_orders.append(order)
            print(f"ORDER {order.name} ADDED TO NEXT DAY ORDERS")
        elif time_diff > 2 * 3600:
            self.more_than_two_hours.append(order)
            print(f"ORDER {order.name} ADDED TO MORE THAN 2 HOURS ORDERS")
        else:
            self.current_orders.append(order)
            print(f"ORDER {order.name} ADDED TO CURRENT ORDERS")

        # Sort the lists by execution time:
        self.next_day_orders.sort(key=lambda o: o.scheduled_time)
        self.more_than_two_hours.sort(key=lambda o: o.scheduled_time)
        self.current_orders.sort(key=lambda o: o.scheduled_time)

    async def process_current_orders(self):
        """Process current orders (less than 2 hours)."""
        while True:
            while self.current_orders:
                now = datetime.now()
                order = self.current_orders[0]
                if order.scheduled_time <= now:
                    self.current_orders.pop(0)
                    await self._process_order(order)
                else:
                    break
            await asyncio.sleep(5)  # Pause for 2 minutes

    async def process_more_than_two_hours(self):
        """Process orders scheduled more than 2 hours ahead."""
        while True:
            while self.more_than_two_hours:
                now = datetime.now()
                order = self.more_than_two_hours[0]
                time_diff = (order.scheduled_time - now).total_seconds()
                if time_diff <= 2 * 3600:
                    # Move the order to the current list if less than 2 hours remain
                    self.more_than_two_hours.pop(0)
                    await self.schedule_order(order)
                else:
                    break
            await asyncio.sleep(30 * 60)  # Pause for 30 minutes

    async def process_next_day_orders(self):
        """Process orders for the next day (at 00:00)."""
        while True:
            now = datetime.now()
            next_midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            time_to_wait = (next_midnight - now).total_seconds()

            print(f"Next daily check scheduled at: {next_midnight}")
            await asyncio.sleep(time_to_wait)  # Wait until 00:00

            # Process orders for the next day
            while self.next_day_orders:
                now = datetime.now()
                order = self.next_day_orders[0]
                if order.scheduled_time.date() <= now.date():
                    # Move the order to the appropriate list
                    self.next_day_orders.pop(0)
                    await self.schedule_order(order)
                else:
                    break

    async def _process_order(self, order: Order):
        """Process a specific order."""
        time_to_wait = (order.scheduled_time - datetime.now()).total_seconds()
        if time_to_wait <= 0:
            print(f"Order `{order.name}` is already overdue, processing immediately!")
        else:
            await asyncio.sleep(time_to_wait)
        print(f"\n{order.name} SENT TO SHIPPING DEPARTMENT")


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
    # Launch all handlers as separate tasks
    scheduler.task = [
        asyncio.create_task(scheduler.process_current_orders()),  # Current orders
        asyncio.create_task(scheduler.process_more_than_two_hours()),  # Orders with more than 2 hours
        asyncio.create_task(scheduler.process_next_day_orders())  # Orders for the next day
    ]

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