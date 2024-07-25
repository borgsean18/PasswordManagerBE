-- Up Migration
CREATE TABLE IF NOT EXISTS passwords (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    user_id BIGINT NOT NULL,
    folder_id BIGINT
);