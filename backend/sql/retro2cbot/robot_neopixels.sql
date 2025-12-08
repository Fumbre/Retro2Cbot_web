create table robot_neopixels
(
    id             bigint                             not null
        primary key,
    robot_id       bigint                             not null,
    neopixel_index int                                not null,
    R              int                                not null,
    G              int                                not null,
    B              int                                not null,
    create_time    datetime default CURRENT_TIMESTAMP not null
);

