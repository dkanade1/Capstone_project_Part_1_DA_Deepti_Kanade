# Capstone_project_DA_Deepti_Kanade
Capstone Project for Data Analytics course
<img width="743" height="166" alt="image" src="https://github.com/user-attachments/assets/048f27f5-e6ef-4cd8-906e-4085fc7f2d92" />
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
