CREATE SEQUENCE IF NOT EXISTS customer_id_seq START WITH 1 INCREMENT BY 50;


CREATE TABLE customer
(
    id            BIGINT PRIMARY KEY,
    firstname     VARCHAR(50) NOT NULL,
    lastname      VARCHAR(50),
    email         VARCHAR(255) UNIQUE NOT NULL,
    password      TEXT                NOT NULL,
    status        VARCHAR(20) NOT NULL DEFAULT 'Active'
    accountType   VARCHAR(30) NOT NULL,
    createdAT     TIMESTAMP           NOT NULL DEFAULT NOW(),
    updatedAt     TIMESTAMP           NOT NULL DEFAULT NOW()
);

