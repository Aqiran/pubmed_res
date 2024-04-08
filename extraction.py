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
    us_states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
    for state in us_states:
        if state in affiliation:
            return True
    return False

def has_zipcode(affiliation):
    if any(char.isdigit() for char in affiliation) and len([char for char in affiliation if char.isdigit()]) == 6:
        return True
    return False

def extract_author_info(author):
    last_name = author.findtext("LastName", "")
    fore_name = author.findtext("ForeName", "")
    initials = author.findtext("Initials", "")
    full_name = f"{fore_name} {last_name}"
    affiliations = [affiliation.text for affiliation in author.findall(".//AffiliationInfo/Affiliation")]
    affiliations_str = " | ".join(affiliations)
    return f"{full_name} - {affiliations_str}"

def extract_authors(article):
    authors = article.findall(".//AuthorList/Author")
    author_info = [extract_author_info(author) for author in authors]
    return author_info

def extract_article_info(article):
    pubmed_id = article.findtext("./MedlineCitation/PMID", "")
    article_title = article.findtext(".//Article/ArticleTitle", "")
    journal_title = article.findtext(".//Article/Journal/Title", "")
    publication_date = extract_publication_date(article)
    authors = extract_authors(article)
    grants = extract_grants(article)
    research_funding = extract_publication_types(article)
    
    return {
        "PubMedID": pubmed_id,
        "Article_Title": article_title,
        "Journal_Title": journal_title,
        "Publication_Date": publication_date,
        "Authors": authors,
        "Research_Funding": research_funding,
        "Grants": grants  # Add grants here
    }

def extract_publication_date(article):
    pub_date_element = article.find(".//Article/Journal/JournalIssue/PubDate")
    year = pub_date_element.findtext("Year", "")
    month = pub_date_element.findtext("Month", "")
    day = pub_date_element.findtext("Day", "")
    medline_date = article.findtext("./MedlineCitation/MedlineDate", "")
    if year or month or day:
        return f"{year}-{month}-{day}"
    elif medline_date:
        return medline_date
    else:
        return ""

def extract_publication_types(article):
    publication_types = article.findall(".//PublicationTypeList/PublicationType")
    research_funding = [pt.text for pt in publication_types if 'Research Support' in pt.text]
    return "| ".join(research_funding)

def extract_grants(article):
    grants = article.findall(".//GrantList/Grant")
    grant_info = [grant.findtext("Agency", "") + ", " + grant.findtext("Country", "") for grant in grants]
    return "| ".join(grant_info)

def extract_us_articles(xml_files):
    us_articles = []

    for xml_file in xml_files:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for article in root.findall(".//PubmedArticle"):
            affiliations = [affiliation.text for affiliation in article.findall(".//AffiliationInfo/Affiliation")]
            for affiliation in affiliations:
                if has_us_affiliation(affiliation) or has_state_name(affiliation) or has_zipcode(affiliation):
                    article_info = extract_article_info(article)
                    us_articles.append(article_info)
                    break  # Break loop if US affiliation found

    return us_articles

def store_articles_to_csv(articles, csv_file):
    with open(csv_file, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["PubMedID", "Article_Title", "Journal_Title", "Publication_Date", "Authors", "Research_Funding", "Grants"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header to the CSV file
        writer.writeheader()

        # Iterate through articles and write to CSV
        for article in articles:
            writer.writerow(article)

if __name__ == "__main__":
    xml_files_path = "C:\\Users\\Patron\\Downloads\\pubmed_res"
    csv_file_path = os.path.join(xml_files_path, "us_articles.csv")

    # List all XML files in the specified directory
    #xml_files = [os.path.join(xml_files_path, file) for file in os.listdir(xml_files_path) if file.endswith(".xml")]

    xml_files = ["one_pub_article.xml"]

    # Extract articles with US affiliation
    us_articles = extract_us_articles(xml_files

)

    # Store articles to CSV
    store_articles_to_csv(us_articles, csv_file_path)
