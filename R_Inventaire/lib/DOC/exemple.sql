/**
* 
* BD HR en version MySQL
*  
* 
*/


DROP DATABASE IF EXISTS Labo11;
CREATE DATABASE Labo11 CHARACTER SET utf8 COLLATE utf8_general_ci;

use Labo11;

/* *************************************************************** 
*************************** QUESTIONS 01 ************************
**************************************************************** */

SELECT
    e.last_name AS "Nom",
    j.job_title AS "Titre"
FROM
    employees e
JOIN jobs j ON
    e.job_id = j.job_id
    WHERE e.employee_id IN (100, 200, 205, 206);

/* *************************************************************** 
*************************** QUESTIONS 02 ************************
**************************************************************** */

SELECT
    e.last_name AS "Nom",
    j.job_title AS "Titre",
    d.department_name AS "Service"
FROM
    employees e
JOIN jobs j ON  e.job_id = j.job_id
JOIN departments d ON e.department_id = d.department_id
    WHERE e.employee_id IN (100, 200, 205, 206);

/* *************************************************************** 
*************************** QUESTIONS 03 ************************
**************************************************************** */

SELECT
    e.last_name AS "Nom",
    j.job_title AS "Titre",
    d.department_name AS "Service",
    l.city AS "Ville"
FROM
    employees e
JOIN jobs j ON  e.job_id = j.job_id
JOIN departments d ON e.department_id = d.department_id
JOIN locations l ON d.location_id = l.location_id
    WHERE e.employee_id IN (100, 200, 205, 206);

/* *************************************************************** 
*************************** QUESTIONS 04 ************************
**************************************************************** */

SELECT
    e.last_name AS "Nom",
    j.job_title AS "Titre",
    d.department_name AS "Service",
    l.city AS "Ville", 
    CONCAT(ROUND(e.commission_pct*100), " %") AS "Commision"
FROM
    employees e
JOIN jobs j ON  e.job_id = j.job_id
JOIN departments d ON e.department_id = d.department_id
JOIN locations l ON d.location_id = l.location_id
    WHERE e.commission_pct IS NOT NULL
    ORDER BY "Commission";

/* *************************************************************** 
***************************CREATING TABLES************************
**************************************************************** */

	CREATE TABLE clients(
		ClientID INT(11) IS NOT NULL PRIMARY KEY,
		Nom VARCHAR(50) NOT NULL,
		Adresse VARCHAR(255) NOT NULL,
		Ville VARCHAR(3) NOT NULL,
		MembreDepuis DATETIME NOT NULL,
		Solde DECIMAL(10,2) NOT NULL,
		PRIMARY KEY (ClientID)
	);

	CREATE TABLE villes(
		CodeVille VARCHAR(3) NOT NULL,
		NomVille VARCHAR(100) NOT NULL,
		PRIMARY KEY (CodeVille)
	)

/* *************************************************************** 
***************************FOREIGN KEYS***************************
**************************************************************** */

ALTER TABLE clients ADD FOREIGN KEY (Ville) 
	REFERENCES villes(CodeVille);