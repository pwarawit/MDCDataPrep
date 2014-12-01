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

action = sys.argv[1]
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

# for pricelist - read the first line for pricelist name and pricelist version name
if action == 'pricelist':
    pricelist_name = inputlist1[0]['pricelist_name']
    version_name = inputlist1[0]['version_name']

first_line = True

for data in inputlist2:
#     print data['default_code']
    found_matched = False
    for prod_code in inputlist1:
        re_pat = prod_code['prod_code'] + '[B|BL|D|G|M|P|W]{0,2}[0-9]{0,4}P?[1|2|3|4|6|12|24|36|48|60|72]{0,2}[B|BL|D|G|M|P|W]{0,2}$'
        if re.search(re_pat, data['default_code']):
            # Found the matched RE pattern
            packcount_factor = 1
            packcount = re.search(r'(P[2|3|4|6|12|24|36|48|60|72]{1,2}$)', data['default_code'])
            if packcount and not (prod_code['prod_code'] == data['default_code']):
                if int(packcount.group(1)[1:]) > 1:
                    packcount_factor = int(packcount.group(1)[1:])
            
            logmsg = logmsg + data['default_code'] + " matched with " + prod_code['prod_code'] + " multiplied by " + str(packcount_factor) +"\n"
            if action == 'baseprice':
                outputlist.append({'id':data['id'],'default_code':data['default_code'],
                                   'list_price':str(float(prod_code['srp'])*packcount_factor)})
            elif action == 'pricelist' and first_line:
                outputlist.append({'Price List': pricelist_name,
                                   'Name': version_name,
                                   'Price List Items / Rule Name':data['default_code'],
                                   'Price List Items / Product':data['default_code'],
                                   'Price List Items / Sequence': '50',
                                   'Price List Items / Based On': 'Public Price',
                                   'items_id/price_discount': -1,
                                   'items_id/price_surcharge':str(float(prod_code['price'])*packcount_factor)})
                first_line = False
            elif action == 'pricelist':
                outputlist.append({'Price List': '',
                                   'Name': '',
                                   'Price List Items / Rule Name':data['default_code'],
                                   'Price List Items / Product':data['default_code'],
                                   'Price List Items / Sequence': '1',
                                   'Price List Items / Based On': 'Public Price',
                                   'items_id/price_discount': -1,
                                   'items_id/price_surcharge':str(float(prod_code['price'])*packcount_factor)})
            
            found_matched = True
            first_line = False
            break
    
    if not found_matched:
        logmsg = logmsg + data['default_code'] + " DOES NOT FOUND ANY MATCHED \n"

baseprice_header = ["id","default_code","list_price"]
pricelist_header = ["Price List","Name",
                    "Price List Items / Rule Name",
                    "Price List Items / Product", 
                    "Price List Items / Sequence", 
                    "Price List Items / Based On",
                    "items_id/price_discount",
                    "items_id/price_surcharge"
                    ]

if action == 'baseprice':
    fieldname = baseprice_header
elif action == 'pricelist':
    fieldname = pricelist_header
    # Also add the 'default price'
    outputlist.append({'Price List': '',
                                   'Name': '',
                                   'Price List Items / Rule Name': 'Default to Base Price',
                                   'Price List Items / Product': '',
                                   'Price List Items / Sequence': '999',
                                   'Price List Items / Based On': 'Public Price',
                                   'items_id/price_discount': 0,
                                   'items_id/price_surcharge': 0})

outfile = open(outputfile,"wb")
csvwriter = csv.DictWriter(outfile, delimiter=',',fieldnames=fieldname)
csvwriter.writerow(dict((fn,fn) for fn in fieldname))
for row in outputlist:
     csvwriter.writerow(row)
outfile.close()

#print logmsg


