#drop database pokemon_db if exists;
CREATE DATABASE pokemon_db;

USE pokemon_db;

CREATE TABLE pokemon (
    pokedex_number INT PRIMARY KEY,
    name VARCHAR(100),
    original_image LONGBLOB,
    black_image LONGBLOB
);

CREATE TABLE user (
    user_ID INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
)

CREATE TABLE highscores (
    name VARCHAR(255) NOT NULL,
    score INT NOT NULL
)