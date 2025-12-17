
/* drop table score  */


create table public.score
(
	gender varchar(100),
	race_ethnicity varchar(100),
	parental_level_of_education varchar(100),
	lunch varchar(100),
	test_preparation_course varchar(100),
	math_score decimal(18,2),
	reading_score decimal(18,2),
	writing_score decimal(18,2)	
);

select * from public.score;

copy score (gender,	race_ethnicity,	parental_level_of_education,
	lunch,	test_preparation_course,	math_score,
	reading_score,	writing_score)
from 'D:\Python\mlproject\artifacts\train.csv'
delimiter ','
CSV header;

select * from score
