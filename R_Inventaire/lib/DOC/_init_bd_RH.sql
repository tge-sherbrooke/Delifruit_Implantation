DROP DATABASE IF EXISTS bd_rh; 
CREATE DATABASE bd_rh CHARACTER SET utf8 COLLATE utf8_general_ci;
USE bd_rh;

-- ================================
-- 1) Tables de référence simples
-- ================================

-- ================================
-- 2) Table finale : Employe
-- ================================

CREATE TABLE Employe (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fonctions VARCHAR(200) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    nom VARCHAR(100) NOT NULL,
    departement VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    courriel VARCHAR(200) NOT NULL,
    privilege VARCHAR(200) NOT NULL,
    age DATE NOT NULL,
    entreprise VARCHAR(150) NOT NULL,
    adresses VARCHAR(200) NOT NULL,
    date_creation DATE NOT NULL,
    editeur VARCHAR(150) NOT NULL,
    liens VARCHAR(500) NOT NULL
) ENGINE=InnoDB;


-- I N S E R T I O N    D E S     D O N N E E S

