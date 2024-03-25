import os
import csv
import xml.etree.ElementTree as ET

def has_us_affiliation(affiliation):
    usa_keywords = ["U.S.A", "U.S", "USA"]
    for keyword in usa_keywords:
        if keyword in affiliation:
            return True
    return False

def has_state_name(affiliation):
    us_states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
]
    for state in us_states:
        if state in affiliation:
            return True
    return False

def has_zipcode(affiliation):
    if any(char.isdigit() for char in affiliation) and len([char for char in affiliation if char.isdigit()]) == 6:
        return True
    return False

def extract_us_articles(xml_files, csv_file):
    us_articles = []

    for xml_file in xml_files:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for article in root.findall(".//PubmedArticle"):
            affiliations = [affiliation.text for affiliation in article.findall(".//AffiliationInfo/Affiliation")]
            for affiliation in affiliations:
                if has_us_affiliation(affiliation) or has_state_name(affiliation) or has_zipcode(affiliation):
                    pubmed_id = article.findtext("./MedlineCitation/PMID", "")
                    title = article.findtext(".//Article/ArticleTitle", "")
                    us_articles.append({"PubMedID": pubmed_id,"Article_Title":title})
                    break  # Break loop if US affiliation found

    # Store US articles to CSV
    with open(csv_file, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["PubMedID","Article_Title"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header to the CSV file
        writer.writeheader()

        # Iterate through US articles and write to CSV
        for article in us_articles:
            writer.writerow(article)

if __name__ == "__main__":
    xml_files_path = "C:\\Users\\Patron\\Downloads\\pubmed_res"
    csv_file_path = os.path.join(xml_files_path, "us_articles.csv")

    # List all XML files in the specified directory
    #xml_files = [os.path.join(xml_files_path, file) for file in os.listdir(xml_files_path) if file.endswith(".xml")]

    xml_files=["one_pub_article.xml"]

    # Call the function to extract articles with US affiliation and store PMID and Grant IDs in CSV
    extract_us_articles(xml_files, csv_file_path)
