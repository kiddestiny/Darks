import os
import pandas as pd
import geo as g
import json as json
from db_connects.db_connects import db 
import pandas as pd
from math import radians, cos, sin, asin, sqrt
from datetime import datetime
import time
from urllib import request
db = db()
# from tools.icd import idcard_recognize 

CURR_PATH = os.path.split(os.path.abspath(__file__))[0]
SHOPS_WITHGEO = os.path.join(CURR_PATH,'../data_demo/csv/shops_withgeo_demo.csv')
USERS_WITHGEO = os.path.join(CURR_PATH,'../data_demo/csv/users_withgeo_demo.csv')
D_JSON = os.path.join(CURR_PATH,'../data_demo/d.json')
LINES_JSON = os.path.join(CURR_PATH,'../data_demo/lines.json')

def haversine(lon1, lat1, lon2, lat2): # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
 
    # haversine公式
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # 地球平均半径，单位为公里
    return c * r * 1000

def get_geo(name):
    try:
        geo = g.GeoQQ()
        # geo = g.GeoBaidu()
        latitude, longitude = geo.geocoder(name)
        print('%s \n纬度：%f\n经度：%f\n' % (name, latitude,longitude))
    except Exception as e:
        print(e)
        print('调用异常，给默认00')
        return(0,0)
    return(latitude, longitude)

def get_data(sqlname,id=0):
    '''
    商户信息读取
    '''
    sqlpath = os.path.join(os.path.dirname(__file__),'sql',sqlname+'.sql')
    sqlfile = open(sqlpath, encoding='utf-8').read()
    print(sqlfile.format(id))
    return pd.read_sql(sqlfile.format(id), db.ENGINE_MYSQL_duckchat)

def shop_transform():
    '''
    ''' 
    df_shops_new = pd.read_csv(SHOPS_WITHGEO, encoding='utf-8', sep=',',index_col='shop_id')
    # exit()
    if len(df_shops_new)!=0:
        # 构造地址 采用城市+当前住址或公司地址
        df_shops_new.loc[:,'address'] = df_shops_new['城市'] + df_shops_new['address']\
                                .fillna(df_shops_new['company_registered_address'])\
                                .fillna(df_shops_new['name'])\
                                .fillna(df_shops_new['城市'])
        # 地址为空的去掉
        df_shops_new = df_shops_new[-df_shops_new['address'].isnull()]
        # 调用api获取经纬度(读取shops_withgeo.csv判断是否有新增的机构，如果有调用get_geo)
        df_shops_new[['latitude','longitude']] = df_shops_new['address'].apply(lambda x: get_geo(x)).apply(pd.Series)

    df_shops_res = df_shops_new
    #解决concat字段自动排序问题   https://github.com/pandas-dev/pandas/issues/4588
    # df_shops_res = df_shops_res.reindex(df_shops_withgeo.columns,axis=1)
    # df_shops_res.update(df_shops)
    # dtypes = df_shops_new.dtypes.combine_first(df_shops_withgeo.dtypes)
    # df_shops_res = df_shops_new.combine_first(df_shops_withgeo)
    # for k, v in dtypes.iteritems():
    #     df_shops_res[k] = df_shops_res[k].astype(v)
    df_shops_res.to_csv(SHOPS_WITHGEO)
    # exit()

    '''
    shops_withgeo 处理成最终的json格式
    [{
        "height": 2000,
        "polygon": [[121.47556, 31.19144], [121.47556, 31.20344], [121.46356, 31.20344], [121.46356, 31.19144]] },
    {
    "height": 137,
    "polygon": [
        [121.41766, 31.270552],
        [121.41752, 31.270572],
        [121.41751, 31.270572],
        [121.41745, 31.270569],
    ]
    }
            ]
    '''
    def getSquare(geo, length=0.006):
        res = []
        # print([geo[0]+length, geo[1]-length])
        res.append( [geo[0]+length, geo[1]-length] )
        res.append( [geo[0]+length, geo[1]+length] )
        res.append( [geo[0]-length, geo[1]+length] )
        res.append( [geo[0]-length, geo[1]-length] )
        return res

    res = []
    def construct_json(x):
        # print(x[0])
        latitude = x[0]
        longitude = x[1]
        abbreviation = x[2]
        passes = x[3]
        rejects = x[4]
        accepts = x[5]
        ac_amounts = x[6]
        temp = {}
        temp["latitude"] = round(latitude,7)
        temp["longitude"] = round(longitude,7)
        temp["abbreviation"] = abbreviation
        temp["passes"] = int(passes)
        temp["rejects"] = int(rejects)
        temp["accepts"] = int(accepts)
        temp["ac_amounts"] = ac_amounts     
        temp["polygon"] = getSquare([longitude, latitude])
        res.append(temp)
    # 如果加载太慢把数据换成800个 df_shops_withgeo[:800]
    df_shops_res[:][['latitude','longitude','abbreviation','通过数','拒绝数','接受数','接受金额']].apply(construct_json, axis = 1)
    with open(D_JSON,'w') as f:
        f.write(str(res).replace('\'','"'))  # 把构造好的json写入到d.json
    return df_shops_res

