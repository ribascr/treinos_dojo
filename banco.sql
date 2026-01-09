-- ============================================================
--  CRIAÇÃO DO BANCO
-- ============================================================
CREATE DATABASE IF NOT EXISTS dojo_presencas
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE dojo_presencas;

-- ============================================================
--  TABELA DE CONFIGURAÇÕES DO DOJO
-- ============================================================
CREATE TABLE configuracoes_dojo (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome_dojo VARCHAR(150),
    duracao_aula_minutos INT NOT NULL DEFAULT 75,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Inserir configuração inicial
INSERT INTO configuracoes_dojo (nome_dojo, duracao_aula_minutos)
VALUES ('Meu Dojo', 75);

-- ============================================================
--  TABELA DE ALUNOS
-- ============================================================
CREATE TABLE alunos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(150) NOT NULL,
    data_nascimento DATE,
    telefone VARCHAR(20),
    email VARCHAR(150),
    data_cadastro DATE DEFAULT CURRENT_DATE,
    faixa_atual VARCHAR(50),
    observacoes TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Índices úteis
CREATE INDEX idx_alunos_nome ON alunos(nome);
CREATE INDEX idx_alunos_email ON alunos(email);

-- ============================================================
--  TABELA DE USUÁRIOS (LOGIN)
-- ============================================================
CREATE TABLE usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    tipo ENUM('ADMIN', 'ALUNO') NOT NULL DEFAULT 'ALUNO',
    aluno_id INT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (aluno_id) REFERENCES alunos(id) ON DELETE SET NULL
);

-- ============================================================
--  TABELA DE PRESENÇAS
-- ============================================================
CREATE TABLE presencas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    aluno_id INT NOT NULL,
    data_aula DATE NOT NULL,
    duracao_minutos INT NOT NULL,
    tipo_aula VARCHAR(100),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (aluno_id) REFERENCES alunos(id) ON DELETE CASCADE
);

-- Índices úteis
CREATE INDEX idx_presencas_aluno ON presencas(aluno_id);
CREATE INDEX idx_presencas_data ON presencas(data_aula);

-- ============================================================
--  TABELA DE EXAMES DE GRADUAÇÃO
-- ============================================================
CREATE TABLE exames_graduacao (
    id INT PRIMARY KEY AUTO_INCREMENT,
    aluno_id INT NOT NULL,
    faixa_anterior VARCHAR(50),
    faixa_nova VARCHAR(50) NOT NULL,
    data_exame DATE NOT NULL,
    observacoes TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (aluno_id) REFERENCES alunos(id) ON DELETE CASCADE
);

CREATE INDEX idx_exames_aluno ON exames_graduacao(aluno_id);

-- ============================================================
--  TABELA DE ATIVIDADES EXTRAS
-- ============================================================
CREATE TABLE atividades_extras (
    id INT PRIMARY KEY AUTO_INCREMENT,
    aluno_id INT NOT NULL,
    tipo_atividade VARCHAR(100) NOT NULL,
    descricao TEXT,
    data_inicio DATE NOT NULL,
    data_fim DATE,
    carga_horaria_minutos INT DEFAULT 0,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (aluno_id) REFERENCES alunos(id) ON DELETE CASCADE
);

CREATE INDEX idx_atividades_aluno ON atividades_extras(aluno_id);

-- ============================================================
--  VIEW: TOTAL DE HORAS POR ALUNO (AULAS + EXTRAS)
-- ============================================================
CREATE OR REPLACE VIEW vw_total_horas_treinadas AS
SELECT 
    a.id AS aluno_id,
    a.nome,
    COALESCE(SUM(p.duracao_minutos), 0) 
        + COALESCE((SELECT SUM(carga_horaria_minutos) 
                    FROM atividades_extras ae 
                    WHERE ae.aluno_id = a.id), 0) 
        AS total_minutos
FROM alunos a
LEFT JOIN presencas p ON p.aluno_id = a.id
GROUP BY a.id;
