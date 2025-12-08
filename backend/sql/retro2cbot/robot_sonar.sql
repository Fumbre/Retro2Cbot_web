create table robot_sonar
(
    id             bigint                             not null
        primary key,
    robot_id       bigint                             null,
    sonar_distance float(2, 0)                        not null comment 'unit: cm',
    create_time    datetime default CURRENT_TIMESTAMP null
);

