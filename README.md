# Search & Recommendation System (S&R)
Senior Design Project

## What is **S&R**?
Search & Recommendation System(S&R) is a web application.

It accepts a search query and a brand query from the user and uses these parameters to make a search on Trendyol and Amazon websites.

Scrapes the products from these websites and finally displays the processed results in a simple --yet effective GUI.

## Important Features  
### Sentiment Analysis  
Product reviews are analyzed with a Huggingface Sentiment Analysis Model.

### **Grouping**  
Groups are created from the products based on the product description. This enables a better and more organized shopping experience. User can browse the groups by looking at their labels.

### **Filtering**  
Low quality products are filtered, so the user can find exactly what they want.

### **Ranking**  
All products are ranked with a custom ranking formula, this ensures that high-quality products take first positions in the groups.

### **Simple GUI**  
Product Cards are designed to be simple and effective. Starred Attributes and most positive&negative comments can be found in the product cards.

## Implementation
Web Scraping is made with Selenium - (Python).
Web Application is made with Flask - (Python).
Logic is implemented with Python.
GUI is made with HTML, CSS, Javascript and Bootstrap 5.


## Running the App
ChromeDriver needs to be installed from here: https://chromedriver.chromium.org/

Clone the repository and run the following codes in terminal;
```  pip install -r requirements.txt ```
``` flask --app flaskui run ```

## Running w/ Docker
***Soon***
