import os
import requests
import xml.etree.ElementTree as ET
import argparse

def download_objects_from_xml(xml_url, download_folder):
    # Download the XML content from the provided URL
    response = requests.get(xml_url)
    if response.status_code != 200:
        print("Failed to fetch XML content.")
        return
    else:
        print("Fetched XML content.")

    # Parse the XML content
    root = ET.fromstring(response.content)

    # Define the namespace used in the XML
    ns = {'ns': 'http://obs.otc.t-systems.com/doc/2016-01-01/'}

    # Create the download folder if it doesn't exist
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

   # print(f"Downloading objects to: {download_folder}, {root.findall('.//ns:Contents', namespaces=ns)}")

   # Iterate through the "Contents" elements
    for content in root.findall('.//ns:Contents', namespaces=ns):
        key_element = content.find("ns:Key", namespaces=ns)
        size_element = content.find("ns:Size", namespaces=ns)
      
        if key_element is not None and size_element.text is not "0":

            print(f"key_element: {key_element.text}, size_element: {size_element.text}")

            key = key_element.text

            # Get the object name from the key to use as the local file name
            file_name = key.split('/')[-1]
            print(f"Downloading: {file_name}")

            # Extract the directory structure from the key
            directory_structure = os.path.dirname(key)
            directory_path = os.path.join(download_folder, directory_structure)

             # Create the directory structure if it doesn't exist
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)

            # Build the URL for the object using the key
            object_url = f"{xml_url}{key}"
            
            # Download the object
            response = requests.get(object_url)
            if response.status_code == 200:
                with open(os.path.join(directory_path, file_name), 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded: {file_name}")
            else:
                print(f"Failed to download: {file_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download objects from XML content")
    parser.add_argument("xml_url", help="URL of the XML content")
    parser.add_argument("--download-folder", default="downloaded_files2", help="Folder to save downloaded files")

    args = parser.parse_args()
    
    download_objects_from_xml(args.xml_url, args.download_folder)

