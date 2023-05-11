import urllib, urllib.request
from bs4 import BeautifulSoup
import arxiv
import requests
import io
import PyPDF2

def find_professor_papers(url):
    with urllib.request.urlopen(url) as response:
        soup = BeautifulSoup(response, "lxml")

    pdf_urls_prof = list(map(lambda x: x.text + '.pdf', soup.find_all('id')))
    del pdf_urls_prof[0]
    urls_to_remove = list([pdf_urls_prof[15], pdf_urls_prof[33]])
    for url_rm in urls_to_remove:
        pdf_urls_prof.remove(url_rm)

    return pdf_urls_prof

def find_topic_papers(keyword, max_results):
    search = arxiv.Search(query=keyword, max_results=max_results, sort_by=arxiv.SortCriterion.SubmittedDate)
    pdf_urls = list()
    for result in search.results():
        pdf_urls.append(result.pdf_url + ".pdf")

    return pdf_urls

def scrap_pdf(url, keyword, max_results):
    prof_urls = find_professor_papers(url)
    pdf_urls = find_topic_papers(keyword, max_results)
    pdf_urls.extend(prof_urls)

    papers = list()

    for pdf_url in pdf_urls:
        response = requests.get(pdf_url)
        content = response.content
        file = io.BytesIO(content)
        pdf_reader = PyPDF2.PdfReader(file)
        page = pdf_reader.pages[0]  # Get the first page
        text = page.extract_text()
        papers.append(text)

    with open("papers.txt", "w") as f:
        f.writelines(papers)

    if __name__ == "__main__":
        scrap_pdf('https://export.arxiv.org/api/query?search_query=au:robert+koenig&cat:quant-ph&start=0&max_results=59', "quantum", 300)
