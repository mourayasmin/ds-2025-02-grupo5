-- Migration: 002_update_serie_ano_length.sql
-- Update serie_ano field to support longer values

ALTER TABLE estudantes 
ALTER COLUMN serie_ano TYPE VARCHAR(100);

