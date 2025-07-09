

from typing import List, Dict, Optional
import requests
import re

PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

def search_pubmed(query: str, retmax: int = 20) -> List[str]:
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": str(retmax)
    }
    resp = requests.get(PUBMED_SEARCH_URL, params=params)
    resp.raise_for_status()
    data = resp.json()
    return data["esearchresult"]["idlist"]

def fetch_pubmed_details(pmid_list: List[str]) -> List[Dict]:
    if not pmid_list:
        return []
    params = {
        "db": "pubmed",
        "id": ",".join(pmid_list),
        "retmode": "xml"
    }
    resp = requests.get(PUBMED_FETCH_URL, params=params)
    resp.raise_for_status()
    from xml.etree import ElementTree as ET
    root = ET.fromstring(resp.text)
    papers = []
    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID")
        title = article.findtext(".//ArticleTitle")
        pub_date = article.findtext(".//PubDate/Year") or article.findtext(".//PubDate/MedlineDate")
        authors = []
        for author in article.findall(".//Author"):
            last = author.findtext("LastName") or ""
            first = author.findtext("ForeName") or ""
            affiliation = author.findtext(".//Affiliation") or ""
            email_match = re.search(r'[\w\.-]+@[\w\.-]+', affiliation)
            email = email_match.group(0) if email_match else ""
            authors.append({
                "name": f"{first} {last}".strip(),
                "affiliation": affiliation,
                "email": email
            })
        papers.append({
            "pmid": pmid,
            "title": title,
            "pub_date": pub_date,
            "authors": authors
        })
    return papers

def is_non_academic_affiliation(affiliation: str) -> bool:
    academic_keywords = [
        "university", "institute", "college", "school", "hospital", "faculty", "department", "center", "centre"
    ]
    pharma_keywords = [
        "pharma", "pharmaceutical", "biotech", "inc", "ltd", "gmbh", "s.a.", "corp", "company", "laboratories", "labs"
    ]
    affil_lower = affiliation.lower()
    if any(word in affil_lower for word in pharma_keywords):
        return True
    if any(word in affil_lower for word in academic_keywords):
        return False
    # Heuristic: if contains company-like words and not academic, consider non-academic
    return False

def extract_non_academic_authors(authors: List[Dict]) -> List[Dict]:
    return [a for a in authors if is_non_academic_affiliation(a["affiliation"])]

def get_papers_with_non_academic_authors(query: str, retmax: int = 20, debug: bool = False) -> List[Dict]:
    pmids = search_pubmed(query, retmax)
    if debug:
        print(f"Found {len(pmids)} PMIDs")
    papers = fetch_pubmed_details(pmids)
    results = []
    for paper in papers:
        non_acad_authors = extract_non_academic_authors(paper["authors"])
        if non_acad_authors:
            result = {
                "PubmedID": paper["pmid"],
                "Title": paper["title"],
                "Publication Date": paper["pub_date"],
                "Non-academic Author(s)": "; ".join(a["name"] for a in non_acad_authors),
                "Company Affiliation(s)": "; ".join(a["affiliation"] for a in non_acad_authors),
                "Corresponding Author Email": non_acad_authors[0].get("email", "")
            }
            results.append(result)
    return results
