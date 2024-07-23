Jamaican Colleges Program Scraper
Overview
This Python script is designed to scrape undergraduate program information from three Jamaican universities: University of the Commonwealth Caribbean (UCC), University of Technology (UTech), and The Mico University College. The script gathers data on various academic programs offered by these institutions and saves the information in both CSV and MongoDB formats.

Table of Contents
Requirements
Setup
Script Details
Constants
Functions
Execution
Error Handling
License
Requirements
To run this script, you'll need:

Python 3.x
The following Python libraries:
requests
beautifulsoup4 (BeautifulSoup)
pymongo
csv (standard library)
You can install the required libraries using pip:

bash
Copy code
pip install requests beautifulsoup4 pymongo
Setup
Clone or Download the Script:

Download the script from your repository or clone it if it’s hosted on a version control system.

Configure MongoDB:

Ensure you have MongoDB installed and running. Create a database and note the connection details.

Update Script Constants:

Edit the script to include your MongoDB connection details and update URLs if needed.

Script Details
Constants
UCC_URL: The URL to the undergraduate programs page of University of the Commonwealth Caribbean (UCC).
UTECH_BASE_URL: Base URL for University of Technology (UTech).
UTECH_ENDPOINTS: Dictionary containing endpoints for various faculties at UTech.
THEMICO_URL: URL to the undergraduate programs page of The Mico University College.
headers: HTTP headers used for making requests to avoid being blocked by the websites.
Functions
1. save_to_csv(data, filename)
Description: Saves the scraped data to a CSV file.

Parameters:

data (list of dicts): The data to save.
filename (str): The name of the file to save the data to.
Usage:

python
Copy code
save_to_csv(all_data, 'output.csv')
2. save_to_mongodb(data)
Description: Saves the scraped data to MongoDB. Each college's data is stored in a separate collection.

Parameters:

data (list of dicts): The data to save.
Usage:

python
Copy code
save_to_mongodb(all_data)
3. scrape_ucc_table(table, table_name)
Description: Scrapes program data from a UCC table.

Parameters:

table (BeautifulSoup object): The table HTML element.
table_name (str): The name of the table (e.g., "School of Business, Administration and Management").
Returns: A list of dictionaries with program details.

Usage:

python
Copy code
programs = scrape_ucc_table(ucc_tables[0], "School of Business, Administration and Management")
4. scrape_utech_programs()
Description: Scrapes programs from various faculties at UTech.

Returns: A list of dictionaries with program details for UTech.

Usage:

python
Copy code
programs = scrape_utech_programs()
5. scrape_cohs_programs(soup, url)
Description: Scrapes programs from the College of Health Sciences (COHS) at UTech.

Parameters:

soup (BeautifulSoup object): The parsed HTML content.
url (str): The URL of the page.
Returns: A list of dictionaries with program details.

Usage:

python
Copy code
programs = scrape_cohs_programs(soup, url)
6. scrape_cobam_soba_programs(soup, url)
Description: Scrapes programs from the School of Business Administration (SOBA) at UTech.

Parameters:

soup (BeautifulSoup object): The parsed HTML content.
url (str): The URL of the page.
Returns: A list of dictionaries with program details.

Usage:

python
Copy code
programs = scrape_cobam_soba_programs(soup, url)
7. scrape_fels_programs(soup, url)
Description: Scrapes programs from the Faculty of Education and Liberal Studies (FELS) at UTech.

Parameters:

soup (BeautifulSoup object): The parsed HTML content.
url (str): The URL of the page.
Returns: A list of dictionaries with program details.

Usage:

python
Copy code
programs = scrape_fels_programs(soup, url)
8. scrape_fenc_programs(soup, url)
Description: Scrapes programs from the Faculty of Engineering and Computing (FENC) at UTech.

Parameters:

soup (BeautifulSoup object): The parsed HTML content.
url (str): The URL of the page.
Returns: A list of dictionaries with program details.

Usage:

python
Copy code
programs = scrape_fenc_programs(soup, url)
9. scrape_fol_programs(soup, url)
Description: Scrapes programs from the Faculty of Law (FOL) at UTech.

Parameters:

soup (BeautifulSoup object): The parsed HTML content.
url (str): The URL of the page.
Returns: A list of dictionaries with program details.

Usage:

python
Copy code
programs = scrape_fol_programs(soup, url)
10. scrape_foss_programs(soup, url)
Description: Scrapes programs from the Faculty of Science and Sport (FOSS) at UTech.

Parameters:

soup (BeautifulSoup object): The parsed HTML content.
url (str): The URL of the page.
Returns: A list of dictionaries with program details.

Usage:

python
Copy code
programs = scrape_foss_programs(soup, url)
11. scrape_fobe_programs(soup, url)
Description: Scrapes programs from the Faculty of the Built Environment (FOBE) at UTech.

Parameters:

soup (BeautifulSoup object): The parsed HTML content.
url (str): The URL of the page.
Returns: A list of dictionaries with program details.

Usage:

python
Copy code
programs = scrape_fobe_programs(soup, url)
12. scrape_joint_programs(soup, url)
Description: Scrapes programs from the Joint Faculty of Oral Health Sciences and School of Public Health & Health Technology at UTech.

Parameters:

soup (BeautifulSoup object): The parsed HTML content.
url (str): The URL of the page.
Returns: A list of dictionaries with program details.

Usage:

python
Copy code
programs = scrape_joint_programs(soup, url)
13. scrape_themico_programs()
Description: Scrapes programs from The Mico University College.

Returns: A list of dictionaries with program details.

Usage:

python
Copy code
programs = scrape_themico_programs()
Execution
To run the script:

Navigate to the Script Directory:

Open your terminal or command prompt and navigate to the directory containing the script.

Run the Script:

Execute the script using Python:

bash
Copy code
python script.py
This will:

Scrape data from UCC, UTech, and The Mico University College.
Save the data to a CSV file with a timestamp.
Store the data in MongoDB in separate collections for each college.
Error Handling
Network Errors: The script handles exceptions related to network issues, such as connection errors or timeouts, and prints relevant messages.
Unexpected Errors: General exceptions are caught and printed to the console.
Ensure you have a stable internet connection and correct URLs for the script to function properly.