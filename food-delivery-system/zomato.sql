create database zomato;
use zomato;
CREATE TABLE Users (
    User_ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Phone VARCHAR(15) UNIQUE NOT NULL,
    Address TEXT,	
    Payment_Details TEXT
);


CREATE TABLE Restaurants(
	Restaurant_ID INT PRIMARY KEY,
	name varchar(200) NOT NULL,
	
	ratings INT CHECK(ratings between 0 and 5),
	address varchar(50) NOT NULL,
	status enum('OPEN','CLOSE') ,
	contact varchar(20) NOT NULL);



CREATE TABLE MenuItems (
    Item_ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Price DECIMAL(10,2) NOT NULL,
    Category VARCHAR(50),
    Description TEXT,
    Restaurant_ID INT,
    FOREIGN KEY (Restaurant_ID) REFERENCES Restaurants(Restaurant_ID) ON DELETE CASCADE
);

CREATE TABLE Orders (
    Order_ID INT PRIMARY KEY AUTO_INCREMENT,
    User_ID INT,
    Restaurant_ID INT,
    Order_Status ENUM('Placed', 'Preparing', 'Out for Delivery', 'Delivered') DEFAULT 'Placed',
    Total_Amount DECIMAL(10,2) NOT NULL,
    Payment_Status ENUM('Pending', 'Paid') DEFAULT 'Pending',
    Order_Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID) ON DELETE CASCADE,
    FOREIGN KEY (Restaurant_ID) REFERENCES Restaurants(Restaurant_ID) ON DELETE CASCADE
);

CREATE TABLE Delivery (
    Delivery_ID INT PRIMARY KEY AUTO_INCREMENT,
    Order_ID INT UNIQUE,
    Delivery_Partner_ID INT,
    Estimated_Delivery_Time TIMESTAMP,
    Actual_Delivery_Time TIMESTAMP,
    Status ENUM('Assigned', 'Picked Up', 'On the Way', 'Delivered') DEFAULT 'Assigned',
    FOREIGN KEY (Order_ID) REFERENCES Orders(Order_ID) ON DELETE CASCADE,
    FOREIGN KEY (Delivery_Partner_ID) REFERENCES Users(User_ID) ON DELETE CASCADE
);

CREATE TABLE Payments (
    Payment_ID INT PRIMARY KEY AUTO_INCREMENT,
    Order_ID INT UNIQUE,
    User_ID INT,
    Amount DECIMAL(10,2) NOT NULL,
    Payment_Method ENUM('Credit Card', 'Debit Card', 'UPI', 'Cash on Delivery'),
    Payment_Status ENUM('Success', 'Failed', 'Pending') DEFAULT 'Pending',
    FOREIGN KEY (Order_ID) REFERENCES Orders(Order_ID) ON DELETE CASCADE,
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID) ON DELETE CASCADE
);

INSERT INTO Users (Name, Email, Phone, Address, Payment_Details) 
VALUES 
('Sandesh Jawale', 'sandy@gmail.com', '9876543210', 'Narhe', 'UPI: idfc@bank'),
('Aditya Nalla', 'andy@gmail.com', '9876543211', 'Katraj', 'UPI: hdfc@bank');

select * from Users;


INSERT INTO Restaurants 
VALUES 
('Maratha',101 ,3 , 'Narhe', 'OPEN','9998887770'),
('Arav',102 ,4 , 'Manaji Nagar','OPEN' ,'9998887771');

select * from Restaurants;

INSERT INTO MenuItems (Name, Price, Category, Description, Restaurant_ID) 
VALUES 
('Margherita Pizza', 49, 'Pizza', 'Classic cheese pizza', 101),
('Cheeseburger', 19, 'Burger', 'Juicy beef burger with cheese', 102);

select * from MenuItems;

INSERT INTO Orders (User_ID, Restaurant_ID, Total_Amount, Payment_Status) 
VALUES 
(1, 101, 49, 'Paid');

select * from Orders;

INSERT INTO Delivery (Order_ID, Delivery_Partner_ID, Estimated_Delivery_Time, Status) 
VALUES 
(1, 2, NOW() + INTERVAL 30 MINUTE, 'Picked Up');

select * from Delivery;

INSERT INTO Payments (Order_ID, User_ID, Amount, Payment_Method, Payment_Status) 
VALUES 
(1, 1, 49, 'UPI', 'Success');

select * from Payments;