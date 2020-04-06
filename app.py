from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# Line 5 - Line 12: Retrieves search term from user and formats it
search_term = input("Enter search term: ")
search_term_terms = search_term.split(' ')
new_search_term = ""

for x in search_term_terms:
	new_search_term = new_search_term + "%20" + x

new_search_term = new_search_term[3:]

# Loop variable for below loop
i = 1

# Loop for going through 5 search result pages
while i <= 5:

	# To add "&page=" for URLs except 1st one
	if i == 1:

		# Variable for storing the webpage address
		my_url = 'https://www.flipkart.com/search?q=' + new_search_term + '&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'

	else:

		# Variable for storing the webpage address
		my_url = 'https://www.flipkart.com/search?q=' + new_search_term + '&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off' + '&page=' + str(i)

	# Reading the contents in webpage
	uClient = uReq(my_url)
	page_html = uClient.read()
	uClient.close()

	# Parsing using BeautifulSoup
	page_soup = soup(page_html, "html.parser")

	# List of every search result (products)
	list_of_products = page_soup.findAll("div", {"style":"width:25%"})

	# Name of the output CSV file
	csv_file_name = "products.csv"

	# Name of column headers of CSV file
	csv_headers = "brand,product_name,price\n"

	# Creating CSV file for first time
	if i == 1:

		# Opening/Creating the CSV file and writing headers into it
		f = open(csv_file_name, "w")
		f.write(csv_headers)

	# Only appending the file
	else:

		f = open(csv_file_name, "a")


	# Loop for going through every product
	for product in list_of_products:

		# Storing every <a> blocks from webpage
		name_container = product.findAll("a")
		
		# Retrieving product name from 2nd <a> block
		product_name = name_container[1].text
		
		# Retrieving brand name by collecting first two words from product name
		brand = product_name.split()[0]

		# Removing brand name from product_name
		temp = product_name.split(' ', 1)
		product_name = temp[1]

		# Retrieving price info from 3rd <a> block
		# text[1:] strips 'Rupee' symbol
		price = name_container[2].div.div.text[1:]

		# Writing everything into CSV file, separated by commas
		# \n at end to move to next line in CSV file
		# replace used to remove commas from product name and price
		f.write(brand + "," + product_name.replace(",","|") + "," + price.replace(",","") + "\n")

	# Closing CSV file
	f.close()

	# Loop variable updation
	i += 1
