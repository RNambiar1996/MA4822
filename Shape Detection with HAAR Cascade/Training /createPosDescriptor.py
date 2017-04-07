import os

def create_pos():
    for file_type in ['data/pos_corrected_bgRemoved']:
        
        for img in os.listdir(file_type):
	    
		line = file_type+'/'+img+' 1 0 0 60 160\n'
		print line
                with open('people_60_160.info','a') as f:
                    f.write(line)            

create_pos()
