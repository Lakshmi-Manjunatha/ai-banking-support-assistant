CREATE SEQUENCE IF NOT EXISTS customer_id_seq
    START WITH 1
    INCREMENT BY 50;

CREATE TABLE customer
(
    id           BIGINT PRIMARY KEY DEFAULT nextval('customer_id_seq'),
    first_name    VARCHAR(50)  NOT NULL,
    last_name     VARCHAR(50),
    email        VARCHAR(255) NOT NULL UNIQUE,
    password     TEXT         NOT NULL,
    status       VARCHAR(20)  NOT NULL DEFAULT 'Active',
    account_type VARCHAR(30)  NOT NULL,
    created_at   TIMESTAMP    NOT NULL DEFAULT NOW(),
    updated_at   TIMESTAMP    NOT NULL DEFAULT NOW()
);