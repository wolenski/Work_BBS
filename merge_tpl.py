# -*- coding=utf8 -*-
## merge PA tpl files 
## output into one file 
import os
import json
import sys
import copy

############################################################
# @brief compare "MATCH FEATURE" of two templates
# @return True or False
############################################################ 
def is_tpl_equal(exist_tpl, tpl):
    exist_xpaths = copy.deepcopy(exist_tpl["MATCH FEATURE"]["XPATH"])
    xpaths = copy.deepcopy(tpl["MATCH FEATURE"]["XPATH"])
    exist_xpaths.sort()
    xpaths.sort()
    return str(exist_xpaths) == str(xpaths) 

############################################################
# @brief Judge if a template is existing
# @return True or False
############################################################ 
def is_tpl_contained(exist_tpls, tpl):
    for e_tpl in exist_tpls:
        if is_tpl_equal(e_tpl, tpl):
            return True
    return False


############################################################
# @brief merge template files, remove duplicated templates
############################################################ 
def merge_tpl(old_file,current_file, output_file):
    # dict for all tpl
    tpl_dict = {}

    if len(old_file) <= 0:
        old_file = "bbs_tpl"
    elif len(current_file) <=0:
        current_file = "PAGE_TYPE_BBS"

#********************************************************
    print "read old_file start"
    file_to_read = open(old_file, 'r')   
    line_num = 0;    
    for line in file_to_read:
        line_num += 1
        if len(line) == 0:
            break
        else:
            try:
                current_tpl = json.loads(line)
                # get key [string]
                url_pattern = current_tpl["TARGET"]["URL_PATTERN"]
                # get tpl [json array]
                tpls = current_tpl["TPL"]               
                if tpl_dict.has_key(url_pattern):  
                    exist_tpls = tpl_dict[url_pattern]["TPL"]
                    count = len(exist_tpls)
                    for tpl in tpls: 
                        if is_tpl_contained(exist_tpls,tpl):
                            print url_pattern,
                            print line_num
                            continue       
                        # increment NO
                        tpl["NO"]  = count
                        count = count + 1
                        tpl_dict[url_pattern]["TPL"].append(tpl)
                else:
                    tpl_dict[url_pattern] = current_tpl;     
            except Exception, e:
                print line
                break;                  
    file_to_read.close()
#********************************************************
    print "read current_file start"
    file_to_read = open(current_file, 'r')       
    for line in file_to_read:
        if len(line) == 0:
            break
        else:
            try:
                current_tpl = json.loads(line)
                # get key [string]
                url_pattern = current_tpl["TARGET"]["URL_PATTERN"]
                # get tpl [json array]
                tpls = current_tpl["TPL"]               
                if tpl_dict.has_key(url_pattern):  
                    exist_tpls = tpl_dict[url_pattern]["TPL"]
                    count = len(exist_tpls)
                    for tpl in tpls: 
                        if is_tpl_contained(exist_tpls,tpl):
                            continue       
                        # increment NO
                        tpl["NO"]  = count
                        count = count + 1
                        tpl_dict[url_pattern]["TPL"].append(tpl)
                else:
                    tpl_dict[url_pattern] = current_tpl;      
            except Exception, e:
                print line
                break

    file_to_read.close()
#********************************************************
    print "write file start"
    file_to_write = open(output_file, "w")
    for k in tpl_dict.keys():
        # print k
        file_to_write.write(json.dumps(tpl_dict[k], sort_keys=True) + "\n")
    file_to_write.close()

############################################################
# main function
############################################################                                                             
if __name__ == '__main__':
    # merge_tpl(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3])
    merge_tpl("non-generator/page_type_bbs_general","non-generator/a.txt","non-generator/page_type_bbs_general.dict")