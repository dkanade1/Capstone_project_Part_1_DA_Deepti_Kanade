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
## Prerequisites
Before getting started, make sure your development environment meets the following requirements:
Python: Version 3.11.7 
For the rest , please refer to Requirements.txt

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

- **Relationship analyzed: Employees → EmployeeTerritories .Grouping the Orders table by EmployeeID showed that many employees have more than one territory (HAVING COUNT(*) > 1 returned multiple rows), confirming that the relationship is 1:many.**
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

## Task 7: Clean CSV data in Pandas

```python
import pandas as pd
import numpy as np
from scipy.stats import zscore
df = pd.read_csv("Task_8_1.csv")

#find out missing count
print("_______Missing values in the CSV __________")
missing_count = df.isnull().sum()
print(missing_count)

#Converting the date fields from string to Date type
df["OrderDate"] = pd.to_datetime(df["OrderDate"],format="mixed", errors="coerce")
df["ShippedDate"] = pd.to_datetime(df["ShippedDate"],format="mixed", errors="coerce")

##Calculate median of shipping delays
median_delay = (df["ShippedDate"] - df["OrderDate"]).dt.days.median()
mask = df["ShippedDate"].isna() & df["OrderDate"].notna()
print("\n_________Displaying Rows with valid order date but null shipping date________\n")
print(df.loc[mask].to_string())

##Update the shipping date with the delay from order date
df.loc[mask, "ShippedDate"] = (
   df.loc[mask, "OrderDate"] +
   pd.to_timedelta(int(median_delay), unit="D")
)
print("_____________Updated shipped date after imputation____________\n")
print(df.loc[mask].to_string())

# ## Fill 'unknown' values in region and country column with null values
print("_________________________________\n")
print("No of Rows with null values in Region and country Column: ",df["Region"].isna().sum(),df["Country"].isna().sum())
df["Region"] = df["Region"].fillna("Unknown")
df["Country"] = df["Country"].fillna("Unknown")
print("No of Rows with null values in Region and country Column after updating with unknown: ",df["Region"].isna().sum(),df["Country"].isna().sum())

#Calculating missing values after imputaion
missing_count2 = df.isnull().sum()
print(f"\n_______________Missing value count after imputation____________\n",missing_count2)

#  Check and remove duplicates
print("_______________Checking for duplicate rows_____________\n")
print("Rows before:", len(df))
print("Duplicate rows:", df.duplicated().sum())
df = df.drop_duplicates()
print("Rows after:", len(df))
```

- **In the data extracted, there were missing values in 'Shipping Date', 'Region' and 'Country' Column**
- **For shipped date , we calculate the median of shipping delay(from order date) and use it to fill missing ShipDate values by adding the delay to the order dates. We are only updating shipping date if an order date exists. Using the median is often a better choice if shipping times are skewed or contain unusually long delays and is less sensitive to extreme values (outliers) than the mean.**
- **For the 'Region' and 'Country' column , we filled the missing rows with 'unknown' because these are categorical values.**
- **There were few duplicate records which were inserted in the database to showcase the removal of duplicate entries.** 
### Refer to the output below:

