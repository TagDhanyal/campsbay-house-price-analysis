from bs4 import BeautifulSoup
import csv
import boto3
import os
import datetime

def extract_property_data(html_content):
    import re
    from bs4 import BeautifulSoup

    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract the data from the HTML table
    table = soup.find('table')
    if not table:
        print("No property listings found in the HTML content.")
        return []

    rows = table.find_all('tr')

    # Create a list to store the data
    data = []

    for row in rows:
        # Find all <td> elements in the row
        td_elements = row.find_all('td')
        
        # Check if there are at least two <td> elements in the row
        if len(td_elements) >= 2:
            address = re.sub(r'<[^>]*>|\s+', '', td_elements[0].text)
            price = re.sub(r'<[^>]*>|\s+', '', td_elements[1].text)

            data.append({
                'address': address,
                'price': price
            })

    return data

def write_property_data_to_csv(properties, filename):
    try:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['address', 'price'])

            for property in properties:
                writer.writerow([property['address'], property['price']])
    except Exception as e:
        print(f'Error writing to CSV file: {e}')

def upload_to_s3(file_path, bucket_name, object_key):
    s3 = boto3.client('s3')

    # Upload the file to S3
    s3.upload_file(file_path, bucket_name, object_key)

def function_handler(event, context):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    html_file_path = os.path.join(script_dir, 'data.html')

    # Read the HTML content from the file
    with open(html_file_path, 'rb') as f:
        html_content = f.read()

    properties = extract_property_data(html_content)

    csv_filename = 'property_data.csv'
    write_property_data_to_csv(properties, csv_filename)

    s3_bucket_name = 'dhanyals-lambda-zips'

    # Generate a timestamp
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    # Modify the object key to include the timestamp
    s3_object_key = f'property_data_{timestamp}.csv'

    upload_to_s3(csv_filename, s3_bucket_name, s3_object_key)

    response = {
        'statusCode': 200,  # Modify this as needed
        'body': 'Data uploaded successfully'  # Modify this as needed
    }

    return response