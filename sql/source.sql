-- shop 

select odr.shop_id
        ,sbi.address
        ,ifnull(area1.area_name,substr(area.area_name,1,2)) as 城市
        ,sbi.company_registered_address
        ,shop.abbreviation
        ,shop.name
        ,count(odr.id ) as 总计
        ,count(case when approve_state =1 then odr.id end) as 通过数
        ,count(case when approve_state =2 then odr.id end) as 拒绝数
        ,count(case when approve_state =1 and odr.user_accept =1 then odr.id end) as 接受数
        ,concat(round(ifnull(sum(case when approve_state =1 and odr.user_accept =1 then odr.apply_amount end)/100,0),2),'元') as 接受金额
         from  duckchatdb.debit_order odr
        left join shop_basic_info sbi
         on odr.shop_id = sbi.shop_id
        left join shop shop
        on sbi.shop_id = shop.id
        left join duckchatdb.area_info as area				on shop.province_id = area.area_id
        left join duckchatdb.area_info as area1				on shop.city_id = area1.area_id
        where odr.approve_state in (1,2)         -- 1 通过  2拒绝   
        and odr.final_input_state =1   -- 资料填写 
        and odr.debit_level  !=2         -- 2 展期
        and odr.shop_id NOT IN (SELECT id FROM shop WHERE type='TEST')
        -- and shop.id = 19211329
        -- and date(odr.final_input_time) between CURRENT_date()-300 and CURRENT_date()
        group by 1,2,3,4,5,6
        
-- user
select 
odr.id
,odr.current_address
,odr.company_address
,odr.shop_id
,area.area_name
from debit_order odr
left join debit_order_ext as et
on odr.id = et.debit_id
left join shop_basic_info sbi
on odr.shop_id = sbi.shop_id
left join shop shop
on sbi.shop_id = shop.id
left join duckchatdb.area_info as area		
on et.current_address_city_id = area.area_id
where odr.approve_state in (1,2)         -- 1 通过  2拒绝   
and odr.final_input_state =1   -- 资料填写 
and odr.debit_level  !=2         -- 2 展期
and odr.shop_id NOT IN (SELECT id FROM shop WHERE type='TEST')
-- and shop.id = 19211329
-- and date(odr.final_input_time) between CURRENT_date()-300 and CURRENT_date()








