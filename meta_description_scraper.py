import requests
import csv
#If you're new to CSV files: https://en.wikipedia.org/wiki/Comma-separated_values
from bs4 import BeautifulSoup
#BeautifulSoup documentation: https://beautiful-soup-4.readthedocs.io/en/latest/

while True:
    #Requests TXT file from user
    provided_file = input("Please enter the name of your TXT file: ").strip()

    #Checks that the input ends with '.txt' (case-insensitive)
    if provided_file.lower().endswith(".txt"):
        break
    else:
        #Custom error message. Feel free to change!
        print("Invalid file. Please enter a file with a .txt extension.")


def read_urls_from_file(file_path):
    #Reads URLs from the provided txt file 
    with open(file_path, 'r', encoding='utf-8') as file:
        urls = file.readlines()
    return [url.strip() for url in urls]
    #Removes newline characters

def get_meta_description(url):
    #Grabs meta description from page
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        #Raises an error for bad responses

        soup = BeautifulSoup(response.text, 'html.parser')
        meta_description = soup.find('meta', attrs={'name': 'description'})

        if meta_description and 'content' in meta_description.attrs:
            return meta_description.attrs['content']
        else:
            return "No meta description found"

    except requests.exceptions.RequestException as e:
        return f"Failed to retrieve: {e}"

def main():
    input_file = provided_file
    #List can be generated at https://www.seowl.co/sitemap-extractor/ then saved as txt file
    #Txt files explained: https://en.wikipedia.org/wiki/Text_file
    output_file = 'meta_descriptions.csv'
    #Make sure not to overwrite your previous file if using script more than once!
    #Make sure to close your previous meta_descriptions.csv file before running the script again

    urls = read_urls_from_file(input_file)

    #Opens the newly created CSV, loops to write data to the file
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        #Writes column headers for CSV
        writer.writerow(['URL', 'Meta Description'])

        for url in urls:
            meta_description = get_meta_description(url)

            #Writes the URL and meta description to CSV
            writer.writerow([url, meta_description])

    print(f"Completed! Your results saved to {output_file}")

if __name__ == '__main__':
    main()
