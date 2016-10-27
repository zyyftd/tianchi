# -*- coding: utf-8 -*-
"""
    handle cff_offline_stage1_train.csv
        1. try to divide it into some pieces by user_id
            maybe we can consider dividing it by merchant_id
        2. try to standardlize the discount_rate by percent
            x:y   ==> (x-y)/x
        3. add a property which identifies wheather the conpon is used
"""

test_date = ' 16-10-26'
div_num = 50
file_wr_list = []
for i in range(div_num):
    file_wr_list.append(open('offline_train/userid'+str(i)+test_date+'.csv','w'))
with open('ccf_offline_stage1_train.csv') as file_re:
    while True:
        line = file_re.readline().split(',')
        if len(line) == 1:
            break
        """
            line[0] --> user_id
            line[1] --> merchant_id
            line[2] --> coupon_id
                        null -> no coupon
            line[3] --> discount_rate
                        x in [0,1] -> discount
                        x:y        -> full x minus y
            line[4] --> distance 
                        null -> no distance information
                        x in [0,10] -> distance
            line[5] --> date_received
            line[6] --> date
                        if data==null && conpon_id!=null:
                            getting conpon without using
                        elif data!=null && conpon_id!=null:
                            the conpon is not used
                        elif data!=null && conpon_id!=null:
                            the conpon is used
                        else:
                            pass
        """
        num = int(line[0]) % div_num
        line[-1] = line[-1][:-1]    # del \n
        if line[2] != 'null' and line[6] != 'null':
            line.append('1\n')
        else:
            line.append('0\n')
        
        # write to the file
        res = ''
        for j in range(len(line)):
            res += line[j] + ','
        res = res[:-1]
        file_wr_list[num].write(res)


# close the file steam
for i in range(div_num):
    file_wr_list[i].close()
