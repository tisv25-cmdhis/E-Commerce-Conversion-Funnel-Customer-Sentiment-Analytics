-- SQL statement to join dim_customers with dim_geography to enrich customer data with geographic information

SELECT 
    c.CustomerID,
    c.CustomerName,
    c.Email,
    c.Gender,
    c.Age,
    g.Country,
    g.City
FROM 
    dbo.customers as c
LEFT JOIN
    dbo.geography g
ON 
    c.GeographyID = g.GeographyID;




-- Query to categorize products based on their price

    SELECT 
    ProductID,
    ProductName,
    Price,
    CASE
        WHEN Price < 50 THEN 'Low'
        WHEN Price BETWEEN 50 AND 200 THEN 'Medium'
        ELSE 'High'
    END AS PriceCategory
FROM 
    dbo.products;





-- Query to clean whitespace issues in the ReviewText column

    SELECT 
    ReviewID,
    CustomerID,
    ProductID,
    ReviewDate,
    Rating,
    REPLACE(ReviewText, '  ', ' ') AS ReviewText
FROM 
    dbo.customer_reviews;





-- Query to clean and normalize the engagement_data table

    SELECT 
    EngagementID,
    ContentID,
    CampaignID,
    ProductID,
    UPPER(REPLACE(ContentType, 'Socialmedia', 'Social Media')) AS ContentType,
    LEFT(ViewsClicksCombined, CHARINDEX('-', ViewsClicksCombined) - 1) AS Views,
    RIGHT(ViewsClicksCombined, LEN(ViewsClicksCombined) - CHARINDEX('-', ViewsClicksCombined)) AS Clicks,
    Likes,
    FORMAT(CONVERT(DATE, EngagementDate), 'dd.MM.yyyy') AS EngagementDate
FROM 
    dbo.engagement_data
WHERE 
    ContentType != 'Newsletter';