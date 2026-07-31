--Task 1 Foreign key integrity check 

PRAGMA foreign_keys = ON;
INSERT INTO Orders (OrderID,CustomerID)
VALUES (99997, 'XYZ89');

--Task 2: Basic  SQL queries 
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

select CompanyName,ContactName,ContactTitle from Customers where ContactTitle like "Sales%"

-- Task 3 GROUP BY + HAVING query 
select count(SupplierID) from Suppliers GROUP BY Region HAVING count(SupplierID) > 2;
select sum(Quantity),ProductID from 'Order Details' group BY ProductID having sum(Quantity) < 200000;

--Task 4 one INNER JOIN and one LEFT JOIN 
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

--Task 5
--a COUNT(DISTINCT ...) query 
SELECT count(distinct E.EmployeeID)
FROM Employees as E
left OUTER JOIN EmployeeTerritories as ET
ON E.EmployeeID = ET.EmployeeID;

--a grouped child-count query 
SELECT E.EmployeeID , count(*) as no_of_terr
FROM Employees as E
left OUTER JOIN EmployeeTerritories as ET
ON E.EmployeeID = ET.EmployeeID
Group BY E.EmployeeID 
HAVING COUNT(*) > 1;

-- an explicit orphan check 
SELECT *
FROM Orders o
WHERE NOT EXISTS (
    SELECT 1
    FROM Customers c
    WHERE o.CustomerID = c.CustomerID);


