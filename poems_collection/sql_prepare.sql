-- 诗歌概要
create table poems_summary(
	poem_id	varchar		primary key,
	title 	varchar	 	not null,
	writer	varchar,
	dynasty	varchar,
	tags	  varchar,
	style		varchar,
	type	  varchar		not null
);

-- 古诗文
create table poems_context(
	poem_id		varchar	primary key,
	sentence	varchar	not null,
	serial		int   	not null
);

-- 诗歌主题标签
create table poems_tags(
	tag_id	int			primary key,
	tag			varchar
);

------------------------------------------------
-- 译文暂时不爬取 --
------------------------------------------------

-- 古诗文翻译
create table poems_translation(
	poem_id			varchar		primary key,
	translation	varchar 	not null,
	serial			int   		not null
);

-- 古诗字词注释
create table words_annotation(
	poem_id			varchar	primary key,
	word				varchar	not null,
	annotation	varchar
);

-- 常用操作
-- drop table if exists poems_summary;