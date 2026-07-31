# Capstone_project_DA_Deepti_Kanade
Capstone Project for Data Analytics course

The Northwind sample database represents a small-scale specialty food export-import business. It manages core business operations including sales, customer relationships, product inventory, supplier sourcing, employee management, and order logistics.
Entity-Relationship Diagram (ERD)
<img width="763" height="666" alt="image" src="https://github.com/user-attachments/assets/2a910040-eb0f-40a0-9c36-1d60524c4315" />



Main Tables
Table	Description	Primary Key
Customers	Stores customer information such as company name, region, and country.	CustomerID
Orders	Stores customer orders, including order date, shipping date, freight, customer, and employee information.	OrderID
Order Details	Stores the products included in each order, along with quantity, unit price, and discount.	(OrderID, ProductID)
Products	Stores product information, prices, stock levels, reorder levels, and supplier/category references.	ProductID
Categories	Stores product categories.	CategoryID
Suppliers	Stores supplier information.	SupplierID
Employees	Stores employee information responsible for processing orders.	EmployeeID
Shippers	Stores shipping company information.	ShipperID

### 📋 Detailed Table Descriptions

#### 1. Sales & Order Fulfillment
* **`Orders`** 
  * Stores overall transaction details, including order dates, required dates, shipping dates, freight charges, and shipping destination addresses.
  * **Primary Key:** `OrderID`
  * **Foreign Keys:** `CustomerID`, `EmployeeID`, `ShipVia` (references `Shippers.ShipperID`)
* **`Order Details`** 
  * Junction table creating a **Many-to-Many (N:M)** relationship between `Orders` and `Products`. Tracks historical unit price, quantity ordered, and applied discount percentage for every line item.
  * **Composite Primary Key:** (`OrderID`, `ProductID`)
  * **Foreign Keys:** `OrderID`, `ProductID`

#### 2. Product Catalog & Inventory
* **`Products`**
  * Core inventory catalog detailing item pricing, stock quantities (`UnitsInStock`), reorder thresholds (`ReorderLevel`), and stock status (`Discontinued`).
  * **Primary Key:** `ProductID`
  * **Foreign Keys:** `SupplierID`, `CategoryID`
* **`Categories`**
  * High-level product classification (e.g., Beverages, Condiments, Dairy Products) along with text/image descriptions.
  * **Primary Key:** `CategoryID`
* **`Suppliers`**
  * Vendor contact information, address details, and regional location data for product sourcing.
  * **Primary Key:** `SupplierID`

#### 3. Customer & Shipping Logistics
* **`Customers`**
  * Client demographics, company names, point-of-contact roles, and full billing addresses.
  * **Primary Key:** `CustomerID` (Alphanumeric 5-character string)
* **`Shippers`**
  * Freight and carrier services responsible for delivering orders (e.g., Speedy Express, United Package, Federal Shipping).
  * **Primary Key:** `ShipperID`

#### 4. Human Resources & Sales Territories
* **`Employees`**
  * Staff profile records including reporting hierarchies (self-referencing relationship via `ReportsTo`), titles, hire dates, and home contact details.
  * **Primary Key:** `EmployeeID`
  * **Foreign Key:** `ReportsTo` (Self-referencing foreign key to `Employees.EmployeeID`)
* **`EmployeeTerritories` & `Territories` & `Region`**
  * Tracks sales territories assigned to specific employees, linked back to broader geographical regions (Eastern, Western, Northern, Southern).
  * **Primary Keys:** `TerritoryID`, `RegionID`
  

<img width="743" height="166" alt="image" src="https://github.com/user-attachments/assets/048f27f5-e6ef-4cd8-906e-4085fc7f2d92" />
