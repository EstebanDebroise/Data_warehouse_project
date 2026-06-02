-- Active: 1780304008398@@127.0.0.1@3306
Drop view if exists vue_ads;
Create view vue_ads as
select *
From dim_ads, dim_date, dim_users, fact_ad_events
where dim_ads.ad_id = fact_ad_events.ad_id
and dim_date.date_id = fact_ad_events.date_id
and dim_users.user_id = fact_ad_events.user_id;