import PyPDF2

from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("Falconsai/text_summarization")
model = AutoModelForSeq2SeqLM.from_pretrained("Falconsai/text_summarization")
summarizer = pipeline("summarization", model="Falconsai/text_summarization")

# importing all the required modules

# creating a pdf reader object
reader = PyPDF2.PdfReader('../tech_papers/GoogleFileSystem-GFS.pdf')

# print the number of pages in pdf file
print(len(reader.pages))

# print the text of the first page
#print(reader.pages[0].extract_text())
full_sum = []
page = 1
while page < len(reader.pages):
    full_sum.append(summarizer(reader.pages[page].extract_text(), max_length=1000, min_length=200, do_sample=False))
    page +=1


print(full_sum)