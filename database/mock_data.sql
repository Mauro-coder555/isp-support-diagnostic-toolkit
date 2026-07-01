CREATE TABLE IF NOT EXISTS clients (
    id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(100) NOT NULL,
    service_plan VARCHAR(50) NOT NULL,
    service_status VARCHAR(30) NOT NULL,
    assigned_ip VARCHAR(45),
    gateway_ip VARCHAR(45),
    router_brand VARCHAR(50),
    connection_type VARCHAR(50),
    radius_status VARCHAR(30),
    tr069_status VARCHAR(30),
    last_seen DATETIME,
    has_open_ticket BOOLEAN DEFAULT FALSE
);

INSERT INTO clients (
    full_name,
    service_plan,
    service_status,
    assigned_ip,
    gateway_ip,
    router_brand,
    connection_type,
    radius_status,
    tr069_status,
    last_seen,
    has_open_ticket
) VALUES
(
    'Juan Perez',
    'Fibra 100MB',
    'active',
    '192.168.10.34',
    '192.168.10.1',
    'MikroTik',
    'FTTH',
    'authorized',
    'online',
    NOW(),
    FALSE
),
(
    'Laura Gomez',
    'Fibra 300MB',
    'suspended',
    '192.168.20.45',
    '192.168.20.1',
    'Huawei',
    'FTTH',
    'rejected',
    'offline',
    DATE_SUB(NOW(), INTERVAL 2 DAY),
    TRUE
),
(
    'Carlos Diaz',
    'Fibra 50MB',
    'active',
    NULL,
    '192.168.30.1',
    'MikroTik',
    'FTTH',
    'authorized',
    'unknown',
    DATE_SUB(NOW(), INTERVAL 5 HOUR),
    FALSE
);