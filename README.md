# Part 1 — Data Foundations: SQL Extraction, Cleaning & Outlier Audit

### Database Schema
The Northwind sample database represents a small-scale specialty food export-import business. It manages core business operations including sales, customer relationships, product inventory, supplier sourcing, employee management, and order logistics.
Entity-Relationship Diagram (ERD)
<img width="763" height="666" alt="image" src="https://github.com/user-attachments/assets/2a910040-eb0f-40a0-9c36-1d60524c4315" />

## Main Tables

| Table | Description | Primary Key | Foreign Key(s) |
|-------|-------------|-------------|----------------|
| Customers | Stores customer information such as company name, region, and country. | `CustomerID` | None |
| Orders | Stores customer orders, including order date, required date, shipped date, and freight. | `OrderID` | `CustomerID` → Customers, `EmployeeID` → Employees, `ShipVia` → Shippers |
| Order Details | Stores the products included in each order, along with quantity, unit price, and discount. | (`OrderID`, `ProductID`) | `OrderID` → Orders, `ProductID` → Products |
| Products | Stores product information, prices, inventory levels, and reorder levels. | `ProductID` | `SupplierID` → Suppliers, `CategoryID` → Categories |
| Categories | Stores product categories. | `CategoryID` | None |
| Suppliers | Stores supplier information. | `SupplierID` | None |
| Employees | Stores employee information responsible for processing orders. | `EmployeeID` | `ReportsTo` → Employees (self-reference) |
| Shippers | Stores shipping company information. | `ShipperID` | None |

## Entity Relationships

| Parent Table | Child Table | Relationship | Foreign Key |
|--------------|-------------|--------------|-------------|
| Customers | Orders | One-to-Many (1:M) | `CustomerID` |
| Employees | Orders | One-to-Many (1:M) | `EmployeeID` |
| Shippers | Orders | One-to-Many (1:M) | `ShipVia` |
| Orders | Order Details | One-to-Many (1:M) | `OrderID` |
| Products | Order Details | One-to-Many (1:M) | `ProductID` |
| Categories | Products | One-to-Many (1:M) | `CategoryID` |
| Suppliers | Products | One-to-Many (1:M) | `SupplierID` |
| Employees | Employees | One-to-Many (Manager Hierarchy) | `ReportsTo` |