def user_transform(df_shops_withgeo):
    '''
    ''' 
    # 读取历史数据
    df_users_new = pd.read_csv(USERS_WITHGEO, encoding='utf-8', sep=',',index_col='id')
    if len(df_users_new)!=0:
        # 地址用填写的城市名称+当前地址，如果为空用公司地址，都为空用身份证省所在省会城市
        df_users_new.loc[:,'address'] = (df_users_new['area_name']+df_users_new['current_address'].fillna(df_users_new['company_address'])).fillna(df_users_new['idcard_area_name'])
        df_users_new.loc[:,'address'] = df_users_new['address'].str.replace('\'','_').str.replace('"','_').str.replace('{','_').str.replace('}','_')
        df_users_new[['latitude','longitude']] = df_users_new['address'].apply(lambda x: get_geo(x)).apply(pd.Series)
        # print('new')
    # df_users_res = pd.concat([df_users_new,df_users_withgeo], axis=0)
    #解决concat字段自动排序问题   https://github.com/pandas-dev/pandas/issues/4588
    # df_users_res = df_users_res.reindex(df_users_withgeo.columns,axis=1)

    # 计算datesince final_input_time:2018-08-28 17:11:12
    df_users_new['final_input_time'] = pd.to_datetime(df_users_new['final_input_time'])
    df_users_new.loc[:,'datesince'] = df_users_new['final_input_time'].apply(lambda x: (x.date() - datetime.today().date()).days)
    
    
    # df_users_res.update(df_users)
    df_users_new.to_csv(USERS_WITHGEO)
  
    df_users_withgeo = pd.read_csv(USERS_WITHGEO, encoding='utf-8', sep=',')

    # print( len(df_users_withgeo[-df_users_withgeo['longitude'].isnull()]) )

    lines = df_users_withgeo[-df_users_withgeo['longitude'].isnull()][-df_users_withgeo['longitude'].isnull()][['id','shop_id','address','latitude','longitude','datesince']]
    lines = lines[lines['longitude']>1] #把返回（0，0）的过滤掉

    merge_res = pd.merge(lines,df_shops_withgeo, how='left', left_on='shop_id',right_index=True,copy=True,suffixes=('_user', '_shop'))
    # merge_res = merge_res[-merge_res['longitude_shop'].isnuindex
    print(merge_res.dtypes)
    
    merge_res  = merge_res[['id','shop_id','address_user','longitude_user','latitude_user','longitude_shop','latitude_shop','datesince']]

    features = []
    def construct_users_json(x):
        id = x[0]
        shop_id = x[1]
        address_user = x[2]
        longitude_user = x[3]
        latitude_user = x[4]
        longitude_shop = x[5]
        latitude_shop = x[6]
        datesince = x[7]
        coordinates = [[longitude_user,latitude_user],[longitude_shop,latitude_shop]]
        if datesince==0:
            linetype = 'Today'
        elif datesince==-1:
            linetype = 'Yesterday'
        else:
            linetype = 'History'
        temp = {"type":"Feature","properties":{"fclass":"secondary","name": address_user,"oneway":"B","bridge":"F","tunnel":"F"},"geometry":{"type":linetype,"coordinates":coordinates}}
        features.append(temp)

    merge_res.apply(construct_users_json, axis=1)

    usres = {
        "type": "FeatureCollection",
        "features": features[:500]
        }

    with open(LINES_JSON,'w') as f:
        f.write(str(usres).replace('"',"_").replace('\'','"'))    # 先把双引号过滤掉  否则json会出错     py中dict转str是单引号转成js里的json需要转换成双引号
    return df_users_new

def transform_one(debitid):
    '''
    供接口实时调用
    '''
    df_info = get_data('user_one',id=debitid)
    df_info = df_info.set_index('id')
    df_info[['user_latitude','user_longitude']] = df_info['user_address'].apply(lambda x: get_geo(x)).apply(pd.Series)
    df_info[['shop_latitude','shop_longitude']] = df_info['shop_address'].apply(lambda x: get_geo(x)).apply(pd.Series)
    return df_info

def mask(s,h=5,t=12,sn=3,c='*'):
    '''
    保留前h个字符后t个字符中间用sn个c替换
    '''
    return s[:h] + sn*c + s[-t:] 

def run(debitid=0):
    if debitid==0:
        df_shops_withgeo = shop_transform()
        user_transform(df_shops_withgeo)
    else:
        time.sleep(0.5)
        res = transform_one(debitid)
        print(res)
        res = res.loc[debitid]
        res_json = {"debitid":debitid,"shopid":res['shop_id'],"user_address":mask(res['user_address']),"shop_address":mask(res['shop_address']),"final_input_time":res['final_input_time'].strftime("%Y-%m-%d %H:%M:%S"),"abbreviation":res["abbreviation"],"user_name":res["user_name"],"gender":res["gender"],"age":res['age'],"oper_nm":res['oper_nm'],"consumer_apply_amount":res['consumer_apply_amount'],"month_count":res['month_count'],"grade_class":res['grade_class'],"coords":[[res['user_longitude'],res['user_latitude']],[res['shop_longitude'],res['shop_latitude']]]}
        print(res_json)
        return res_json

def run_demo(user_name,gender,demo_address):
    geo = get_geo(demo_address)
    res_json = {"debitid":000,"shopid":000,"user_address":demo_address,"shop_address":demo_address,"final_input_time":"2018-11-12 18:00:00","abbreviation":"测试","user_name":user_name,"gender":gender,"age":"18","oper_nm":"测试测试","consumer_apply_amount":100000,"month_count":12,"grade_class":"A","coords":[[geo[1],geo[0]],[121.417475, 31.211993]]}
    return res_json


if __name__ == '__main__':
   run()
