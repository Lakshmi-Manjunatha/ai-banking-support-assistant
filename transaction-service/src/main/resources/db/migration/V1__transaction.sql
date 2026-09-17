CREATE SEQUENCE IF NOT EXISTS transaction_id_seq
    START WITH 1
    INCREMENT BY 50;

CREATE TABLE transactions (
                              id BIGINT PRIMARY KEY DEFAULT nextval('transaction_id_seq'),

                              account_id BIGINT NOT NULL,

                              transaction_type VARCHAR(20) NOT NULL,

                              amount NUMERIC(19,2) NOT NULL,

                              currency VARCHAR(3) NOT NULL,

                              status VARCHAR(20) NOT NULL,

                              description VARCHAR(255),

                              failure_reason VARCHAR(255),

                              created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_transactions_account_id
    ON transactions(account_id);