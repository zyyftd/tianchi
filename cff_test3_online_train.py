# -*- coding: utf-8 -*-
"""
    Analysis the preference of user to merchant for online data by the number of times for shopping.
    1. the exception value
        the data which to delete makes the variance smaller two times
    2. the merchant which the user often goes to is favored by
        if the number of records for the user is less than 10
          the merchant mentioned are labed 1 and versus others for 0
        if the number of records for the user is no less than 10
          the exception value are labeled 1 and others for 0
"""
import numpy as np
import copy as copy

def detect_ex(para1):
    """
        detect the exception value
        @para para1 : the list
        @return ex_arg : the index of exception value
    """
    if sum(para1) >= 10:
        ex_index = []
        para_list = copy.deepcopy(para1)
        while True:
            np_list = np.array(para_list)
            max_arg = np_list.argmax()
            if np_list.var() / np.array([np_list[temp] for temp in range(len(np_list)) if i != max_arg]).var() > 2:
                ex_index.append(max_arg)
                del(para_list[max_arg])
            else:
                break
    else:
        # to do !!!
        # if the records are few, how to define the favored merchant ??
        ex_index = [x for x in range(len(para1))]
        # ex_index = []
    return ex_index


read_date = ' 16-10-25'
test_date = ' 16-10-26'
div_num = 50
file_wr = (open('online_train/user_preference'+test_date+'.csv','w'))
for i in range(div_num):
    file_name = 'online_train/userid'+str(i)+read_date+'.csv'
    user_list = []
    with open(file_name) as file_re:
        mer_count = None
        while True:
            line = file_re.readline().split(',')
            if len(line) == 1:
                break
            """
                line[0] --> user_id
                line[1] --> merchant_id
                line[2] --> action 
                            0 -> clicking
                            1 -> buying
                            2 -> getting coupon
                line[3] --> coupon_id
                            null -> no coupon
                line[4] --> discount_rate
                            x in [0,1] -> discount
                            x:y        -> full x minus y
                            fixed      -> on sale
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
            user_id = int(line[0])
            if user_id not in user_list:
                # when a new user_id is read, analysis last user_id at first
                # analysis this user
                if mer_count != None:
                    mer_list = []
                    num_list = []
                    for k,v in mer_count.items():
                        mer_list.append(k)
                        num_list.append(k)
                    mer = [mer_list[temp] for temp in detect_ex(num_list)]
                    res = str(user_id)+','
                    for temp in mer:
                        res += str(temp) + ','
                    res = res[:-1] + '\n'
                    file_wr.write(res)
                
                # start to record the next user
                user_list.append(user_id)
                # merchant dic : merchant->counting
                mer_count = {}
                merchant = int(line[1])
                mer_count[merchant] = 1
            else:
                # record the data of this user
                merchant = int(line[1])
                if merchant not in mer_count.keys():
                    mer_count[merchant] = 1
                else:
                    mer_count[merchant] += 1
file_wr.close()