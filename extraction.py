import os
import json
import csv
import xml.etree.ElementTree as ET

def extract_all_agencies(xml_files, json_file, csv_file):
    all_agencies = []

    for xml_file in xml_files:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for article in root.findall(".//PubmedArticle/MedlineCitation/Article/GrantList/Grant"):
            
            try:
                grant_id = article.findtext("GrantID", "")
                acronym = article.findtext("Acronym", "")
                agency = article.findtext("Agency", "")
                country = article.findtext("Country", "")
                pubmed_id = root.findtext(".//PubmedArticle/MedlineCitation/PMID", "")
                 # Find all PublicationType elements
                publication_types = root.findall(".//PubmedArticle/MedlineCitation/Article/PublicationType")

                # Filter PublicationType elements containing 'Research Support'
                research_support_types = [pt.text for pt in publication_types if 'Research Support' in pt.text]

                # Combine multiple research support types into a single string
                research_support = ', '.join(research_support_types)

                # Append agency information to the list
                all_agencies.append({
                    "Grant ID": grant_id,
                    "Acronym": acronym,
                    "Agency": agency,
                    "Country": country,
                    "PubMedID": pubmed_id,
                    "Reasearch_Support": research_support
                })
            except KeyError:
                pass  # Some articles might not have funding information

    # Save all agencies to a JSON file
    with open(json_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(all_agencies, jsonfile, ensure_ascii=False, indent=4)

    # Extract specific data from the JSON format and store in CSV
    with open(csv_file, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["Grant ID", "Acronym", "Agency", "Country", "PubMedID","Reasearch_Support"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header to the CSV file
        writer.writeheader()

        # Iterate through JSON data and write to CSV
        for agency in all_agencies:
            writer.writerow(agency)

if __name__ == "__main__":
    xml_files_path = "C:\\Users\\Patron\\Downloads\\pubmed_res"
    json_file_path = os.path.join(xml_files_path, "all_funding_data.json")
    csv_file_path = os.path.join(xml_files_path, "selected_funding_data.csv")

    # List all XML files in the specified directory
    #xml_files = [os.path.join(xml_files_path, file) for file in os.listdir(xml_files_path) if file.endswith(".xml")]
    xml_files = ['pubmed24n0002.xml']
    # Call the function to extract all funding agency information and save to JSON and CSV
    extract_all_agencies(xml_files, json_file_path, csv_file_path)
