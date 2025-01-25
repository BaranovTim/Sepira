# Sepira

**Sepira** is a website currently running on **[sepira.com](https://sepira.com)**, designed to manage a system of goods, allowing for their creation, modification, and organization. This platform facilitates the allocation of goods into specific sections within a warehouse using only their QR codes. Workers can add items to the warehouse, retrieve them, and monitor quantities. All operations are supported by a PostgreSQL database.

The QR code scanner is implemented in **JavaScript**, while the backend leverages the **Django framework** written in Python. Additionally, there are unique features for **superusers**—individuals responsible for managing the database. Superusers have access to advanced functionalities, such as adding **news updates** to ensure workers stay informed about the latest developments within the warehouse, as well as tracking worker activities, including the time, item, and quantity involved in each operation.

## Key Features:

### 1. QR Code Scanning:
- Scans goods to track and allocate them efficiently within the warehouse.
- Links scanned data to the user and timestamp, ensuring traceability.
- Workers input the quantity after scanning, which updates the database.

### 2. Warehouse Operations:
- Add goods to the warehouse.
- Retrieve goods.
- Update item quantities.
- Return goods.

### 3. PostgreSQL Database:
- Centralized storage for all data related to goods, users, and operations.

### 4. Superuser Features:
- Manage the database.
- Add and edit warehouse-related news.
- Track worker actions, including time, items handled, and quantities.

### 5. News Feature:
- Keeps workers informed about the latest updates, changes, and announcements.

### 6. User Roles:
- **Workers:** Focus on day-to-day operations like scanning, adding, and managing goods.
- **Superusers:** Handle administrative tasks and maintain data integrity.

### 7. Optimized Design:
- The interface is specifically tailored for efficient interaction, prioritizing functionality to streamline warehouse operations.

---

The code can be found here: [GitHub Repository](https://github.com/BaranovTim/Sepira).
