-- V2__create_accounts.sql

CREATE SEQUENCE IF NOT EXISTS account_id_seq
    START WITH 1
    INCREMENT BY 50;

CREATE TABLE accounts (
                          id BIGINT PRIMARY KEY DEFAULT nextval('account_id_seq'),

                          customer_id BIGINT NOT NULL,

                          account_number VARCHAR(8) NOT NULL,
                          sort_code VARCHAR(8) NOT NULL DEFAULT '09-06-20',
                          currency VARCHAR(3) NOT NULL,

                          account_type VARCHAR(20) NOT NULL,
                          account_status VARCHAR(20) NOT NULL,

                          balance NUMERIC(19,2) NOT NULL DEFAULT 0.00,
                          daily_transfer_limit NUMERIC(19,2) NOT NULL,

                          created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

                          CONSTRAINT uk_account_number UNIQUE (account_number),

                          CONSTRAINT fk_account_customer
                              FOREIGN KEY (customer_id)
                                  REFERENCES customer(id)
);