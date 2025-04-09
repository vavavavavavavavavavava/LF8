CREATE DATABASE IF NOT EXISTS pokemon_db;

USE pokemon_db;

CREATE TABLE IF NOT EXISTS pokemon (
    pokedex_number INT PRIMARY KEY,
    name VARCHAR(100),
    original_image LONGBLOB,
    black_image LONGBLOB
);

CREATE TABLE IF NOT EXISTS highscores (
    name VARCHAR(255) NOT NULL,
    score INT NOT NULL
)