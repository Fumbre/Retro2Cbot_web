create table robots
(
    id         bigint  not null
        constraint id
            primary key,
    robot_name varchar not null,
    robot_code varchar not null
);

alter table robots
    owner to root;

create table robot_sonar
(
    id             bigint                              not null
        constraint sonar_id
            primary key,
    robot_id       bigint                              not null,
    sonar_distance real                                not null,
    create_time    timestamp default CURRENT_TIMESTAMP not null,
    direction      char
);

comment on column robot_sonar.direction is '0:front, 1:rigth,2:left';

alter table robot_sonar
    owner to root;

create index create_time_sonar
    on robot_sonar (create_time);

create table robot_pulses
(
    id                bigint                              not null
        constraint pulses_id
            primary key,
    robot_id          bigint                              not null,
    left_wheel_pulse  bigint                              not null,
    right_wheel_pulse bigint                              not null,
    create_time       timestamp default CURRENT_TIMESTAMP not null
);

alter table robot_pulses
    owner to root;

create index create_time
    on robot_pulses (create_time);

create table robot_neopixels
(
    id             bigint                  not null
        primary key,
    robot_id       bigint                  not null,
    neopixel_index integer                 not null,
    r              integer                 not null,
    g              integer                 not null,
    b              integer                 not null,
    create_time    timestamp default now() not null
);

alter table robot_neopixels
    owner to root;

create table robot_gripper
(
    id             bigint                              not null
        constraint grippr_id
            primary key,
    robot_id       bigint                              not null,
    gripper_status boolean                             not null,
    create_time    timestamp default CURRENT_TIMESTAMP not null
);

comment on column robot_gripper.gripper_status is 'true :open, false: close';

alter table robot_gripper
    owner to root;

create index create_time_gripper
    on robot_gripper (create_time);

create table reflective_sensor
(
    id             bigint                  not null
        primary key,
    robot_id       bigint                  not null,
    a0             integer                 not null,
    a1             integer                 not null,
    a2             integer                 not null,
    a3             integer                 not null,
    a4             integer                 not null,
    a5             integer                 not null,
    a6             integer                 not null,
    a7             integer                 not null,
    current_status varchar                 not null,
    create_time    timestamp default now() not null
);

alter table reflective_sensor
    owner to root;

create index create_time_rs
    on reflective_sensor (create_time);

