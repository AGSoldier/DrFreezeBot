DROP TABLE IF EXISTS roles CASCADE;
CREATE TABLE roles(
    
    -- Columns
    id SERIAL NOT NULL,
    role int NOT NULL,
    name varchar NOT NULL,
    
    -- Constraints
    PRIMARY KEY(id)
    
);

INSERT INTO roles(id, role, name)
VALUES  (1, 0, 'User'),
        (2, 1, 'Admin');
        
ALTER TABLE users
ADD COLUMN role int NOT NULL DEFAULT(1),
ADD FOREIGN KEY(role) REFERENCES roles(id),
ADD COLUMN debugger boolean NOT NULL DEFAULT(false);