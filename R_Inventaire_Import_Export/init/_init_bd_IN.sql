DROP DATABASE IF EXISTS bb_inv; 
CREATE DATABASE bb_inv CHARACTER SET utf8 COLLATE utf8_general_ci;
USE bb_inv;

-- ================================
-- 1) Tables de référence simples
-- ================================

CREATE TABLE Types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE Annee (
    id INT AUTO_INCREMENT PRIMARY KEY,
    valeur INT NOT NULL
) ENGINE=InnoDB;

CREATE TABLE Fabricant (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(150) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE Provenance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pays VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE Destination (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pays VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE Date_de_creation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date_production DATE NOT NULL
) ENGINE=InnoDB;

CREATE TABLE Lien (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(500) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE Quantite (
    id INT AUTO_INCREMENT PRIMARY KEY,
    valeur INT NOT NULL
) ENGINE=InnoDB;

CREATE TABLE Prix (
    id INT AUTO_INCREMENT PRIMARY KEY,
    montant DECIMAL(10,2) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE Editeur (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(150) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE Produit (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(200) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE Approbations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    organisme VARCHAR(200) NOT NULL
) ENGINE=InnoDB;


-- ================================
-- 2) Table principale
-- ================================

CREATE TABLE Produits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    produit_id INT,
    types_id INT,
    annee_id INT,
    fabricant_id INT,
    provenance_id INT,
    destination_id INT,
    date_de_creation_id INT,
    lien_id INT,
    quantite_id INT,
    prix_id INT,
    approbations_id INT,
    editeur_id INT,

    FOREIGN KEY (produit_id) REFERENCES Produit(id),
    FOREIGN KEY (types_id) REFERENCES Types(id),
    FOREIGN KEY (annee_id) REFERENCES Annee(id),
    FOREIGN KEY (fabricant_id) REFERENCES Fabricant(id),
    FOREIGN KEY (provenance_id) REFERENCES Provenance(id),
    FOREIGN KEY (destination_id) REFERENCES Destination(id),
    FOREIGN KEY (date_de_creation_id) REFERENCES Date_de_creation(id),
    FOREIGN KEY (quantite_id) REFERENCES Quantite(id),
    FOREIGN KEY (prix_id) REFERENCES Prix(id),
    FOREIGN KEY (lien_id) REFERENCES Lien(id),
    FOREIGN KEY (approbations_id) REFERENCES Approbations(id),
    FOREIGN KEY (editeur_id) REFERENCES Editeur(id)
) ENGINE=InnoDB;

-- ================================
-- 3) Approbations (relation 1 → N)
-- ================================


-- ================================
-- (Insertion de données ensuite)
-- ================================

