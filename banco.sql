create database projetodiario1;

use projetodiaro1;

create table aluno(
	id int primary key auto_increment,
    ra char(8) not null unique,
	nome VARCHAR(80),
    tempoestudo INT not null,
    rendafamiliar DECIMAL(10, 2)
);

CREATE TABLE diariobordo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    texto TEXT,
    datahora DATETIME DEFAULT CURRENT_TIMESTAMP,
    fk_aluno_ra VARCHAR(10) NOT NULL,
    polaridade TEXT,
    FOREIGN KEY (fk_aluno_ra) REFERENCES aluno(ra)
);

CREATE TABLE funcionarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rg CHAR(8) NOT NULL UNIQUE,
    nome VARCHAR(100) NOT NULL,
    setor VARCHAR(50)
);

    
CREATE TABLE avaliacao (
    id int PRIMARY KEY auto_increment,
    nota1 int,
    nota2 int,
    nota3 int,
    nota4 int,
    fk_aluno_id int NOT NULL
);''

ALTER TABLE avaliacao
ADD CONSTRAINT CHECK (nota1 <= 25),
ADD CONSTRAINT CHECK (nota2 <= 25),
ADD CONSTRAINT CHECK (nota3 <= 25),
ADD CONSTRAINT CHECK (nota4 <= 25);

ALTER TABLE avaliacao MODIFY nota1 INT;

ALTER TABLE avaliacao ADD CONSTRAINT FK_avaliacao_2
    FOREIGN KEY (fk_aluno_id)
    REFERENCES aluno (id);

INSERT INTO aluno (ra, nome, tempoestudo, rendafamiliar) VALUES 
('12345678', 'Lucas Mendes', 15, 50000.00),
('12345679', 'Fernanda Lima', 12, 80000.00),
('12345680', 'Ricardo Silva', 20, 150000.00),
('12345681', 'Juliana Santos', 18, 120000.00),
('12345682', 'Roberto Gomes', 14, 60000.00),
('12345683', 'Tatiane Alves', 16, 90000.00),
('12345684', 'Júlio César', 11, 30000.00),
('12345685', 'Vanessa Soares', 19, 110000.00);

INSERT INTO funcionarios (rg, nome, setor) VALUES 
('22222222', 'Vargas Andre', 'TI'),
('87654321', 'Maria Oliveira', 'Financeiro'),
('23456789', 'Carlos Pereira', 'Manutenção'),
('34567890', 'Ana Costa', 'Psicologia');

select *from diariobordo;


