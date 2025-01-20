# Hillal_Python_pro
My study))

# Delivery Management System
## Overview
The application manages and simulates order deliveries using randomly selected delivery providers ("Uber" or "Uklon"). The primary aim is to simulate the process of adding, processing, shipping, and automatically archiving outdated orders in a multithreaded environment. It supports dynamic order input, real-time processing, and automated data cleanup.
## Key Features
### 1. **Order Addition**
The system allows users to add orders, which are stored in a queue for processing. Each order comes with a delay (in seconds) after which it is scheduled for delivery.
### 2. **Order Processing and Dispatch**
Orders are assigned to a randomly chosen delivery provider (`Uber` or `Uklon`). The delivery time is randomly selected depending on the provider:
- **Uber:** Delivery time ranges from **1 to 3 seconds**.
- **Uklon:** Delivery time ranges from **4 to 8 seconds**.

### 3. **Order Archiving**
Once the delivery is complete, an order’s status is updated to `Archived`. Orders that remain in the `Archived` state longer than the defined cleanup time (`ARCHIVE_THRESHOLD_SECONDS = 60` seconds) are automatically removed from storage.
## System Components
### 1. **Classes and Logic**
#### a. **`DeliveryService` (Abstract Class)**
A base abstract class for all delivery providers. It defines logic for managing delivery statuses:
- Tracks the status of all current orders.
- Moves delivered orders to the archive state.
- Implements thread-safe mechanisms using `Lock` to ensure data consistency in a multithreaded environment.

#### b. **`Uber` and `Uklon` (Concrete Classes)**
Define specific delivery logic for the `Uber` and `Uklon` providers.
#### c. **`Scheduler` **
Manages the order queue and distributes them to the respective delivery providers for processing.
Features:
- Continuously monitors and sends ready orders for delivery.
- Randomly selects a delivery provider for each order.

#### d. **`DeliveryRecord` **
A data class that stores delivery information, including:
- **Provider name:** Either `uber` or `uklon`.
- **Status:** (`ongoing`, `finished`, or `Archived`).
- **Last status update timestamp (`updated_at`).**

#### e. **`DeliveryOrder` **
Represents the structure of an individual order with a name (`order_name`) and a unique identifier (`uuid`).
### 2. **Global Components**
#### a. **Storage (`STORAGE`)**
Stores information about users, available dishes, and delivery orders

#### b. **Multithreading**
The system is multithreaded, with the following threads:
- **Order queue processing.**
- **Delivery status updates.**
- **Cleaning up expired archived orders.**

## Workflow
1. **Create a Scheduler:**
A `Scheduler` object starts a thread to continuously monitor the order queue.
2. **Add Orders:**
Users input order details (`Order Name` and `Delay in Seconds`), which get added to the queue for processing.
3. **Dispatch Orders:**
The system randomly selects a delivery provider for each order:
    - A `DeliveryOrder` with a unique identifier (`UUID`) is created.
    - The order is added to the delivery storage with an initial status of `ongoing`.

4. **Process Deliveries:**
After the delivery time delay, the order is marked as `finished`, then moved to the `Archived` state.
5. **Archive Cleanup:**
Regularly checks and removes orders in the `Archived` state that exceed the allowable archive retention time.


### Adding Orders
- Creates an order named `Pizza` which will become ready for delivery after a delay of 5 seconds.

### Delivery Process
🚚 Shipping [DeliveryOrder(order_name='Pizza', number=UUID)] with Uber. Time to wait: 3
UPDATED STORAGE: UUID is finished

### Archive Cleanup
Order UUID removed from STORAGE (archived for > 60 seconds)

## How to Run
1. Ensure Python version 3.10 or newer is installed.
2. Start the script:
3.    python delivery_ultra.py 

3. Provide orders as input in the format:
ORDER_NAME DELAY_IN_SECONDS
4.Stop the system by pressing `Ctrl+C`.

## Advantages
- **Multithreaded:** Efficient real-time processing of orders.
- **Thread-safe:** Secure access to shared resources using locks.
- **Automated Cleaning:** Automatically removes outdated orders to maintain performance.
- **Random Provider Selection:** Simulates real-world dynamic dispatching.

## Potential Improvements
1. **Implement REST API:**
Allow users to interact with the system programmatically rather than through the console.
2. **Logging:**
Add a mechanism for persisting logs to a file for easier debugging and tracking.
3. **Extend Delivery Providers:**
Add more providers and improve the provider selection logic.
4. **User Interface:**
Implement a graphical or web-based user interface to enhance usability.