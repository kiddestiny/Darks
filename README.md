## 项目架构
![image](https://user-images.githubusercontent.com/7627381/47973227-50eef800-e0de-11e8-9571-566ea8114521.png)

## 功能介绍
Darks整合了多项技术，目的是为了简化数据分析和开发处理日常的报表，邮件发送，数据解析，可视化，接口，数据转换等工作：

- 报表开发 
> 邮件发送html或excel格式报表，可采用sql和pandas处理数据，多种数据库连接方式

- 可视化 
> 地理信息接口，3D地图数据可视化，整合superset实现可视化大屏，包含语言和手势控制功能

- 复杂json结构转换
> 把结构复杂或不标准的json数据转换到关系型数据库存储

- 条件规则预警
> 整合自定义算法，设置条件阈值触发预警生成报表

- 规则引擎
> 简易的规则引擎实现部署线下开发的线性模型

-  在线机器学习
> 基于spark和redis-ml的在线实时机器学习部署

- 异构数据转换
> pdf解析，网页爬虫，证件信息提取



## ScreenCasts
![v4](https://user-images.githubusercontent.com/7627381/44331558-5d2ec600-a49c-11e8-9406-ee71ac94b52c.gif)
<img width="1082" alt="2018-08-20 5 16 24" src="https://user-images.githubusercontent.com/7627381/44331788-083f7f80-a49d-11e8-9fad-5668b53ab954.png">




## 目录结构
| 目录 | 内容 | 用途|
|-------------|------------|-------------|
|hdr  |存放hdr图| echarts在渲染实体时可以使用增加物体质感
|js | 存放js库|主要包含了echarts maptalks jquery等常用库和自定义的commonUI等|
|tokens| 存放geo接口和mapbox的token| 需要到相应网站申请,按照固定的格式写在json里，后面会有说明|
|css|样式|通用的mapbox样式，自定义样式 背景图片（加载时）等|
|data|json数据|经度维度地址等业务数据|
|api|接口 批量程序|sse接口服务 批量程序 数据转换提取工具等|
|maptalksx.html|maptalks版本|maptalks版本主页
|mapbox.html/mapbox_test.html|mapbbox版本|mapbox版本主页


## 开发环境部署
#### 申请tokens
Darks依赖外部的geo接口和mapbox瓦片图服务，需要开发者申请自己的帐号获取tokens，步骤如下：

- 登录并注册mapbox：

 https://www.mapbox.com/account/

- 在account页面找到Accesstokens标签页
<img width="1100" alt="2018-11-13 11 37 17" src="https://user-images.githubusercontent.com/7627381/48389483-9fcd0b00-e738-11e8-98e0-636a1239def0.png">
- 复制Accesstokens

- 打开Darks/tokens_demo/mapbox.json粘贴mapbox生成的token
``` json
{"token": "粘贴你的token"}
```

另外我们还需要geoapi的token，这里我们使用高德和qq的api，步骤如下：
- 登录高德开放平台https://lbs.amap.com/ 注册并登录
![image](https://user-images.githubusercontent.com/7627381/48390014-02bfa180-e73b-11e8-8eaa-7aeeba9cfa62.png)
- 在个人中心找到创建应用，选择web服务
- 复制生成的key
- 打开


#### sse server
#### 批量


## 生产环境部署
#### nginx
#### sse server
#### 批量

## 技术依赖



