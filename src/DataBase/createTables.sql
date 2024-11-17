-- Create Tables Jobbly
-- Petitioner = Solicitante
-- Worker = Trabajador
-- Request = Peticion
-- Service = Servicio

-- Tabla que almacena los datos del usuario
create table users (
    id serial primary key not null,
    first_name varchar(30),
    second_name varchar(30),
    lastname varchar(30),
    phone_number integer unique not null,
    address varchar(30),
    rut integer not null,
    age integer not null,
    calification real not null
);

-- Tabla que almacena los datos necesarios para realizar un log-in. La clave esta encriptada
create table user_login (
    id serial primary key not null,
    mail varchar(30) unique not null,
    pass_hash varchar(30) unique not null,
    id_user int unique not null,
    foreign key (id_user) references users(id) on delete cascade
);

-- Tabla que almacena las id_user de todos los usuarios que son trabajadores
create table worker (
    id serial primary key not null,
    id_user integer not null,
    foreign key (id_user) references users(id) on delete cascade
);

-- Tabla que almacenar las id_user de todos los usuarios que son solicitantes
create table petitioner (
    id serial primary key not null,
    id_user integer not null,
    foreign key (id_user) references users(id) on delete cascade
);

-- Tabla que almacena todos los campos necesarios para almacenar un servicio
create table service (
    id serial primary key not null,
    id_worker integer not null,
    foreign key (id_worker) references worker(id) on delete cascade,
    title varchar(50) not null,
    subtitle varchar(100) not null,
    content text,
    init_date date not null,
    finish_date date default null,
    price int not null
);

-- Peticion del solicitante para que el trabajador le de un servicio
create table petitioner_service(
    id serial primary key not null,
    id_service integer not null,
    foreign key (id_service) references service(id) on delete cascade,
    id_petitioner integer not null,
    foreign key (id_petitioner) references petitioner(id) on delete cascade,
    petition_date date not null,
    solved boolean                                                          -- Si el trabajador ha satisfacido el servicio
);

-- Evaluacion de parte del solicitante a un servicio dado por un trabajador
create table evaluation_petitioner( 
    id serial primary key not null,
    id_petitioner_service integer unique not null,
    foreign key (id_petitioner_service) references petitioner_service(id),
    content text,
    calification integer not null
);

-- Evaluacion de parte del trabajador al solicitante dado un servicio dado por un trabajador
create table evaluation_worker( 
    id serial primary key not null,
    id_petitioner_service integer unique not null,
    foreign key (id_petitioner_service) references petitioner_service(id),
    content text,
    calification int not null
);

-- Tabla que almacena todos los elementos necesarios para levantar una solicitud
create table request (
    id serial primary key not null,
    id_petitioner integer not null,
    foreign key (id_petitioner) references petitioner(id),
    title varchar(50) not null,
    subtitle varchar(100) not null,
    content text,
    init_date date not null,
    finish_date date default null,
    price int not null
);

-- Peticion de `Worker` para realizar una solicitud
create table worker_request (
    id serial primary key not null,
    id_worker integer not null,
    foreign key (id_worker) references worker(id),
    id_request integer not null,
    foreign key (id_request) references request(id),
    petition_date date not null,
    solved boolean
);

-- Resena de un solicitante a un trabajador por una solicitud realizada al solicitante
create table petitioner_review ( 
    id serial primary key not null,
    id_worker_request integer unique not null,
    foreign key (id_worker_request) references worker_request(id),
    content text,
    calification integer not null
);

-- Resena de un trabajador a un solicitante dado una solicitud realizada por el trabajador
create table worker_review ( 
    id serial primary key not null,
    id_worker_request integer unique not null,
    foreign key (id_worker_request) references worker_request(id),
    content text,
    calification integer not null
);