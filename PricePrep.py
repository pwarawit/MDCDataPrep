import sys
import time
import csv
import re

'''
PricePrep.py
'''
usage_msg = '''
usage: action, input1, input2, output
action: ['help','usage','baseprice','pricelist']
'''

action_list = ['help','usage','baseprice','pricelist']
if len(sys.argv) < 2:
    print usage_msg
    exit()
if sys.argv[1] not in action_list or sys.argv[1] in ['help','usage']:
    print usage_msg
    exit()

inputfile1 = sys.argv[2]
inputfile2 = sys.argv[3]
outputfile = sys.argv[4]

# Check for input files exists

inputlist1 = []
inputdata1 = csv.DictReader(open(inputfile1))
for row in inputdata1:
    inputlist1.append(row)

inputlist2 = []
inputdata2 = csv.DictReader(open(inputfile2))
for row in inputdata2:
    inputlist2.append(row)

outputlist =[]

logmsg = ""

for data in inputlist2:
#     print data['default_code']
    found_matched = False
    for prod_code in inputlist1:
        re_pat = prod_code['prod_code'] + '[B|BL|D|G|M|P|W]{0,2}[0-9]{0,4}P?[1|2|3|4|6|12]{0,2}[B|BL|D|G|M|P|W]{0,2}$'
        if re.search(re_pat, data['default_code']):
            packcount_factor = 1
            packcount = re.search(r'(P[2|3|4|6|12]{1,2}$)', data['default_code'])
            if packcount:
                if int(packcount.group(1)[1:]) > 1:
                    packcount_factor = int(packcount.group(1)[1:])
            
            logmsg = logmsg + data['default_code'] + " matched with " + prod_code['prod_code'] + " multiplied by " + str(packcount_factor) +"\n"
            outputlist.append({'id':data['id'],'default_code':data['default_code'],'list_price':str(int(prod_code['srp'])*packcount_factor)})
            found_matched = True
            break
    
    if not found_matched:
        logmsg = logmsg + data['default_code'] + " DOES NOT FOUND ANY MATCHED \n"

baseprice_header = ["id","default_code","list_price"]

outfile = open(outputfile,"wb")
csvwriter = csv.DictWriter(outfile, delimiter=',',fieldnames=baseprice_header)
csvwriter.writerow(dict((fn,fn) for fn in baseprice_header))
for row in outputlist:
     csvwriter.writerow(row)
outfile.close()

#print logmsg


