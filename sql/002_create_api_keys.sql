CREATE TABLE IF NOT EXISTS api_keys (
    api_key_id VARCHAR(100) PRIMARY KEY,

    client_id VARCHAR(100) NOT NULL,

    api_key_hash TEXT NOT NULL UNIQUE,

    description VARCHAR(255),

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    last_used_at TIMESTAMP,

    CONSTRAINT fk_api_keys_client
        FOREIGN KEY (client_id)
        REFERENCES clients(client_id)
        ON DELETE CASCADE
);
