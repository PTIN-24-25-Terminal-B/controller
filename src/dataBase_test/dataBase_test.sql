-- crea la tabla
CREATE TABLE car (
    carType INTEGER,
    seatCount TEXT,
    id TEXT,
    mileage FLOAT,
    completedRuns INTEGER
);

-- inserta algunos valores de ejemplo
INSERT INTO car VALUES (1, '4', 'CAR001', 12345.6, 150);
INSERT INTO car VALUES (2, '2', 'CAR002', 6543.2, 75);
INSERT INTO car VALUES (1, '5', 'CAR003', 20400.0, 230);
INSERT INTO car VALUES (3, '7', 'CAR004', 500.0, 10);
INSERT INTO car VALUES (2, '2', 'CAR005', 9999.9, 120);
