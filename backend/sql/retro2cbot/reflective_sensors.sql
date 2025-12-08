create table reflective_sensors
(
    id          bigint                             not null
        primary key,
    robot_id    bigint                             not null,
    A0          int                                null,
    A1          int                                null,
    A2          int                                null,
    A3          int                                null,
    A4          int                                null,
    A5          int                                null,
    A6          int                                null,
    A7          int                                null,
    create_time datetime default CURRENT_TIMESTAMP null
);

