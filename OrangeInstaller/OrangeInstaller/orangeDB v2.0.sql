CREATE DATABASE  IF NOT EXISTS `soporteprueba` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `soporteprueba`;
-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: openlisa.saas.la    Database: soporteprueba
-- ------------------------------------------------------
-- Server version	5.7.19-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Temporary view structure for view `CompaniesAndCodes`
--

DROP TABLE IF EXISTS `CompaniesAndCodes`;
/*!50001 DROP VIEW IF EXISTS `CompaniesAndCodes`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `CompaniesAndCodes` AS SELECT 
 1 AS `name`,
 1 AS `companykey`,
 1 AS `dueDateofKey`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `ExpiredCodes`
--

DROP TABLE IF EXISTS `ExpiredCodes`;
/*!50001 DROP VIEW IF EXISTS `ExpiredCodes`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `ExpiredCodes` AS SELECT 
 1 AS `name`,
 1 AS `companykey`,
 1 AS `dueDate`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `OnlyValidCodes`
--

DROP TABLE IF EXISTS `OnlyValidCodes`;
/*!50001 DROP VIEW IF EXISTS `OnlyValidCodes`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `OnlyValidCodes` AS SELECT 
 1 AS `companykey`,
 1 AS `svnusername`,
 1 AS `svnpassword`,
 1 AS `idcompany`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `company`
--

DROP TABLE IF EXISTS `company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `company` (
  `idcompany` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `dbms` varchar(20) DEFAULT 'mysql',
  `skin` varchar(20) DEFAULT 'GlossyOpen',
  `logqueries` tinyint(1) DEFAULT '0',
  `languaje` varchar(10) DEFAULT NULL,
  `beep_on_queries` tinyint(1) DEFAULT NULL,
  `webdir` varchar(10) DEFAULT 'web',
  `defaultcompany` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`idcompany`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=123 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `company_keys`
--

DROP TABLE IF EXISTS `company_keys`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `company_keys` (
  `companykey` varchar(8) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `svnusername` varchar(50) DEFAULT NULL,
  `svnpassword` varchar(50) DEFAULT NULL,
  `idcompany` int(11) NOT NULL,
  `dueDateOfKey` date NOT NULL,
  PRIMARY KEY (`companykey`),
  UNIQUE KEY `companykey_UNIQUE` (`companykey`),
  UNIQUE KEY `idcompany_UNIQUE` (`idcompany`),
  CONSTRAINT `idcompany` FOREIGN KEY (`idcompany`) REFERENCES `company` (`idcompany`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `company_orangedb`
--

DROP TABLE IF EXISTS `company_orangedb`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `company_orangedb` (
  `id_orangedb` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) DEFAULT NULL,
  `database` varchar(20) DEFAULT NULL,
  `port` int(11) DEFAULT '3306',
  `url` varchar(50) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `default_username` varchar(50) DEFAULT NULL,
  `default_password` varchar(50) DEFAULT NULL,
  `idcompany` int(11) NOT NULL,
  PRIMARY KEY (`id_orangedb`),
  UNIQUE KEY `database_UNIQUE` (`database`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `modules`
--

DROP TABLE IF EXISTS `modules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `modules` (
  `idmodules` int(11) NOT NULL AUTO_INCREMENT,
  `module` varchar(50) NOT NULL,
  `level` int(11) NOT NULL,
  `revision` int(11) DEFAULT '0',
  `svnurl` varchar(50) NOT NULL DEFAULT 'svn://svn.openorange.com/',
  `path` varchar(50) NOT NULL,
  `idcompany` int(11) NOT NULL,
  PRIMARY KEY (`idmodules`)
) ENGINE=InnoDB AUTO_INCREMENT=773 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'soporteprueba'
--
/*!50003 DROP FUNCTION IF EXISTS `BuscarCodigo` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`admin`@`%` FUNCTION `BuscarCodigo`(companyname VARCHAR(50)) RETURNS varchar(100) CHARSET utf8
BEGIN
	DECLARE codecompany VARCHAR(100);
	SELECT CONCAT("Company: ",c.name, " Code: ", ck.companykey) into codecompany from company c join company_keys ck on ck.idcompany = c.idcompany where c.name like CONCAT('%', companyname, '%');
RETURN codecompany;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Final view structure for view `CompaniesAndCodes`
--

/*!50001 DROP VIEW IF EXISTS `CompaniesAndCodes`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`admin`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `CompaniesAndCodes` AS select `c`.`name` AS `name`,`ck`.`companykey` AS `companykey`,`ck`.`dueDateOfKey` AS `dueDateofKey` from (`company` `c` join `company_keys` `ck` on((`ck`.`idcompany` = `c`.`idcompany`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `ExpiredCodes`
--

/*!50001 DROP VIEW IF EXISTS `ExpiredCodes`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`admin`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `ExpiredCodes` AS select `c`.`name` AS `name`,`ck`.`companykey` AS `companykey`,`ck`.`dueDateOfKey` AS `dueDate` from (`company` `c` join `company_keys` `ck` on((`ck`.`idcompany` = `c`.`idcompany`))) where (`ck`.`dueDateOfKey` < curdate()) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `OnlyValidCodes`
--

/*!50001 DROP VIEW IF EXISTS `OnlyValidCodes`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`admin`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `OnlyValidCodes` AS select `company_keys`.`companykey` AS `companykey`,`company_keys`.`svnusername` AS `svnusername`,`company_keys`.`svnpassword` AS `svnpassword`,`company_keys`.`idcompany` AS `idcompany` from `company_keys` where (`company_keys`.`dueDateOfKey` > curdate()) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-09-23 16:00:36
