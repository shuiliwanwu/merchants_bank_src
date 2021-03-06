# -*- coding: utf-8 -*-
# @Date    : 2018-06-17 16:26:14
# @Author  : GEFE (gh_efe@163.com)
# @Version : 1.0.0
# @Describe : 简单模型训练训练集

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression,Ridge
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier


# common_path = r'~/Documents/Study/Python/merchants_bank/'
common_path = r'~/Documents/merchants_bank'
# train 
train_agg_path = common_path + r'/data/corpus/output/train_agg.csv'
# merge_evt3
train_usrid_merge_evt3_path = common_path + r'/data/feature/train_usrid_merge_evt3.csv'
train_pre_usrid_merge_evt3_path = common_path + r'/data/feature/train_pre_usrid_merge_evt3.csv'
# log_count
train_log_count_path = common_path + r'/data/feature/train_log_count.csv'
train_pre_log_count_path = common_path + r'/data/feature/train_pre_log_count.csv'

# time_feat
train_time_path = common_path + r'/data/feature/train_time.csv'
train_pre_time_path = common_path + r'/data/feature/train_pre_time.csv'

# train_log_path = r'/data/corpus/train_log.csv'
train_flg_path = common_path + r'/data/corpus/output/train_flg.csv'

# tfidf
train_tfidf_path = common_path + r'/data/feature/train_tfidf.csv'

# time two
train_time_two_path = common_path + r'/data/Final_time.csv'
# last time
last_time_path = common_path + r'/data/all_lasttime_feature.csv'
# max click
max_click_path = common_path +r'/data/all_lasttime_feature.csv'


# temp
train_temp = common_path + r'/data/feature/trian_temp.csv'

# test
test_agg_path = common_path + r'/data/corpus/output/test_agg.csv'
# merge_evt3
test_usrid_merge_evt3_path = common_path + r'/data/feature/test_usrid_merge_evt3.csv'
test_pre_usrid_merge_evt3_path = common_path + r'/data/feature/test_pre_usrid_merge_evt3.csv'
# log_count
test_log_count_path = common_path + r'/data/feature/test_log_count.csv'
test_pre_log_count_path = common_path + r'/data/feature/test_pre_log_count.csv'
# time_feat
test_time_path = common_path + r'/data/feature/test_time.csv'
test_pre_time_path = common_path + r'/data/feature/test_pre_time.csv'
# time two
test_time_two_path = common_path + r'/data/Final_Test_Time.csv'


# temp
test_temp = common_path + r'/data/feature/test_temp.csv'

# tfidf
test_tfidf_path = common_path + r'/data/feature/test_tfidf.csv'

result_path = common_path + r'/data/corpus/output/test_result6.csv'

def pre_proba_to_csv(pre_proba):
    
    # 获取测试集的USRID
    test_agg_usrid_data = pd.read_csv(test_agg_path)['USRID']
    # 将概率转化为DataFrame
    result_data_pre = pd.DataFrame(pre_proba, columns=['RST'])
    # 合并概率和USRID为DataFrame
    result_data = pd.concat([test_agg_usrid_data, result_data_pre],axis=1)

    print(result_data[:10])
    # 存储结果
    result_data.to_csv(result_path, index=0, sep='\t')


