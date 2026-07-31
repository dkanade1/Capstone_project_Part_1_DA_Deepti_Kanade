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


## Tables Used in This Project
### The following tables were used for data cleaning and analysis:

* Orders – order dates, shipped dates, freight charges.
* Customers – company information, region, and country.
* Order Details – quantity, unit price, discount.
* Products – unit price, inventory, and reorder information.

## Task 1:	Stand up a two-table (or more) relational dataset :
#### Foreign key integrity check 
```python
PRAGMA foreign_keys = ON;
INSERT INTO Orders (OrderID,CustomerID)
VALUES (99997, 'XYZ89');
```
<img width="717" height="177" alt="image" src="https://github.com/user-attachments/assets/fde35733-2eb2-49a0-b995-92748ab8a7e2" />

## Task 2 : Basic  SQL queries 

```python
select * from Products where CategoryID IN ('1','8');
select * from Products where CategoryID NOT IN ('1','8');
select * from Orders where OrderDate BETWEEN '2016-7-11' AND '2019-01-01' ;
select * from Orders where OrderDate BETWEEN '2016-7-11' AND '2019-01-01' ORDER BY CustomerID ASC , OrderDate DESC;
select * from Products p 
where NOT EXISTS (
select *
from 'Order Details' as o
 where  p.ProductID = o.ProductID
); 

SELECT c.CustomerID,
       c.CompanyName
FROM Customers c
WHERE NOT EXISTS (
    SELECT 1
    FROM Orders o
    WHERE o.CustomerID = c.CustomerID
);
```

**Result:**
1. There are no products which havent been ordered.
2. There are customers who havent placed any order.
<img width="424" height="404" alt="image" src="https://github.com/user-attachments/assets/c1aca755-ffb5-44d6-b610-39d8a28796c3" />

## Task 3: GROUP BY + HAVING query 
```python
-- Task 3 GROUP BY + HAVING query 
select count(SupplierID) from Suppliers GROUP BY Region HAVING count(SupplierID) > 2;
select sum(Quantity),ProductID from 'Order Details' group BY ProductID having sum(Quantity) < 200000;
```
**Result:**
<img width="982" height="242" alt="image" src="https://github.com/user-attachments/assets/e3c519c0-4a93-4b54-bb95-305cc39eb45e" />
______________________________________________________________________
<img width="1005" height="441" alt="image" src="https://github.com/user-attachments/assets/60389e27-6a26-4157-91c0-8cceb6dad047" />

## Task 4: Inner and Left Join
- The inner join query combines information from four related tables to create a single dataset containing Order information using  order, and product details.Orders is used as the starting (left) table because it represents the main business transaction. Every record in the final dataset is centered around an order and it is the primary entity being analyzed.Customers is joined to Orders using CustomerID because each order belongs to one customer.Order Details is joined to Orders using OrderID because to obtain order details.Products is joined to Order Details using ProductID to retrieve product-specific information.
- The left join query retrieves all employees together with the territories assigned to them.Employees is the primary table and is placed on the left side because the objective is to list every employee, regardless of whether they have been assigned a territory and EmployeeTerritories stores the relationship between employees and territories. It is a child table that contains only employees who have territory assignments.
```sql
SELECT
    o.OrderID,
    o.OrderDate,
    o.ShippedDate,
	   o.Freight,
    c.CustomerID,
    c.CompanyName,
    c.Region,
    c.Country,
    od.ProductID,
    od.Quantity,
    od.UnitPrice,
	p.UnitsInStock,
	p.UnitsOnOrder,
    od.Discount
FROM Orders o
JOIN Customers c
    ON o.CustomerID = c.CustomerID
JOIN [Order Details] od
    ON o.OrderID = od.OrderID
Join Products p
	ON od.ProductID = p.ProductID
	LIMIT 10000;

SELECT E.EmployeeID,ET.TerritoryID
FROM Employees as E
left  JOIN EmployeeTerritories as ET
ON E.EmployeeID = ET.EmployeeID;
```
**Result:**
<img width="1318" height="773" alt="image" src="https://github.com/user-attachments/assets/02afbbb6-904f-4eb6-a88f-3b2c8174f45d" />

**There is one employee who has not been assigned a territory**

<img width="401" height="700" alt="image" src="https://github.com/user-attachments/assets/25492248-3452-4f52-957d-066f4e9527cb" />

## Task 5: Validate referential integrity before analysis
- **COUNT(DISTINCT EmployeeID) in Employees showed that 9 Employees have  Territories assigned to them.**
```sql
--a COUNT(DISTINCT ...) query 
SELECT count(distinct E.EmployeeID)
FROM Employees as E
left OUTER JOIN EmployeeTerritories as ET
ON E.EmployeeID = ET.EmployeeID;
```
<img width="503" height="223" alt="image" src="https://github.com/user-attachments/assets/c7e77a20-5e97-421e-849c-549a0b22ad71" />

- **Grouping the Orders table by EmployeeID showed that many employees have more than one territory (HAVING COUNT(*) > 1 returned multiple rows), confirming that the relationship is 1:many.**
```sql
--a grouped child-count query 
SELECT E.EmployeeID , count(*) as no_of_terr
FROM Employees as E
left OUTER JOIN EmployeeTerritories as ET
ON E.EmployeeID = ET.EmployeeID
Group BY E.EmployeeID 
HAVING COUNT(*) > 1;
```
<img width="488" height="511" alt="image" src="https://github.com/user-attachments/assets/2ee53bcb-d4c1-44b1-9fbe-10c6f737ee4f" />

- **An orphan check using NOT EXISTS returned 1 rows, indicating that there is one order record with no customer information referencing in the customer table.One  orphan record was found.**
```sql
-- an explicit orphan check 
SELECT *
FROM Orders o
WHERE NOT EXISTS (
    SELECT 1
    FROM Customers c
    WHERE o.CustomerID = c.CustomerID);
```
<img width="1275" height="276" alt="image" src="https://github.com/user-attachments/assets/2c547f8c-4171-4d8c-91b5-b47504b20e38" />



