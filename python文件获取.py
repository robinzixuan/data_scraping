# -*- coding: utf-8 -*-
"""
Created on Mon May 22 14:28:20 2017

@author: admin
"""

from urllib import request
import re
import psycopg2
conn = psycopg2.connect(database="", user="postgres", password="postgres", host="192.168.10.80", port="5432")
cur = conn.cursor()
cur.execute("CREATE TABLE result(id serial PRIMARY KEY,Name varchar(32),Status varchar(32),Description text,Refer text,Phase text,other text);")
def tablewrite(n,b,c,d,e,f):
    cur.execute("INSERT INTO test(Name,Status,Description,Refer,Phase,other)VALUES(%s, %s, %s, %s, %s, %s)", (n,b,c,d,e,f))
D=dict()
list2=[]
file=open("allitems1.txt",'r')
fp=''
f=open('result4.txt',"w")
for line in file:
        list1=line.strip().split()
        if "Name:" in list1:
            a=''
            a=list1[1]
            D[a]=dict()
            list2.append(list1[1])
        else:
            if "======================================================" in list1:
                pass
            elif line=="\n":
                pass
            elif "Status:" in list1:
                D[a]['Status']=list1[1]
            elif "Reference:" in list1:
                if "Reference:" not in D[a]:
                    D[a]["Reference"]=line[11:]
                else:
                    D[a]["Reference"]+="\,"+line[11:]
            else:
                if 'other' not in D[a]:
                    D[a]['other']=line[:-1]
                else:
                    D[a]['other']+="\,"+line[:-1]
file.close()
for n in list2:
    response = request.urlopen(r'http://cve.mitre.org/cgi-bin/cvename.cgi?name='+n) 
    page = response.read()
    page = page.decode('utf-8')    
    page.replace(" ","").replace("\t","").replace("\n", "").strip()
    reg2 = r'<td><b>([\s\S]+?)</b></td>'
    imgre2 = re.compile(reg2)
    imglist2 = re.findall(imgre2, page)
    D[n]['Date Entry Created']=str(imglist2)
    reg3 = r'''Description</th>\s*</tr>\s*\<tr>\s*<td colspan=\"2\"\>([\s\S]+?)\</td>\s*</tr>'''
    imgre3 = re.compile(reg3)
    imglist3 = re.findall(imgre3, page)
    D[n]['Description']=str(imglist3)    
str1="{:<15s},{:<20s},{:<500s},{:100s},{:<500s},{:<500s}".format('Name','Status','Description','Date Entry Created','Reference','other')+'\n'
for n in list2:
   tablewrite(n,D[n]['Status'],D[n]['Description'],D[n]['Reference'],D[n]['Date Entry Created'],D[n]['other'])
   data_str=''
   if 'Status' in D[n]:
            data_str+=",{:<20s}".format(D[n]['Status'])
   else:
            data_str+=",{:<20s}".format(" ")
   if 'Description' in D[n]:
            data_str+=",{:<500s}".format(D[n]['Description'])
   else:
            data_str+=",{:<500s}".format(" ")
   if 'Date Entry Created' in D[n]:
            data_str+=",{:<100s}".format(D[n]['Date Entry Created'])
   else:
            data_str+=",{:<100s}".format(" ") 
   if 'Reference' in D[n]:
            data_str+=",{:<500s}".format(D[n]['Reference'])
   else:
            data_str+=",{:<500s}".format(" ") 
   if 'other' in D[n]:
            data_str+=",{:<500s}".format(D[n]['other'])
   else:
            data_str+=",{:<500s}".format(" ") 
   str1+="{:<15s}".format(n)+data_str+'\n'
 
    
    

fp=str1      
f.write(fp)
file.close()
f.close()          