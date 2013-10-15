# methods for json format data
import json
import os
import sys


# list for url
url_list = []
tpl_list = {}
#read in url 
file_to_read = open("page_type_bbs_general", 'r')
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
                    url_str = (json.dumps(sample_url)).strip("\"")
                    url_list.append(url_str)
                    print url_str
                    tpl_list[url_str] = line
        except Exception, e:
            print "json parsing error!",
            print count
            sys.exit(0)
            break
file_to_read.close() 
print len(url_list)
#output the url into a file
out_fname = "page_type_bbs_general" + ".succ_url"
file_to_write = open(out_fname,"w")
url_list.sort()
for pat in url_list:
    file_to_write.write(str(pat) + "\n")          
file_to_write.close()

sys.exit(0)

#read in url 
fail_list = []
fail_file = {}
for i in range(1,101+1):
    file_name = "json_html_general/" + str(i) + ".html"
    
    file_to_read = open(file_name, 'r')
    count = 0
    for line in file_to_read:
        if len(line) == 0:
            break
        else:
            try:
                count += 1
                s = json.loads(line)
                url = s["url"]
                url_str = (json.dumps(url)).strip("\"")
                struct_type = s["struct_type"]
                struct_type_str = (json.dumps(struct_type)).strip("\"")
                # print url_str
                if (url_list.count(url_str) > 0) and (struct_type_str != "PAGE_STRUCT"):     
                    # append the url                    
                    fail_list.append(url_str)
                    fail_file[url_str] = file_name
            except Exception, e:
                print "json parsing error!",
                print count,
                print file_name
                # sys.exit(0)
                continue
    file_to_read.close() 

print len(fail_list)
#output the url into a file
out_fname = "page_type_bbs_general" + ".fail_url"
file_to_write = open(out_fname,"w")
fail_list.sort()
for pat in fail_list:
    file_to_write.write(str(pat) + "\t") 

    if fail_file.has_key(str(pat)):
        file_to_write.write(fail_file[str(pat)]) 

    file_to_write.write("\n")

    if tpl_list.has_key(str(pat)):
        file_to_write.write(tpl_list[str(pat)])            
file_to_write.close()

