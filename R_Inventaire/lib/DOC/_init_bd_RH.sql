DROP DATABASE IF EXISTS BD_RH; 
CREATE DATABASE BD_RH CHARACTER SET utf8 COLLATE utf8_general_ci;
use BD_RH;

-- Activer le moteur transactionnel
SET FOREIGN_KEY_CHECKS = 0;

-- 1) Tables de référence simples
CREATE TABLE Type (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE Annee (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    valeur YEAR NOT NULL
) ENGINE=InnoDB;

CREATE TABLE Fabricant (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(150) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE Provenance (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    pays VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE Destination (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    pays VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE Date_de_creation (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    date_production DATE NOT NULL
) ENGINE=InnoDB;

CREATE TABLE Lien (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(500) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE Specificites (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    description TEXT
) ENGINE=InnoDB;

CREATE TABLE Prix (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    montant DECIMAL(10,2) NOT NULL,
    devise VARCHAR(10) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE Editeur (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(150) NOT NULL
) ENGINE=InnoDB;

-- 2) Table principale
CREATE TABLE Produit (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(200) NOT NULL,

    type_id INT,
    annee_id INT,
    fabricant_id INT,
    provenance_id INT,
    destination_id INT,
    date_de_creation_id INT,
    lien_id INT,
    specificites_id INT,
    prix_id INT,
    editeur_id INT,

    FOREIGN KEY (type_id) REFERENCES Type(ID),
    FOREIGN KEY (annee_id) REFERENCES Annee(ID),
    FOREIGN KEY (fabricant_id) REFERENCES Fabricant(ID),
    FOREIGN KEY (provenance_id) REFERENCES Provenance(ID),
    FOREIGN KEY (destination_id) REFERENCES Destination(ID),
    FOREIGN KEY (date_de_creation_id) REFERENCES Date_de_creation(ID),
    FOREIGN KEY (lien_id) REFERENCES Lien(ID),
    FOREIGN KEY (specificites_id) REFERENCES Specificites(ID),
    FOREIGN KEY (prix_id) REFERENCES Prix(ID),
    FOREIGN KEY (editeur_id) REFERENCES Editeur(ID)
) ENGINE=InnoDB;

-- 3) Approbations liées au produit (relation 1 -> N)
CREATE TABLE Approbations (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    produit_id INT NOT NULL,
    organisme VARCHAR(200) NOT NULL,
    date_approbation DATE,

    FOREIGN KEY (produit_id) REFERENCES Produit(ID)
) ENGINE=InnoDB;

-- 4) Produits similaires (relation N <-> N auto-référencée)
CREATE TABLE Similaires (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    produit_id INT NOT NULL,
    similaire_id INT NOT NULL,

    FOREIGN KEY (produit_id) REFERENCES Produit(ID),
    FOREIGN KEY (similaire_id) REFERENCES Produit(ID),

    UNIQUE (produit_id, similaire_id)
) ENGINE=InnoDB;

SET FOREIGN_KEY_CHECKS = 1;
