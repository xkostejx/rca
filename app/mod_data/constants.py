class Constants():
	ROLE_USER = 0
	
	ROLE_ADMIN = 1

	SQL_COFFEE_USERS = "SELECT c.user_id, sum(c.price) as price_sum, IFNULL(d.deposit_sum,0) as deposit_sum, count(c.id) as coffee_count, max(c.date_created) as coffee_last, u.fullname as name, (sum(c.price)*-1) + IFNULL(d.deposit_sum,0) as balance, CONCAT(SUBSTRING_INDEX(SUBSTRING_INDEX(u.fullname, ' ', 2), ' ', -1),' ', SUBSTRING_INDEX(SUBSTRING_INDEX(u.fullname, ' ', 1), ' ', -1)) as fullnamerev FROM coffee c LEFT JOIN users u ON c.user_id = u.id LEFT JOIN (SELECT user_id, sum(amount) as deposit_sum FROM deposit GROUP BY user_id) AS d ON c.user_id = d.user_id GROUP BY c.user_id;"

	SQL_PERSONAL_SUMMARY = "SELECT c.user_id, sum(c.price) as price_sum, IFNULL(d.deposit_sum,0) as deposit_sum, count(c.id) as coffee_count, min(c.date_created) as coffee_first, max(c.date_created) as coffee_last, u.fullname as name, (sum(c.price)*-1) + IFNULL(d.deposit_sum,0) as balance, IFNULL(mc.sum_month,0) as sum_month, IFNULL(mt.sum_today,0) as sum_today FROM coffee c LEFT JOIN users u ON c.user_id = u.id LEFT JOIN (SELECT user_id, sum(amount) as deposit_sum FROM deposit GROUP BY user_id) AS d ON c.user_id = d.user_id LEFT JOIN (SELECT user_id, count(id) as sum_month FROM coffee WHERE DATE_FORMAT(date_created,'%m-%Y') = DATE_FORMAT(NOW(),'%m-%Y') GROUP BY user_id) AS mc ON c.user_id = mc.user_id LEFT JOIN (SELECT user_id, count(id) as sum_today FROM coffee WHERE DATE(date_created) = CURDATE() GROUP BY user_id) as mt ON c.user_id = mt.user_id WHERE c.user_id=:userid GROUP BY c.user_id;"
 
	SQL_GLOBAL_SUMMARY = "SELECT ct.coffee_count as coffee_today, cm.coffee_count as coffee_month, co.coffee_count as coffee_overall, (co.price_sum*-1) + do.deposit_sum as balance FROM (SELECT count(id) as coffee_count FROM coffee WHERE DATE(date_created) = CURDATE()) as ct,(SELECT count(id) as coffee_count FROM coffee WHERE DATE_FORMAT(date_created,'%m-%Y') = DATE_FORMAT(NOW(),'%m-%Y')) as cm, (SELECT count(id) as coffee_count, sum(price) as price_sum FROM coffee) as co, (SELECT sum(amount) as deposit_sum FROM deposit) as do"

	SQL_BALANCE_SUMMARY = "SELECT count(c.id) as coffee_count, count(distinct(c.user_id)) as user_count, cm.user_month_count, co.price_sum as price_sum, (co.price_sum*-1) + do.deposit_sum as balance FROM coffee c, (SELECT sum(price) as price_sum FROM coffee) as co, (SELECT sum(amount) as deposit_sum FROM deposit) as do, (SELECT count(distinct(user_id)) as user_month_count FROM coffee WHERE DATE_FORMAT(date_created,'%m-%Y') = DATE_FORMAT(NOW(),'%m-%Y')) cm"

	SQL_USERS = "SELECT * FROM users ORDER BY fullname"
	
	SQL_USERS_BY_SURNAME = "SELECT *, CONCAT(SUBSTRING_INDEX(SUBSTRING_INDEX(fullname, ' ', 2), ' ', -1),' ', SUBSTRING_INDEX(SUBSTRING_INDEX(fullname, ' ', 1), ' ', -1)) as fullnamerev FROM users ORDER BY fullnamerev"
