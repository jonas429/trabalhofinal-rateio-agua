-- 1. Tabela para mapear a estrutura física do prédio
CREATE TABLE IF NOT EXISTS apartamentos (
    id SERIAL PRIMARY KEY,
    apartamento VARCHAR(10) UNIQUE NOT NULL,
    andar INT NOT NULL
);

-- 2. Tabela para registrar o gasto global do mês
CREATE TABLE IF NOT EXISTS faturas_mes (
    id SERIAL PRIMARY KEY,
    mes_referencia VARCHAR(7) UNIQUE NOT NULL, -- Formato 'YYYY-MM'
    valor_total NUMERIC(10, 2) NOT NULL,
    valor_por_unidade NUMERIC(10, 2) NOT NULL
);

-- 3. Inserir os 7 apartamentos distribuídos nos 4 andares
INSERT INTO apartamentos (apartamento, andar) VALUES 
('101', 1), ('102', 1),
('201', 2), ('202', 2),
('301', 3), ('302', 3),
('401', 4) 
ON CONFLICT DO NOTHING;