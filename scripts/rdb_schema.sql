create table dev_restrict(
    id int primary key auto_increment,
    url varchar(2048) charset ascii unique key,
    title text charset utf8mb4,
    create_date datetime default CURRENT_TIMESTAMP
)