```
C:\AI_Projects\venv\Scripts\python.exe C:/AI_Projects/Part_1_task_1.py
_______Missing values in the CSV __________
OrderID           0
OrderDate         0
ShippedDate      73
Freight           0
CustomerID        0
CompanyName       0
Region          128
Country         128
ProductID         0
Quantity          0
UnitPrice         0
UnitsInStock      0
UnitsOnOrder      0
Discount          0
dtype: int64

_________Displaying Rows with valid order date but null shipping date________

      OrderID  OrderDate ShippedDate  Freight CustomerID                 CompanyName           Region      Country  ProductID  Quantity  UnitPrice  UnitsInStock  UnitsOnOrder  Discount
1964    11008 2018-04-08         NaT    55.25      ERNSH                Ernst Handel   Western Europe      Austria         28        70      45.60            26             0      0.05
1965    11008 2018-04-08         NaT    55.25      ERNSH                Ernst Handel   Western Europe      Austria         34        90      14.00           111             0      0.05
1966    11008 2018-04-08         NaT    55.25      ERNSH                Ernst Handel   Western Europe      Austria         71        21      21.50            26             0      0.00
1992    11019 2018-04-13         NaT    11.25      RANCH               Rancho grande    South America    Argentina         46         3      12.00            95             0      0.00
1993    11019 2018-04-13         NaT    11.25      RANCH               Rancho grande    South America    Argentina         49         2      20.00            10            60      0.00
2045    11039 2018-04-21         NaT    43.00      LINOD            LINO-Delicateses    South America    Venezuela         28        20      45.60            26             0      0.00
2046    11039 2018-04-21         NaT    43.00      LINOD            LINO-Delicateses    South America    Venezuela         35        24      18.00            20             0      0.00
2047    11039 2018-04-21         NaT    43.00      LINOD            LINO-Delicateses    South America    Venezuela         49        60      20.00            10            60      0.00
2048    11039 2018-04-21         NaT    43.00      LINOD            LINO-Delicateses    South America    Venezuela         57        28      19.50            36             0      0.00
2049    11040 2018-04-22         NaT    15.00      GREAL     Great Lakes Food Market    North America          USA         21        20      10.00             3            40      0.00
2056    11045 2018-04-23         NaT    19.75      BOTTM       Bottom-Dollar Markets    North America       Canada         33        15       2.50           112             0      0.00
2057    11045 2018-04-23         NaT    19.75      BOTTM       Bottom-Dollar Markets    North America       Canada         51        24      53.00            20             0      0.00
2067    11051 2018-04-27         NaT    12.50      LAMAI            La maison d'Asie   Western Europe       France         24        10       4.50            20             0      0.20
2073    11054 2018-04-28         NaT    17.50      CACTU  Cactus Comidas para llevar    South America    Argentina         33        10       2.50           112             0      0.00
2074    11054 2018-04-28         NaT    17.50      CACTU  Cactus Comidas para llevar    South America    Argentina         67        20      14.00            52             0      0.00
2083    11058 2018-04-29         NaT    17.00      BLAUS     Blauer See Delikatessen   Western Europe      Germany         21         3      10.00             3            40      0.00
2084    11058 2018-04-29         NaT    17.00      BLAUS     Blauer See Delikatessen   Western Europe      Germany         60        21      34.00            19             0      0.00
2085    11058 2018-04-29         NaT    17.00      BLAUS     Blauer See Delikatessen   Western Europe      Germany         61         4      28.50           113             0      0.00
2086    11059 2018-04-29         NaT    29.25      RICAR          Ricardo Adocicados    South America       Brazil         13        30       6.00            24             0      0.00
2087    11059 2018-04-29         NaT    29.25      RICAR          Ricardo Adocicados    South America       Brazil         17        12      39.00             0             0      0.00
2088    11059 2018-04-29         NaT    29.25      RICAR          Ricardo Adocicados    South America       Brazil         60        35      34.00            19             0      0.00
2091    11061 2018-04-30         NaT    13.75      GREAL     Great Lakes Food Market    North America          USA         60        15      34.00            19             0      0.00
2092    11062 2018-04-30         NaT    15.50      REGGC          Reggiani Caseifici  Southern Europe        Italy         53        10      32.80             0             0      0.20
2093    11062 2018-04-30         NaT    15.50      REGGC          Reggiani Caseifici  Southern Europe        Italy         70        12      15.00            15            10      0.20
2102    11065 2018-05-01         NaT    16.00      LILAS           LILA-Supermercado    South America    Venezuela         30         4      25.89            10             0      0.25
2103    11065 2018-05-01         NaT    16.00      LILAS           LILA-Supermercado    South America    Venezuela         54        20       7.45            21             0      0.25
2108    11068 2018-05-04         NaT    28.00      QUEEN               Queen Cozinha    South America       Brazil         28         8      45.60            26             0      0.15
2109    11068 2018-05-04         NaT    28.00      QUEEN               Queen Cozinha    South America       Brazil         43        36      46.00            17            10      0.15
2110    11068 2018-05-04         NaT    28.00      QUEEN               Queen Cozinha    South America       Brazil         77        28      13.00            32             0      0.15
2112    11070 2018-05-05         NaT    37.50      LEHMS         Lehmanns Marktstand   Western Europe      Germany          1        40      18.00            39             0      0.15
2113    11070 2018-05-05         NaT    37.50      LEHMS         Lehmanns Marktstand   Western Europe      Germany          2        20      19.00            17            40      0.15
2114    11070 2018-05-05         NaT    37.50      LEHMS         Lehmanns Marktstand   Western Europe      Germany         16        30      17.45            29             0      0.15
2115    11070 2018-05-05         NaT    37.50      LEHMS         Lehmanns Marktstand   Western Europe      Germany         31        20      12.50             0            70      0.00
2116    11071 2018-05-05         NaT    16.25      LILAS           LILA-Supermercado    South America    Venezuela          7        15      30.00            15             0      0.05
2117    11071 2018-05-05         NaT    16.25      LILAS           LILA-Supermercado    South America    Venezuela         13        10       6.00            24             0      0.05
2118    11072 2018-05-05         NaT    60.00      ERNSH                Ernst Handel   Western Europe      Austria          2         8      19.00            17            40      0.00
2119    11072 2018-05-05         NaT    60.00      ERNSH                Ernst Handel   Western Europe      Austria         41        40       9.65            85             0      0.00
2120    11072 2018-05-05         NaT    60.00      ERNSH                Ernst Handel   Western Europe      Austria         50        22      16.25            65             0      0.00
2121    11072 2018-05-05         NaT    60.00      ERNSH                Ernst Handel   Western Europe      Austria         64       130      33.25            22            80      0.00
2122    11073 2018-05-05         NaT    17.50      PERIC   Pericles Comidas clásicas  Central America       Mexico         11        10      21.00            22            30      0.00
2123    11073 2018-05-05         NaT    17.50      PERIC   Pericles Comidas clásicas  Central America       Mexico         24        20       4.50            20             0      0.00
2124    11074 2018-05-06         NaT    13.50      SIMOB               Simons bistro  Northern Europe      Denmark         16        14      17.45            29             0      0.05
2125    11075 2018-05-06         NaT    20.50      RICSU          Richter Supermarkt   Western Europe  Switzerland          2        10      19.00            17            40      0.15
2126    11075 2018-05-06         NaT    20.50      RICSU          Richter Supermarkt   Western Europe  Switzerland         46        30      12.00            95             0      0.15
2127    11075 2018-05-06         NaT    20.50      RICSU          Richter Supermarkt   Western Europe  Switzerland         76         2      18.00            57             0      0.15
2128    11076 2018-05-06         NaT    22.50      BONAP                    Bon app'   Western Europe       France          6        20      25.00           120             0      0.25
2129    11076 2018-05-06         NaT    22.50      BONAP                    Bon app'   Western Europe       France         14        20      23.25            35             0      0.25
2130    11076 2018-05-06         NaT    22.50      BONAP                    Bon app'   Western Europe       France         19        10       9.20            25             0      0.25
2131    11077 2018-05-06         NaT    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA          2        24      19.00            17            40      0.20
2132    11077 2018-05-06         NaT    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA          3         4      10.00            13            70      0.00
2133    11077 2018-05-06         NaT    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA          4         1      22.00            53             0      0.00
2134    11077 2018-05-06         NaT    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA          6         1      25.00           120             0      0.02
2135    11077 2018-05-06         NaT    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA          7         1      30.00            15             0      0.05
2136    11077 2018-05-06         NaT    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA          8         2      40.00             6             0      0.10
2137    11077 2018-05-06         NaT    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         10         1      31.00            31             0      0.00
2138    11077 2018-05-06         NaT    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         12         2      38.00            86             0      0.05
2139    11077 2018-05-06         NaT    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         13         4       6.00            24             0      0.00
2140    11077 2018-05-06         NaT    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         14         1      23.25            35             0      0.03
2141    11077 2018-05-06         NaT    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         16         2      17.45            29             0      0.03
2142    11077 2018-05-06         NaT    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         20         1      81.00            40             0      0.04
2143    11077 2018-05-06         NaT    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         23         2       9.00            61             0      0.00
2144    11077 2018-05-06         NaT    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         32         1      32.00             9            40      0.00
2145    11077 2018-05-06         NaT    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         39         2      18.00            69             0      0.05
2146    11077 2018-05-06         NaT    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         41         3       9.65            85             0      0.00
2147    11077 2018-05-06         NaT    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         46         3      12.00            95             0      0.02
2148    11077 2018-05-06         NaT    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         52         2       7.00            38             0      0.00
2149    11077 2018-05-06         NaT    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         55         2      24.00           115             0      0.00
2150    11077 2018-05-06         NaT    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         60         2      34.00            19             0      0.06
2151    11077 2018-05-06         NaT    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         64         2      33.25            22            80      0.03
2152    11077 2018-05-06         NaT    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         66         1      17.00             4           100      0.00
2153    11077 2018-05-06         NaT    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         73         2      15.00           101             0      0.01
2154    11077 2018-05-06         NaT    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         75         4       7.75           125             0      0.00
2155    11077 2018-05-06         NaT    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         77         2      13.00            32             0      0.00
_____________Updated shipped date after imputation____________

      OrderID  OrderDate ShippedDate  Freight CustomerID                 CompanyName           Region      Country  ProductID  Quantity  UnitPrice  UnitsInStock  UnitsOnOrder  Discount
1964    11008 2018-04-08  2018-04-14    55.25      ERNSH                Ernst Handel   Western Europe      Austria         28        70      45.60            26             0      0.05
1965    11008 2018-04-08  2018-04-14    55.25      ERNSH                Ernst Handel   Western Europe      Austria         34        90      14.00           111             0      0.05
1966    11008 2018-04-08  2018-04-14    55.25      ERNSH                Ernst Handel   Western Europe      Austria         71        21      21.50            26             0      0.00
1992    11019 2018-04-13  2018-04-19    11.25      RANCH               Rancho grande    South America    Argentina         46         3      12.00            95             0      0.00
1993    11019 2018-04-13  2018-04-19    11.25      RANCH               Rancho grande    South America    Argentina         49         2      20.00            10            60      0.00
2045    11039 2018-04-21  2018-04-27    43.00      LINOD            LINO-Delicateses    South America    Venezuela         28        20      45.60            26             0      0.00
2046    11039 2018-04-21  2018-04-27    43.00      LINOD            LINO-Delicateses    South America    Venezuela         35        24      18.00            20             0      0.00
2047    11039 2018-04-21  2018-04-27    43.00      LINOD            LINO-Delicateses    South America    Venezuela         49        60      20.00            10            60      0.00
2048    11039 2018-04-21  2018-04-27    43.00      LINOD            LINO-Delicateses    South America    Venezuela         57        28      19.50            36             0      0.00
2049    11040 2018-04-22  2018-04-28    15.00      GREAL     Great Lakes Food Market    North America          USA         21        20      10.00             3            40      0.00
2056    11045 2018-04-23  2018-04-29    19.75      BOTTM       Bottom-Dollar Markets    North America       Canada         33        15       2.50           112             0      0.00
2057    11045 2018-04-23  2018-04-29    19.75      BOTTM       Bottom-Dollar Markets    North America       Canada         51        24      53.00            20             0      0.00
2067    11051 2018-04-27  2018-05-03    12.50      LAMAI            La maison d'Asie   Western Europe       France         24        10       4.50            20             0      0.20
2073    11054 2018-04-28  2018-05-04    17.50      CACTU  Cactus Comidas para llevar    South America    Argentina         33        10       2.50           112             0      0.00
2074    11054 2018-04-28  2018-05-04    17.50      CACTU  Cactus Comidas para llevar    South America    Argentina         67        20      14.00            52             0      0.00
2083    11058 2018-04-29  2018-05-05    17.00      BLAUS     Blauer See Delikatessen   Western Europe      Germany         21         3      10.00             3            40      0.00
2084    11058 2018-04-29  2018-05-05    17.00      BLAUS     Blauer See Delikatessen   Western Europe      Germany         60        21      34.00            19             0      0.00
2085    11058 2018-04-29  2018-05-05    17.00      BLAUS     Blauer See Delikatessen   Western Europe      Germany         61         4      28.50           113             0      0.00
2086    11059 2018-04-29  2018-05-05    29.25      RICAR          Ricardo Adocicados    South America       Brazil         13        30       6.00            24             0      0.00
2087    11059 2018-04-29  2018-05-05    29.25      RICAR          Ricardo Adocicados    South America       Brazil         17        12      39.00             0             0      0.00
2088    11059 2018-04-29  2018-05-05    29.25      RICAR          Ricardo Adocicados    South America       Brazil         60        35      34.00            19             0      0.00
2091    11061 2018-04-30  2018-05-06    13.75      GREAL     Great Lakes Food Market    North America          USA         60        15      34.00            19             0      0.00
2092    11062 2018-04-30  2018-05-06    15.50      REGGC          Reggiani Caseifici  Southern Europe        Italy         53        10      32.80             0             0      0.20
2093    11062 2018-04-30  2018-05-06    15.50      REGGC          Reggiani Caseifici  Southern Europe        Italy         70        12      15.00            15            10      0.20
2102    11065 2018-05-01  2018-05-07    16.00      LILAS           LILA-Supermercado    South America    Venezuela         30         4      25.89            10             0      0.25
2103    11065 2018-05-01  2018-05-07    16.00      LILAS           LILA-Supermercado    South America    Venezuela         54        20       7.45            21             0      0.25
2108    11068 2018-05-04  2018-05-10    28.00      QUEEN               Queen Cozinha    South America       Brazil         28         8      45.60            26             0      0.15
2109    11068 2018-05-04  2018-05-10    28.00      QUEEN               Queen Cozinha    South America       Brazil         43        36      46.00            17            10      0.15
2110    11068 2018-05-04  2018-05-10    28.00      QUEEN               Queen Cozinha    South America       Brazil         77        28      13.00            32             0      0.15
2112    11070 2018-05-05  2018-05-11    37.50      LEHMS         Lehmanns Marktstand   Western Europe      Germany          1        40      18.00            39             0      0.15
2113    11070 2018-05-05  2018-05-11    37.50      LEHMS         Lehmanns Marktstand   Western Europe      Germany          2        20      19.00            17            40      0.15
2114    11070 2018-05-05  2018-05-11    37.50      LEHMS         Lehmanns Marktstand   Western Europe      Germany         16        30      17.45            29             0      0.15
2115    11070 2018-05-05  2018-05-11    37.50      LEHMS         Lehmanns Marktstand   Western Europe      Germany         31        20      12.50             0            70      0.00
2116    11071 2018-05-05  2018-05-11    16.25      LILAS           LILA-Supermercado    South America    Venezuela          7        15      30.00            15             0      0.05
2117    11071 2018-05-05  2018-05-11    16.25      LILAS           LILA-Supermercado    South America    Venezuela         13        10       6.00            24             0      0.05
2118    11072 2018-05-05  2018-05-11    60.00      ERNSH                Ernst Handel   Western Europe      Austria          2         8      19.00            17            40      0.00
2119    11072 2018-05-05  2018-05-11    60.00      ERNSH                Ernst Handel   Western Europe      Austria         41        40       9.65            85             0      0.00
2120    11072 2018-05-05  2018-05-11    60.00      ERNSH                Ernst Handel   Western Europe      Austria         50        22      16.25            65             0      0.00
2121    11072 2018-05-05  2018-05-11    60.00      ERNSH                Ernst Handel   Western Europe      Austria         64       130      33.25            22            80      0.00
2122    11073 2018-05-05  2018-05-11    17.50      PERIC   Pericles Comidas clásicas  Central America       Mexico         11        10      21.00            22            30      0.00
2123    11073 2018-05-05  2018-05-11    17.50      PERIC   Pericles Comidas clásicas  Central America       Mexico         24        20       4.50            20             0      0.00
2124    11074 2018-05-06  2018-05-12    13.50      SIMOB               Simons bistro  Northern Europe      Denmark         16        14      17.45            29             0      0.05
2125    11075 2018-05-06  2018-05-12    20.50      RICSU          Richter Supermarkt   Western Europe  Switzerland          2        10      19.00            17            40      0.15
2126    11075 2018-05-06  2018-05-12    20.50      RICSU          Richter Supermarkt   Western Europe  Switzerland         46        30      12.00            95             0      0.15
2127    11075 2018-05-06  2018-05-12    20.50      RICSU          Richter Supermarkt   Western Europe  Switzerland         76         2      18.00            57             0      0.15
2128    11076 2018-05-06  2018-05-12    22.50      BONAP                    Bon app'   Western Europe       France          6        20      25.00           120             0      0.25
2129    11076 2018-05-06  2018-05-12    22.50      BONAP                    Bon app'   Western Europe       France         14        20      23.25            35             0      0.25
2130    11076 2018-05-06  2018-05-12    22.50      BONAP                    Bon app'   Western Europe       France         19        10       9.20            25             0      0.25
2131    11077 2018-05-06  2018-05-12    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA          2        24      19.00            17            40      0.20
2132    11077 2018-05-06  2018-05-12    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA          3         4      10.00            13            70      0.00
2133    11077 2018-05-06  2018-05-12    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA          4         1      22.00            53             0      0.00
2134    11077 2018-05-06  2018-05-12    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA          6         1      25.00           120             0      0.02
2135    11077 2018-05-06  2018-05-12    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA          7         1      30.00            15             0      0.05
2136    11077 2018-05-06  2018-05-12    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA          8         2      40.00             6             0      0.10
2137    11077 2018-05-06  2018-05-12    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         10         1      31.00            31             0      0.00
2138    11077 2018-05-06  2018-05-12    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         12         2      38.00            86             0      0.05
2139    11077 2018-05-06  2018-05-12    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         13         4       6.00            24             0      0.00
2140    11077 2018-05-06  2018-05-12    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         14         1      23.25            35             0      0.03
2141    11077 2018-05-06  2018-05-12    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         16         2      17.45            29             0      0.03
2142    11077 2018-05-06  2018-05-12    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         20         1      81.00            40             0      0.04
2143    11077 2018-05-06  2018-05-12    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         23         2       9.00            61             0      0.00
2144    11077 2018-05-06  2018-05-12    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         32         1      32.00             9            40      0.00
2145    11077 2018-05-06  2018-05-12    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         39         2      18.00            69             0      0.05
2146    11077 2018-05-06  2018-05-12    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         41         3       9.65            85             0      0.00
2147    11077 2018-05-06  2018-05-12    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         46         3      12.00            95             0      0.02
2148    11077 2018-05-06  2018-05-12    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         52         2       7.00            38             0      0.00
2149    11077 2018-05-06  2018-05-12    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         55         2      24.00           115             0      0.00
2150    11077 2018-05-06  2018-05-12    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         60         2      34.00            19             0      0.06
2151    11077 2018-05-06  2018-05-12    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         64         2      33.25            22            80      0.03
2152    11077 2018-05-06  2018-05-12    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         66         1      17.00             4           100      0.00
2153    11077 2018-05-06  2018-05-12    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         73         2      15.00           101             0      0.01
2154    11077 2018-05-06  2018-05-12    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         75         4       7.75           125             0      0.00
2155    11077 2018-05-06  2018-05-12    28.00      RATTC  Rattlesnake Canyon Grocery    North America          USA         77         2      13.00            32             0      0.00
_________________________________

No of Rows with null values in Region and country Column:  128 128
No of Rows with null values in Region and country Column after updating with unknown:  0 0

_______________Missing value count after imputation____________
 OrderID         0
OrderDate       0
ShippedDate     0
Freight         0
CustomerID      0
CompanyName     0
Region          0
Country         0
ProductID       0
Quantity        0
UnitPrice       0
UnitsInStock    0
UnitsOnOrder    0
Discount        0
dtype: int64
_______________Checking for duplicate rows_____________

Rows before: 10005
Duplicate rows: 7
Rows after: 9998

```
## Task 8: Audit outliers 

