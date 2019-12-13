from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from csv import reader
import csv
import sys

def split_barcode(code):
    n = 10
    chunks = [code[i:i+n] for i in range(0, len(code), n)]
    return chunks

def sort_Barcode_id(my_list):
    composite_list = [my_list[x:x+8] for x in range(0, len(my_list),8)]
    composite_list = [composite_list[x:x+3] for x in range(0, len(composite_list),3)]
    #print(composite_list)
    #print(len(composite_list))
    real_list = []
    a =0
    for page in composite_list:
        for i in range(0,8):
            for y in page:
                try:
                    real_list.append(y[i])
                except:
                    a =1
                    
    return real_list
    
            
def convert_pdf_to_txt(path, Detector):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8' 
    laparams = LAParams()

    #laparams.char_margin = 5
    #laparams.word_margin = 0.5
    laparams.line_margin = Detector
    #rotation = 1
    device = TextConverter( rsrcmgr,retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text
def final_barcode(filename):
    my_list = split_barcode(convert_pdf_to_txt(filename,0).replace('\x0c',''))
    return sort_Barcode_id(my_list)
def create_csv(alist):
    with open('output_file.csv', 'w', newline='') as file:
        writer = csv.writer(file,  delimiter=';')
        writer.writerows(alist)
    
def normalize_text( barcodes , filename):
    data = convert_pdf_to_txt(filename,0.1).split('\n')
    ####################################
    #print(data)
    data_new = []
    for x in range(0,len(data)):
        

        if len(data[x]) >100:
            long = data[x]
            fixed_long = long.split('')[1]
            #print(fixed_long)
            data_new.append(fixed_long)
        if data[x] != '' and len(data[x]) <100:
            data_new.append(data[x])
        
    n = 2
    chunks = [data_new[i:i+n] for i in range(0, len(data_new), n)]
    del chunks[-1]
    for i in range(0,len(chunks)):
        chunks[i].append(barcodes[i])

        ### Sorting to your Indent
        FNSKU = chunks[i][2]
        Description = chunks[i][0]
        state = chunks[i][1]
        chunks[i][0] = FNSKU
        chunks[i][1] = Description
        chunks[i][2] = state
        
    return chunks
    

def Main(name):
    barcode_list = final_barcode(str(name))
    print("Barcode Number Capturing ... !")
    Writing_data = normalize_text(barcode_list,str(name))
    print("Other text Capturing ... !")
    create_csv(Writing_data)
    print("CSV file Done !")
    




if __name__ == '__main__':
    #sys.exit(main(sys.argv))
    sys.exit(Main(sys.argv[1]))
    
    



