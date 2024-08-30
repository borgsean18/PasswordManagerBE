-- Up Migration
CREATE TABLE IF NOT EXISTS record (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_weak BOOLEAN NOT NULL DEFAULT FALSE,
    user_id UUID NOT NULL,
    group_id UUID 
);