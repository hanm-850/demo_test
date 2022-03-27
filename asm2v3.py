""" Created on 27.Mar.2022 by @author: Manhha """

import os
import numpy as np
import pandas as pd
#Task1 ------------------------------------------------------------------------
Dinh_dang_khoang_cach = 68
print(' MANHHA - ASM2 - DSP301 '.center(Dinh_dang_khoang_cach, '='),'\n')
# Tạo hàm mở file

def open_file(file_name):

    print('Enter a class to grade :', file_name)
    try: 
        file_location = os.path.dirname(os.path.abspath(__file__))
        f_read = open(file_location + '/' + file_name, mode = 'r')
        f_read.close()
        print('Successfully opened', file_name)
        check_file = 'success'
    except:
        print('Sorry, file cannot be found.!')
        check_file = 'unsuccess'
    return check_file
# Tạo hàm đọc file

def read_file(file_name):

    file_location = os.path.dirname(os.path.abspath(__file__))
    f_read = open(file_location + '/' + file_name, mode = 'r')
    data = f_read.readlines()
    f_read.close()
    return [file_location, data]
#Task2 ------------------------------------------------------------------------
# Tạo hàm chạy nội dung chính

def main(file_name):

    file_location, data = read_file(file_name)
    # Tạo biến danh sách ID lỗi loại 1, 2, 3
    invalid_index1 = list(); invalid_index2 = list(); invalid_index3 = list()
    valid_index = list() # Danh sách ID không bị lỗi
    # Kiểm tra danh sách học sinh bị sai mã
    so_luong_hs_sai_mhs = 0
    for i in range(len(data)):
        if data[i].find(',') != 9 or data[i][0] != 'N' :
            so_luong_hs_sai_mhs += 1
            invalid_index1.append(i)
    # Kiểm tra danh sách học sinh bị thừa thiếu kết quả kiểm tra
    so_luong_hs_thua_kq, so_luong_hs_thieu_kq, so_luong_hs_du_kq = [0,0,0]
    for i in range(len(data)):
        count_comma = 0
        if i in invalid_index1: continue
        for j in data[i]:
            if j == ',': count_comma +=1 # Đếm số lượng dấu phảy trong 1 dòng
        if count_comma >= 26:
            so_luong_hs_thua_kq += 1
            invalid_index2.append(i)
        elif count_comma == 25:
            so_luong_hs_du_kq += 1
            valid_index.append(i)
        else : # Trường hợp còn lại count_comma <= 24
            so_luong_hs_thieu_kq += 1
            invalid_index3.append(i)
    # Xuất kết quả ra màn hình
    #2.1 Báo cáo tổng số dòng dữ liệu được lưu trữ trong tệp.
    print('\n'+' ANALYZING  '.center(Dinh_dang_khoang_cach,'='))
    if so_luong_hs_sai_mhs+so_luong_hs_thua_kq+so_luong_hs_thieu_kq == 0:
        print('No errors found!\n')
    else:
        for x in invalid_index1:
            print('Invalid line of data: N# is invalid\n   ' , data[x])
        for y in invalid_index2:
            print('Invalid line of data: does not contain exactly 26 values:\n   ' , data[y])
        for z in invalid_index3:
            print('Invalid line of data: does not contain exactly 26 values:\n   ' , data[z])
    #2.2 Báo cáo tổng số dòng dữ liệu không hợp lệ trong tệp.
    print(' REPORT '.center(Dinh_dang_khoang_cach , '='))
    canh_le = 30
    #print('Total line data in this file:'.ljust(canh_le), len(data))
    #print('Inside :')
    print('Total valid lines of data:'.ljust(canh_le) , so_luong_hs_du_kq)
    print('Total invalid lines of data:'.ljust(canh_le) ,\
        so_luong_hs_sai_mhs + so_luong_hs_thua_kq+so_luong_hs_thieu_kq)

    #Task3 ------------------------------------------------------------------------

    # Đọc file thành dạng bảng kết quả kiểm tra
    so_hs = len(data)
    bang_kqkt = list()
    kq_hs = list()
    for i in range(so_hs):
        kq_hs = data[i].replace('\n','').split(',')
        bang_kqkt.append(kq_hs)
    # Đọc file thành dạng bảng kết quả kiểm tra
    so_hs = len(data)
    bang_kqkt = list()
    kq_hs = list()
    for i in range(so_hs):
        kq_hs = data[i].replace('\n','').split(',')
        bang_kqkt.append(kq_hs)
    # Chuyển bảng kết quả thành DataFrame
    df_kqkt = pd.DataFrame(bang_kqkt)
    names = df_kqkt.columns.tolist()
    names[names.index(0)] = 'Ma_hoc_sinh'  #Đổi tên cột cho dễ nhìn
    df_kqkt.columns = names
    # Xóa các hàng cột bị sai dữ liệu
    invalid_index = invalid_index1 + invalid_index2 + invalid_index3
    for i in invalid_index:
        df_kqkt = df_kqkt.drop([i])
    if df_kqkt.shape[1] == 28: df_kqkt = df_kqkt.drop(27, axis = 1)
    if df_kqkt.shape[1] == 27: df_kqkt = df_kqkt.drop(26, axis = 1)
    # Chuyển đáp án thành list để đối chiếu
    answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"
    answer_key = ['Ma_hoc_sinh'] + answer_key.split(',')
    #Đối chiếu đáp án với câu trả lời để chấm điểm học sinh
    for row in range(df_kqkt.shape[0]):
        for col in range(1,df_kqkt.shape[1]):
            df_kqkt[col] = df_kqkt[col].replace({answer_key[col]: 4, '': 0})
            df_kqkt[col] = df_kqkt[col].replace({'A':-1, 'B':-1, 'C':-1, 'D':-1})
    # Thêm cột tổng điểm vào cuối bảng
    ds_kq = list(x for x in range(1,26))
    df_kqkt['Tong_diem'] = df_kqkt[ds_kq].sum(axis = 1)
    # 3.1. Đếm số lượng học sinh đạt điểm cao (>80)
    so_luong_hoc_sinh_dat_diem_cao = df_kqkt['Tong_diem']\
        [df_kqkt['Tong_diem'] > 80].count()
    print('Total student of high scores: '.ljust(canh_le) ,\
        so_luong_hoc_sinh_dat_diem_cao)
    # 3.2. Điểm trung bình
    diem_trung_binh = df_kqkt['Tong_diem'].mean()
    print('Average score : '.ljust(canh_le),round(diem_trung_binh,3))
    #3.3. Điểm cao nhất.
    diem_cao_nhat = df_kqkt['Tong_diem'].max()
    print('Highest score : '.ljust(canh_le),diem_cao_nhat)
    #3.4. Điểm thấp nhất.
    diem_thap_nhat = df_kqkt['Tong_diem'].min()
    print('Lowest score : '.ljust(canh_le),diem_thap_nhat)
    #3.5. Miền giá trị của điểm (cao nhất trừ thấp nhất)
    mien_gia_tri_cua_diem = diem_cao_nhat - diem_thap_nhat
    print('Range of scores: '.ljust(canh_le),mien_gia_tri_cua_diem)
    #3.6. Giá trị trung vị
    gia_tri_trung_vi = df_kqkt['Tong_diem'].median()
    print('Median score : '.ljust(canh_le),gia_tri_trung_vi)
    # 3.7. và 3.8
    Question_skip = dict(); Question_incorrect = dict()
    skip_max, incorrect_max = [0,0]
    for i in range(1,26):
        a = df_kqkt[names[i]].value_counts()
        #print(i, dict(a))
        try:
            Question_skip[i] = dict(a)[0]
            Question_incorrect[i] = dict(a)[-1]
            if dict(a)[0] > skip_max : skip_max = dict(a)[0]
            if dict(a)[-1] > incorrect_max : incorrect_max = dict(a)[-1]
        except: continue
    # 3.7. Trả về các câu hỏi bị học sinh bỏ qua nhiều nhất
    print('Question that most people skip :')
    print('    ', end = ' ')
    for j in range(1,26):
        try: 
            if Question_skip[j] == skip_max:
                print(j,'-',skip_max,'-',\
                    round(skip_max/len(data)*100,3), '%', end = ' , ')
        except: continue
    # 3.8. Trả về các câu hỏi bị học sinh sai qua nhiều nhất
    print('\nQuestion that most people answer incorrectly:')
    print('    ', end = ' ')
    for k in range(1,26):
        try: 
            if Question_incorrect[k] == incorrect_max:
                print(k,'-',incorrect_max,'-',\
                    round(incorrect_max/len(data)*100,3), '%', end = ' , ')
        except: continue

    #Task4 ------------------------------------------------------------------------
    # Tạo một tệp “kết quả” chứa các kết quả chi tiết cho từng học sinh trong lớp
    file_save_name = file_name
    file_save_name = file_save_name.replace('.txt','_grades.txt')
    f = open(file_location+'/'+file_save_name, mode = 'w', encoding = 'UTF8')
    f.write('# This is result of '+str(file_name[0:(len(file_name)-4)])+'\n')
    #print('# This is result of',file_name[0:(len(file_name)-4)])
    for i in range(df_kqkt.shape[0]):
        if i in invalid_index: 
            f.write(str(bang_kqkt[i][0])+', Invalid line of data'+'\n')
            #print(str(bang_kqkt[i][0])+', Invalid line of data')
        else: 
            f.write(str(df_kqkt['Ma_hoc_sinh'][i])+', '\
                +str(df_kqkt['Tong_diem'][i])+'\n')
            #print(str(df_kqkt['Ma_hoc_sinh'][i])+', '+str(df_kqkt['Tong_diem'][i]))
    f.close()
    print('\n\nThe result file name', file_save_name, 'has been creaded')
    print('path to file :\n', file_location+'\\'+file_save_name )
    
#Chạy chương trình chính
while True:
    file_name = input('Enter the file name you want to open (Eg Class1.txt): ')
    #file_name = 'class2.txt'
    lts_answer = ['ok', 'y', 'yes', 'smile', 'of course', 'co']
    open_file_return = open_file(file_name)
    if open_file_return == 'success' : 
        read_file(file_name)
        main(file_name)
        answer = input('\nDo you want to open another file? (Y/N) : ')
        if answer.lower() in lts_answer: continue
        else: break
    elif open_file_return == 'unsuccess':
        answer = input('\nDo you want to open another file? (Y/N) : ')
        if answer.lower() in lts_answer: continue
        else: break
    else: break
print('\nThank you for run the program!')
input()