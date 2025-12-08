create table robot_pulses
(
    id           bigint                             not null
        primary key,
    robot_id     bigint                             null,
    left_pulses  bigint                             null,
    right_pulses bigint                             null,
    create_time  datetime default CURRENT_TIMESTAMP null
);

