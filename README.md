# Northwestern-Programs
This Python script demonstrates web scraping using BeautifulSoup and requests to extract course information from the Northwestern University Center for Talent Development website. The script fetches course details such as the course name, grade level, location, dates, fees, eligibility, and more. The extracted data is then processed and saved to a CSV file for further analysis.

## Prerequisite
To run this web scraping script, you need the following Python libraries:

1. BeautifulSoup (bs4)
2. requests
3. pandas
4. datetime

You can install these libraries using pip:
```python
pip install beautifulsoup4 requests pandas
```

## How to Use
1. Set the target URL in the URL variable to the Northwestern University Center for Talent Development course page with relevant filters (e.g., grade levels).
2. Run the Python script, and it will fetch and parse the web page's HTML content.
3. The script will extract course information, process it, and create a pandas DataFrame with the data.
4. The extracted data will be saved to a CSV file named "NW_Programs_renewed.csv" in the script's directory.

## Contributions
Contributions to this project are welcome. Feel free to open issues for bugs or new features, and submit pull requests to contribute code improvements.