```
def detect_zscore_outliers( df, column, threshold=3):
    z = zscore(df[column], nan_policy="omit")
# print(z)
    return df[np.abs(z) > threshold]

numeric_columns = [
    "Freight",
    "UnitPrice",
    "Quantity",
    "Discount",
    "UnitsInStock",
    "UnitsOnOrder"
]

def detect_iqr_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return df[(df[column] < lower) | (df[column] > upper)]
print("\n_______________Outliers Counts__________")
for col in numeric_columns:
    print(f"\n--- {col} ---")
    print("Z-score outliers:", len(detect_zscore_outliers(df, col)))
    print("IQR outliers:", len(detect_iqr_outliers(df, col)))

```


### Result
```
_______________Outliers Counts__________

--- Freight ---
Z-score outliers: 0
IQR outliers: 0

--- UnitPrice ---
Z-score outliers: 236
IQR outliers: 475

--- Quantity ---
Z-score outliers: 49
IQR outliers: 49

--- Discount ---
Z-score outliers: 472
IQR outliers: 838

--- UnitsInStock ---
Z-score outliers: 0
IQR outliers: 0

--- UnitsOnOrder ---
Z-score outliers: 243
IQR outliers: 2202

Process finished with exit code 0

```
**Filtering rule: The current csv file contains columns from the ‘Orders’ table , ’Customers’ , ” Order Details” and “Products” table.
Outlier detection was applied only to continuous numeric measures that represent business quantities
(for example: 
"Freight",
"UnitPrice",
"Quantity",
"Discount",
"UnitsInStock",
"UnitsOnOrder"
).**

