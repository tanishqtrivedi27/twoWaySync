-- noinspection SqlNoDataSourceInspectionForFile

CREATE DATABASE zenskar;

\c zenskar

CREATE TABLE IF NOT EXISTS customers (
        id SERIAL PRIMARY KEY,
        username INT NOT NULL,
        password VARCHAR(255) NOT NULL,
    );