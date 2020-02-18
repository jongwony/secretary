create table dev_restrict(
    id varchar(64) charset ascii,
    url varchar(2048) charset ascii unique key,
    title text charset utf8mb4,
    user varchar(16) charset ascii,
    channel varchar(16) charset ascii,
    create_date datetime default CURRENT_TIMESTAMP
)