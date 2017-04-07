import os

def create_neg():
    for file_type in ['Pictures/neg']:
        
        for img in os.listdir(file_type):

             line = file_type+'/'+img+'\n'
             with open('bg.txt','a') as f:
                 f.write(line)

create_neg()