**The following columns were excluded:**
-	Primary and foreign key columns (e.g., OrderID, CustomerID, ProductID) because they are identifiers rather than measurements. 
-	Date columns (OrderDate,  and ShippedDate) were excluded from outlier detection because they represent points in time rather than continuous numeric business measures.  
-	Columns with zero or near-zero variance because statistical outlier detection is not meaningful when there is little or no variation in the data.
-	Tables like c.CompanyName,    c.Region,    c.Country were skipped because they are non numeric data.

### Outlier Counts comparison between the two methods
| Column | Z-score Outliers | IQR Outliers | Agreement | Explanation |
|--------|-----------------:|-------------:|-----------|-------------|
| Freight | 0 | 0 | **Agree** | Both methods found no statistically significant outliers in this column. |
| UnitPrice | 236 | 475 | **Disagree** | The IQR method detected more outliers because it is more sensitive to skewed distributions, whereas the Z-score method is influenced by the mean and standard deviation. |
| Quantity | 49 | 49 | **Agree** | Both methods identified the same number of outliers, indicating a consistent distribution for this variable. |
| Discount | 472 | 838 | **Disagree** | The IQR method identified more outliers because the data is not normally distributed and contains many values at the extremes. |
| UnitsInStock | 0 | 0 | **Agree** | Neither method detected any outliers, suggesting that stock levels fall within the expected range. |
| UnitsOnOrder | 243 | 2202 | **Disagree** | The IQR method detected substantially more outliers because the distribution is highly skewed, while the Z-score method is less sensitive when the mean and standard deviation are affected by extreme values. |




