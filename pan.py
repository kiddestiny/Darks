import os
import pandas as pd
import geoapi.geo as g
import json as json
from db_connects.db_connects import db 
import pandas as pd
db = db()

def get_geo(name):
    try:
        geo = g.GeoQQ()
        longitude, latitude = geo.geocoder(name)
        print('%s \n经度：%f\n纬度：%f\n' % (name, longitude, latitude))
    except:
        return(0,0)
    return(longitude, latitude)

def get_data(sqlname):
    '''
    商户信息读取
    '''
    sqlpath = os.path.join(os.path.dirname(__file__),'sql',sqlname+'.sql')
    sqlfile = open(sqlpath, encoding='utf-8').read()
    return pd.read_sql(sqlfile, db.ENGINE_MYSQL_duckchat)

def shop_transform():
    '''
    商户geo数据构造 先从数据库读取数据，根据地址去外部api查地理位置，再计算转换成前端需要的json格式存成文件，返回值是dataframe给后续调用
    geo的api调用很慢，采用增量模式，已经查过的shop不查
    ''' 
    df_shops = get_data('shop')
    df_shops = df_shops.set_index('shop_id')
    # shops  = 'data/csv/shops.csv'
    # df_shops = pd.read_csv(shops,encoding='utf-8',sep='>')
    # # print(df_shops[['address','城市','company_registered_address']])
    # 读取历史数据
    shops_withgeo = 'data/csv/shops_withgeo.csv'
    df_shops_withgeo = pd.read_csv(shops_withgeo, encoding='utf-8', sep=',',index_col='shop_id')
    # 新增的商户数据   因为在生成shops_withgeo的时候会过滤掉地址为空的数据 因此每次这些数据会在new里面，不用管直接往下执行
    df_shops_new = df_shops.loc[df_shops.index.difference(df_shops_withgeo.index)]
    # print(df_shops_new)

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
        df_shops_new[['longitude','latitude']] = df_shops_new['address'].apply(lambda x: get_geo(x)).apply(pd.Series)

    df_shops_res = pd.concat([df_shops_withgeo,df_shops_new],axis=0)
    #解决concat字段自动排序问题   https://github.com/pandas-dev/pandas/issues/4588
    df_shops_res = df_shops_res.reindex(df_shops_withgeo.columns,axis=1)
    df_shops_res.update(df_shops)
    # dtypes = df_shops_new.dtypes.combine_first(df_shops_withgeo.dtypes)
    # df_shops_res = df_shops_new.combine_first(df_shops_withgeo)
    # for k, v in dtypes.iteritems():
    #     df_shops_res[k] = df_shops_res[k].astype(v)
    df_shops_res.to_csv('data/csv/shops_withgeo.csv')
    # exit()

    '''
    shops_withgeo 处理成最终的json格式
    [{
        "height": 2000,
        "polygon": [[121.47556, 31.19144], [121.47556, 31.20344], [121.46356, 31.20344], [121.46356, 31.19144]]
            },
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
        longitude = x[0]
        latitude = x[1]
        abbreviation = x[2]
        passes = x[3]
        rejects = x[4]
        accepts = x[5]
        ac_amounts = x[6]
        temp = {}
        temp["longitude"] = round(longitude,7)
        temp["latitude"] = round(latitude,7)
        temp["abbreviation"] = abbreviation
        temp["passes"] = int(passes)
        temp["rejects"] = int(rejects)
        temp["accepts"] = int(accepts)
        temp["ac_amounts"] = ac_amounts     
        temp["polygon"] = getSquare([longitude, latitude])
        res.append(temp)
    # 如果加载太慢把数据换成800个 df_shops_withgeo[:800]
    df_shops_res[:][['latitude','longitude','abbreviation','通过数','拒绝数','接受数','接受金额']].apply(construct_json, axis = 1)
    # geo = [121.469560, 31.197440]
    with open('data/d.json','w') as f:
        f.write(str(res).replace('\'','"'))
    return df_shops_res



if __name__ == '__main__':
    df_shops_withgeo = shop_transform()
    exit()
    '''
    用户geo  10w+数据 只跑其中的135000:140000 5000左右的数据  接口有并发量限制
    '''
    # users = 'asset/users.csv'
    # df_users = pd.read_csv(users,encoding='utf-8',sep='>')

    # df_users['address'] = df_users['area_name']+df_users['current_address'].fillna(df_users['company_address'])
    # df_users = df_users[-df_users['address'].isnull()]
    # df_users[['longitude','latitude']] = df_users[138000:140000]['address'].apply(lambda x: get_geo(x)).apply(pd.Series)
    # df_users.to_csv('asset/users_withgeo.csv')
    

    '''
    users_withgeo 处理成最终的json格式
    {
        "type": "FeatureCollection",
        "features": [
        {"type":"Feature","properties":{"fclass":"secondary","name":"West 106th Street","oneway":"B","bridge":"F","tunnel":"F"},"geometry":{"type":"LineString","coordinates":[[121.469560, 31.197440],[121.81700, 31.570000],[121.9910903,31.128485]]}},
        {"type":"Feature","properties":{"fclass":"residential","name":"West 80th Street","oneway":"F","bridge":"F","tunnel":"F"},"geometry":{"type":"LineString","coordinates":[[121.469560, 31.197440],[121.465560, 31.193440]]}},
        {"type":"Feature","properties":{"fclass":"residential","name":"West 84th Street","oneway":"F","bridge":"F","tunnel":"F"},"geometry":{"type":"LineString","coordinates":[[121.469560, 31.197440],[121.49788288,31.7875673]]}},
        {"type":"Feature","properties":{"fclass":"residential","name":"Szold Place","oneway":"F","bridge":"F","tunnel":"F"},"geometry":{"type":"LineString","coordinates":[[121.49753143,31.7265446],[121.4975785,31.72592],[121.4976212,31.725326]]}},
        {"type":"Feature","properties":{"fclass":"residential","name":"La Salle Street","oneway":"B","bridge":"F","tunnel":"F"},"geometry":{"type":"LineString","coordinates":[[121.49568143,31.8126066],[121.49573871,31.8128407],[121.49596274,31.8137561],[121.49596845,31.813781],[121.49598158,31.8138385],[121.4960687,31.814192]]}},
        {"type":"Feature","properties":{"fclass":"unclassified","name":"West 9th Street","oneway":"F","bridge":"F","tunnel":"F"},"geometry":{"type":"LineString","coordinates":[[121.4995914,31.732847],[121.49990143,31.7341472]]}},
        {"type":"Feature","properties":{"fclass":"service","name":"Patchin Place","oneway":"B","bridge":"F","tunnel":"F"},"geometry":{"type":"LineString","coordinates":[[121.4999248,31.734783],[121.49993706,31.7351890]]}}
        ]
    }
    '''
    users_withgeo = 'data/csv/users_withgeo.csv'
    df_users_withgeo = pd.read_csv(users_withgeo, encoding='utf-8', sep=',')

    # print( len(df_users_withgeo[-df_users_withgeo['longitude'].isnull()]) )

    lines = df_users_withgeo[-df_users_withgeo['longitude'].isnull()][-df_users_withgeo['longitude'].isnull()][['id','shop_id','address','longitude','latitude']]
    lines = lines[lines['longitude']>1]

    merge_res = pd.merge(lines,df_shops_withgeo, how='left', left_on='shop_id', right_on='shop_id',left_index=False, right_index=False,copy=True,suffixes=('_user', '_shop'))
    merge_res = merge_res[-merge_res['longitude_shop'].isnull()]
    print(merge_res.dtypes)
    
    merge_res  = merge_res[['id','shop_id','address_user','longitude_user','latitude_user','longitude_shop','latitude_shop']]

    features = []
    def construct_users_json(x):
        id = x[0]
        shop_id = x[1]
        address_user = x[2]
        longitude_user = x[3]
        latitude_user = x[4]
        longitude_shop = x[5]
        latitude_shop = x[6]
        coordinates = [[latitude_user,longitude_user],[latitude_shop,longitude_shop]]
        temp = {"type":"Feature","properties":{"fclass":"secondary","name": address_user,"oneway":"B","bridge":"F","tunnel":"F"},"geometry":{"type":"LineString","coordinates":coordinates}}
        features.append(temp)

    merge_res.apply(construct_users_json, axis=1)

    usres = {
        "type": "FeatureCollection",
        "features": features[:500]
        }

    with open('data/lines.json','w') as f:
        f.write(str(usres).replace('\'','"'))

    # print(lines)

