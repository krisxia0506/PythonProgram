create table t_teacher
(
    id                 int auto_increment
        primary key,
    name               varchar(255) null,
    title              varchar(255) null,
    degree             varchar(255) null,
    research_interests varchar(255) null,
    department         varchar(255) null,
    email              varchar(255) null,
    education          varchar(255) null,
    bio                longtext     null
);

