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
    id int auto_increment PRIMARY KEY,
    texto text NOT NULL,
    datahora datetime,
    fk_aluno_ra char(8)
);

ALTER TABLE diariobordo ADD CONSTRAINT FK_diariobordo_2
    FOREIGN KEY (fk_aluno_ra)
    REFERENCES aluno (ra)
    ON DELETE CASCADE;
    
CREATE TABLE avaliacao (
    id int PRIMARY KEY auto_increment,
    nota1 int,
    nota2 int,
    nota3 int,
    nota4 int,
    fk_aluno_id int NOT NULL
);

ALTER TABLE avaliacao
ADD CONSTRAINT CHECK (nota1 <= 25),
ADD CONSTRAINT CHECK (nota2 <= 25),
ADD CONSTRAINT CHECK (nota3 <= 25),
ADD CONSTRAINT CHECK (nota4 <= 25);

ALTER TABLE avaliacao MODIFY nota1 INT;

ALTER TABLE avaliacao ADD CONSTRAINT FK_avaliacao_2
    FOREIGN KEY (fk_aluno_id)
    REFERENCES aluno (id);

INSERT INTO aluno (ra, nome, tempoestudo, rendafamiliar) VALUES ('11111111', 'André vargas', 10, 100000.00);


