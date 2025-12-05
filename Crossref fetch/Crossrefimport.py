import pandas as pd
import requests

# Function to fetch publication date from CrossRef API using DOI
def fetch_publication_date(doi):
    url = f"https://api.crossref.org/works/{doi}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        publication_date = data['message']['created']['date-time']
        return publication_date
    else:
        return None

# Read DOIs from the CSV file and fetch publication dates
def get_publication_dates_from_csv(file_name):
    data = pd.read_csv(file_name)
    dois = data['doi'].tolist()
#the 'doi' in the above line should be the header of the csv file containg the doi numbers, if you have header name anything other than this, change the above line code in ['doi'] to match with your file.
    publication_dates = {}
    for doi in dois:
        publication_date = fetch_publication_date(doi)
        publication_dates[doi] = publication_date

    return publication_dates

# Function to write DOI and publication date to a new CSV file
def write_to_csv(output_file, data):
    df = pd.DataFrame(list(data.items()), columns=['DOI', 'Publication Date'])
    df.to_csv(output_file, index=False)

# Mention the name and absolute path of the CSV file that contains the DOI numbers and the file where the output must be written.
input_csv_file = 'C:/Users/rupin/Desktop/doi.csv'
output_csv_file = 'C:/Users/rupin/Desktop/output_dates.csv'

# Fetch publication dates
publication_dates = get_publication_dates_from_csv(input_csv_file)

# Write output to a new CSV file
write_to_csv(output_csv_file, publication_dates)


