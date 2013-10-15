# methods for json format data
import json
import os
import sys

#########################################################################
# extract SAMPLE URL field from pa xpath template file of json format ##
#########################################################################
def extract_sample_url_from_pa_tpl(file_name):
    # list for url
    url_list = []

    #read in url 
    file_to_read = open(file_name, 'r')
    count = 0
    for line in file_to_read:
        if len(line) == 0:
            break
        else:
            try:
                count += 1
                s = json.loads(line)
                tpls = s["TPL"]
                for tpl in tpls:
                    sample_url_array = tpl["SAMPLE URL"] 
                    for sample_url in sample_url_array:                
                        # append the url
                        url_list.append((json.dumps(sample_url)).strip("\""))
            except Exception, e:
                print "json parsing error!"
                print count
                sys.exit(0)
                break
    file_to_read.close() 
    

    #output the url into a file
    out_fname = file_name + ".sample_url"
    file_to_write = open(out_fname,"w")
    url_list.sort()
    for pat in url_list:
        file_to_write.write(str(pat) + "\n")             
    file_to_write.close()

if __name__ == '__main__':
    extract_sample_url_from_pa_tpl("page_type_bbs_generator")