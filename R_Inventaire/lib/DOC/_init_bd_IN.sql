DROP DATABASE IF EXISTS bd_inv; 
CREATE DATABASE bd_inv CHARACTER SET utf8 COLLATE utf8_general_ci;
USE bd_inv;

-- ================================
-- 1) Tables de référence simples
-- ================================

-- ================================
-- 2) Table principale
-- ================================

CREATE TABLE Produits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    produit VARCHAR(200) NOT NULL,
    types VARCHAR(100) NOT NULL,
    annee INT NOT NULL,
    fabricant VARCHAR(150) NOT NULL,
    provenance VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    date_production DATE NOT NULL,
    liens VARCHAR(500) NOT NULL,
    quantite INT NOT NULL,
    prix DECIMAL(10,2) NOT NULL,
    approbations VARCHAR(200) NOT NULL,
    editeur VARCHAR(150) NOT NULL

) ENGINE=InnoDB;

-- ================================
-- 3) Approbations (relation 1 → N)
-- ================================


-- ================================
-- (Insertion de données ensuite)
-- ================================

