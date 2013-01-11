##############################################################################
#
# Copyright (c) 2004-2006 TINY SPRL. (http://tiny.be) and Eddy Boer
#                          All Rights Reserved.
#                    Fabien Pinckaers <fp@tiny.Be>
#                    Eddy Boer <tinyerp@EdbO.xs4all.nl>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################
# I used the code of account_coda as base for this module. The module does
# exactly the same thing as account_coda. The difference is the file-layout. 
#
# This filter imports .asc-files (BRI-layout).
#

from osv import fields, osv
import time
import pooler
import conversion
import string



def get_data(self, cr, uid, ids, bankData, bank_statement):
	   
    pool = pooler.get_pool(cr.dbname)


    bal_end = bank_statement['bal_end']
    bank_statement_lines={}
    bank_statements=[]
    line_name = 0
    st_line_name = line_name
    code4 = 0
    bankaccount = ''
    bankaccount = bankData[0][14:35]
    # parse every line in the file and get the right data
    if bankaccount.lower() in bank_statement["acc_number"]:
        for line in bankData:
            if len(line) <= 1:  # the end of the file has an empty line
                continue
            if line[0] != '2' :
                continue
            #else:
                #if line.count("\r") :
                #    pos=line.index("\r")
                #else :
               #     pos=0

                #if pos :
                    #i=pos-1
                    #am2 = am1 = 0
                    #char = line[i]

            st_line_name = line_name
            st_line = {}
            st_line['statement_id']=0
            line_list=line.split('	')
            #st_line['date'] =            
            #st_line['entry_date']=time.strftime('%Y-%m-%d',time.strptime(conversion.str2date(line_list[0]),"%y/%m/%d"))
            #st_line['val_date']=time.strftime('%Y-%m-%d',time.strptime(conversion.str2date(line_list[1]),"%y/%m/%d"))
            st_line['date'] = time.strftime('%d/%m/%y',time.strptime(line_list[0],"%Y/%m/%d"))
            st_line['entry_date']= time.strftime('%Y-%m-%d',time.strptime(line_list[0],"%Y/%m/%d"))
            st_line['val_date']= time.strftime('%Y-%m-%d',time.strptime(line_list[1],"%Y/%m/%d"))
            st_line['partner_id']=0
            st_line['type'] = 'general'
            st_line['name'] = line_list[2]
            st_line['free_comm']= ''
            st_line['ref']=''
            st_line['cntry_number']=''
            st_line['contry_name']=''
     
            if line_list[4] == ' \r' :
                st_line_amt = - conversion.str2float(line_list[3])
                st_line['account_id'] = bank_statement['def_pay_acc']
            else:
            	st_line_amt = conversion.str2float(line_list[4])
                st_line['account_id'] = bank_statement['def_rec_acc']
            
            st_line['amount'] = st_line_amt
            st_line_partner_acc = bankaccount.lower()
            st_line['partner_acc_number'] = ''
            #bank_ids = pool.get('res.partner.bank').search(cr,uid,[('acc_number','=',st_line_partner_acc)])
            
            check_ids = pool.get('account.bank.statement.line').search(cr,uid,[('amount','=',st_line_amt), ('date','=',st_line['entry_date']), ('name','=',line_list[2])])
        
            if not check_ids:   
                bank_statement_lines[line_name]=st_line
                line_name += 1
         #  bank_statements.append(st_line)    
   

     # end if
# end for
      
      
      
      # delete latest row from the list because its an empty row
    if len(bank_statement_lines) >= 1:
        #del bank_statement_lines[ line_name ]  # delete latest row from the list
        for test in bank_statement_lines:
            bank_statements.append(bank_statement_lines[test])
         
      # count the end balance
#      for value in bank_statement_lines:
#         line=bank_statement_lines[value]
#         bal_end += line['amount']

#      bank_statement["balance_end_real"]= bal_end
#      bank_statement["bank_statement_line"]=bank_statement_lines
     
    return bank_statements
                
            
    #end for         
#select distinct b.partner_id, p.ref from res_partner_bank b, res_partner p where b.bank='51' and b.partner_id = p.id
