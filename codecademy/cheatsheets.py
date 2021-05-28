import pdfkit
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfFileReader, PdfFileWriter

class Cheatsheet:
    def __init__(self, url, name):
        self.url = url
        self.name = name
    
    def print_pdf(self):
        pdfkit.from_url(self.url, self.name)

def get_cheatsheets(url,linkWraper):
    r = requests.get(url)
    sdata = r.text
    soup = BeautifulSoup(sdata, 'html.parser')
    querys = {} 
    for x in soup.find_all('div', class_=linkWraper):
        for a in x.find_all('a'):
            querys[a.text] = (a['href'])
    return querys

url = "https://www.codecademy.com/learn/learn-python-3/modules/learn-python3-hello-world/cheatsheet"
linkWraper = "linkWrapper__fSkTpr-PwWiQBjUt_Q_bh hideCourseUnits__B4LXspzwokIdJHXQPyEth"

querys = get_cheatsheets(url, linkWraper)

paths = []
for key, value in querys.items():
    key = key.replace(" ", "")
    key = key + ".pdf"
    paths.append(key)
    print(key)
    value = "https://www.codecademy.com" + value
    cheatsheet = Cheatsheet(value, key)
    cheatsheet.print_pdf()

def merge_pdfs(paths, output):
    pdf_writer = PdfFileWriter()

    for path in paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))

    # Write out the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)

merge_pdfs(paths, 'cheatsheet.pdf')