if __name__ == '__main__':
    # 读取训练集
    train_agg_data = pd.read_csv(train_agg_path)
    # 读取evt3
    train_usrid_merge_evt3_data = pd.read_csv(train_usrid_merge_evt3_path)
    train_pre_usrid_merge_evt3_data = pd.read_csv(train_pre_usrid_merge_evt3_path)
    # train_both_usrid_merge_evt3_data = pd.concat([train_usrid_merge_evt3_data, train_pre_usrid_merge_evt3_data],axis=0)

    train_df = pd.merge(train_agg_data,train_usrid_merge_evt3_data, how='left', on='USRID')
    # train_df = pd.merge(train_agg_data,train_both_usrid_merge_evt3_data, how='left', on='USRID')
    train_dt_tmpe = train_df.fillna(0)
    
    # '''
    # 添加count 
    train_log_count_data = pd.read_csv(train_log_count_path)
    # agg evt3 + log_count
    train_df = pd.merge(train_df, train_log_count_data, how='left', on='USRID')
    
    # 没有count的填充平均数
    # print(train_df['LOG_COUNT'][1])
    # median_count = get_median(list(train_df['LOG_COUNT']))
    train_dt_tmpe = train_df.fillna(0)

    avg_count = sum(list(train_dt_tmpe['LOG_COUNT']))/len(list(train_dt_tmpe['LOG_COUNT']))
    # print('median is ', median_count)
    train_df = train_df.fillna(avg_count)

    # 添加单位时间点击的平均数
    # 取出单位时间点击的平均数
    train_time_data =  pd.read_csv(train_time_path)

    train_df = pd.merge(train_df, train_time_data, how='left', on='USRID')
    # 没有time 的填充0
    train_df = train_df.fillna(0)
    '''
    # log_count 
    train_log_count_data = pd.read_csv(train_log_count_path)
    train_pre_log_count_data = pd.read_csv(train_pre_log_count_path)
    train_both_log_count_data = pd.concat([train_log_count_data, train_pre_log_count_data], axis=0)

    train_df = pd.merge(train_df, train_both_log_count_data, how='left', on='USRID')

    # time
    train_time_data = pd.read_csv(train_time_path)
    train_pre_time_data = pd.read_csv(train_pre_time_path)
    train_both_time_data = pd.concat([train_time_data, train_pre_time_data], axis=0)

    train_df = pd.merge(train_df, train_both_time_data, how='left', on='USRID')

    '''
    # 添加tfidf
    train_tfidf_data = pd.read_csv(train_tfidf_path)

    train_df = pd.merge(train_df, train_tfidf_data, how='left',left_on='USRID',right_on='0')
    train_df = train_df.fillna(0)

    # -----------------------------------------------------------
    # 添加点击天数/点击总数的特征
    train_time_two_data = pd.read_csv(train_time_two_path)
    train_df = pd.merge(train_df, train_time_two_data, how='left', on='USRID')
    train_df = train_df.fillna(0)


    # -----------------------------------------------------------
    # 最后一次点击次数
    train_last_time_data = pd.read_csv(last_time_path)
    train_df = pd.merge(train_df, train_last_time_data, how='left', on='USRID')
    train_df = train_df.fillna(0)



    # -----------------------------------------------------------
    # 最高点击频率
    train_max_click_data = pd.read_csv(max_click_path)
    train_df = pd.merge(train_df, train_max_click_data, how='left', on='USRID')
    train_df = train_df.fillna(0)

    train_df.to_csv(train_temp,index=0)


    # Y
    train_flg_data = pd.read_csv(train_flg_path)

    # 读取测试集
    test_agg_data = pd.read_csv(test_agg_path)

    # merge_evt3
    test_usrid_merge_evt3_data = pd.read_csv(test_usrid_merge_evt3_path)
    test_pre_usrid_merge_evt3_data = pd.read_csv(test_pre_usrid_merge_evt3_path)
    test_both_usrid_mergr_evt3_data = pd.concat([test_usrid_merge_evt3_data, test_pre_usrid_merge_evt3_data],axis=0)
    # agg + merge_vet3
    test_df = pd.merge(test_agg_data, test_both_usrid_mergr_evt3_data, how='left', on='USRID')
    '''
    # 添加count 
    test_log_count_data = pd.read_csv(test_log_count_path)
    # agg evt3 + log_count
    test_df = pd.merge(test_df, test_log_count_data, how='left', on='USRID')
    
    # 没有的填充平均数
    # print(test_df['LOG_COUNT'][1])
    # median_count = get_median(list(test_df['LOG_COUNT']))
    test_dt_tmpe = test_df.fillna(0)

    avg_count = sum(list(test_dt_tmpe['LOG_COUNT']))/len(list(test_dt_tmpe['LOG_COUNT']))
    # print('median is ', median_count)
    test_df = test_df.fillna(avg_count)

    # 添加单位时间点击的平均数
    # 取出单位时间点击的平均数
    test_time_data =  pd.read_csv(test_time_path)

    test_df = pd.merge(test_df, test_time_data, how='left', on='USRID')
    # 没有time 的填充0
    test_df = test_df.fillna(0)
    '''
    # log_count 
    test_log_count_data = pd.read_csv(test_log_count_path)
    test_pre_log_count_data = pd.read_csv(test_pre_log_count_path)
    test_both_log_count_data = pd.concat([test_log_count_data, test_pre_log_count_data], axis=0)

    test_df = pd.merge(test_df, test_both_log_count_data, how='left', on='USRID')

    # time
    test_time_data = pd.read_csv(test_time_path)
    # test_pre_time_data = pd.read_csv(test_pre_time_path)
    # test_both_time_data = pd.concat([test_time_data, test_pre_time_data], axis=0)

    test_df = pd.merge(test_df, test_time_data, how='left', on='USRID')
    test_df.fillna(0)

    # 添加tfidf
    test_tfidf_data = pd.read_csv(test_tfidf_path)

    test_df = pd.merge(test_df, test_tfidf_data, how='left',left_on='USRID',right_on='0')
    test_df = test_df.fillna(0)

    # -----------------------------------------------------------
    # 添加点击天数/点击总数的特征
    test_time_two_data = pd.read_csv(test_time_two_path)
    test_df = pd.merge(test_df, test_time_two_data, how='left', on='USRID')
    test_df = test_df.fillna(0)


    # -----------------------------------------------------------
    # 最后一次点击次数
    test_last_time_data = pd.read_csv(last_time_path)
    test_df = pd.merge(test_df, test_last_time_data, how='left', on='USRID')
    test_df = test_df.fillna(0)



    # -----------------------------------------------------------
    # 最高点击频率
    test_max_click_data = pd.read_csv(max_click_path)
    test_df = pd.merge(test_df, test_max_click_data, how='left', on='USRID')
    test_df = test_df.fillna(0)



    test_df.to_csv(test_temp,index=0)

    # 删除USRID
    train_df.pop('USRID')
    X = train_df.as_matrix()

    train_flg_data.pop('USRID')
    Y = train_flg_data.as_matrix()

    test_df.pop('USRID')
    x_test = test_df.as_matrix()

    # 训练模型
    print('model is begin')
    # xgb_model = XGBClassifier(booster = 'gbtree',
            #   objective = 'binary:logistic',
            #   eta = 0.02,
            #   max_depth = 4,  # 4 3
            #   colsample_bytree = 0.8,#0.8
            #   subsample = 0.7,
            #   min_child_weight = 9,  # 2 3
            #   silent=1)
    print('X shape', X.shape)
    print('X columns', train_df.columns)

    print('Y shape', Y.shape)

    print('x_test shape', x_test.shape)
    print('x_test columns', test_df.columns)

    xgb_model = XGBClassifier(learning_rate=0.01,max_depth=4,n_estimators=800,n_jobs=4)
    
    xgb_model.fit(X, Y)
    y_pre_proba = xgb_model.predict_proba(x_test)[:, 1:]

    # xgb_model = XGBClassifier(silent=1, max_depth=10, n_estimators=1000, learning_rate=0.05)
    # xgb_model.fit(X, Y)
    # y_pre_proba = xgb_model.predict_proba(x_test)
    print('model is end')

    # 取出训练到概率并存入文件
    pre_proba_to_csv(y_pre_proba)
    