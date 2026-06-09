INSERT INTO clients (
    client_id,
    client_name
)
VALUES (
    'commerceai-internal',
    'CommerceAI Internal'
)
ON CONFLICT (client_id)
DO NOTHING;
