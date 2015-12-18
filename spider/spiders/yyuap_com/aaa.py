-- MySQL dump 10.13  Distrib 5.6.23, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: uspider_manager
-- ------------------------------------------------------
-- Server version	5.6.24-log

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
-- Table structure for table `ae_role`
--

DROP TABLE IF EXISTS `ae_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ae_role` (
  `pk_role` varchar(30) NOT NULL,
  `rolename` varchar(20) NOT NULL,
  `rolecaption` varchar(200) DEFAULT NULL,
  `comments` varchar(200) DEFAULT NULL,
  `createtime` varchar(20) DEFAULT NULL,
  `modifytime` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`pk_role`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ae_role`
--

LOCK TABLES `ae_role` WRITE;
/*!40000 ALTER TABLE `ae_role` DISABLE KEYS */;
INSERT INTO `ae_role` VALUES ('hg1pcuinerekkgmdnf8g','admin','管理员','管理员角色','2015-11-19 18:56:08',NULL),('p4il8l26yq441mnfwwke','developer','开发者','开发者角色','2015-11-19 18:56:08',NULL);
/*!40000 ALTER TABLE `ae_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ae_user`
--

DROP TABLE IF EXISTS `ae_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ae_user` (
  `pk_user` varchar(30) NOT NULL,
  `username` varchar(20) NOT NULL,
  `usercaption` varchar(200) DEFAULT NULL,
  `password` varchar(200) NOT NULL,
  `comments` varchar(200) DEFAULT NULL,
  `creator` varchar(30) DEFAULT NULL,
  `createtime` varchar(20) DEFAULT NULL,
  `modifier` varchar(30) DEFAULT NULL,
  `modifytime` varchar(20) DEFAULT NULL,
  `logintime` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`pk_user`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ae_user`
--

LOCK TABLES `ae_user` WRITE;
/*!40000 ALTER TABLE `ae_user` DISABLE KEYS */;
INSERT INTO `ae_user` VALUES ('2nvr3z0th110cffgaztk','admin','管理员','admin','','4v12unpppeynlgkwo8pf','2015-11-20 08:48:38',NULL,NULL,NULL),('0fvakmtmn39xslumt25h','dev1','张三','dev1','','4v12unpppeynlgkwo8pf','2015-11-20 08:49:10',NULL,NULL,NULL),('5652a903c70d028620f6d2c4','dev2','李四','dev2','','2nvr3z0th110cffgaztk','2015-11-23 13:49:55','5652a903c70d028620f6d2c4','2015-11-24 16:48:17',NULL),('565424a4c70d3f3231f55b1f','biancm','边传猛','biancm','','2nvr3z0th110cffgaztk','2015-11-24 16:49:40',NULL,NULL,NULL),('56581312c70d6793494425d6','dev3','王五','dev3','','565424a4c70d3f3231f55b1f','2015-11-27 16:23:46',NULL,NULL,NULL),('565bf613c70d6a05beaf9fc9','dev4','马六','dev4','','2nvr3z0th110cffgaztk','2015-11-30 15:09:07',NULL,NULL,NULL);
/*!40000 ALTER TABLE `ae_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ae_user_group`
--

DROP TABLE IF EXISTS `ae_user_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ae_user_group` (
  `pk_group` varchar(30) NOT NULL,
  `groupname` varchar(50) NOT NULL,
  `comments` varchar(200) DEFAULT NULL,
  `creator` varchar(30) DEFAULT NULL,
  `createtime` varchar(20) DEFAULT NULL,
  `modifier` varchar(30) DEFAULT NULL,
  `modifytime` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`pk_group`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ae_user_group`
--

LOCK TABLES `ae_user_group` WRITE;
/*!40000 ALTER TABLE `ae_user_group` DISABLE KEYS */;
INSERT INTO `ae_user_group` VALUES ('56581371c70d6793494425da','BA业务部','','565424a4c70d3f3231f55b1f','2015-11-27 16:25:21',NULL,NULL),('5657d399c70db922ec0b9848','AE开发部','','565424a4c70d3f3231f55b1f','2015-11-27 11:52:57',NULL,NULL);
/*!40000 ALTER TABLE `ae_user_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ae_user_group_related`
--

DROP TABLE IF EXISTS `ae_user_group_related`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ae_user_group_related` (
  `pk_related` varchar(30) NOT NULL,
  `pk_user` varchar(30) NOT NULL,
  `pk_user_group` varchar(30) NOT NULL,
  `createtime` varchar(20) DEFAULT NULL,
  `modifytime` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`pk_related`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ae_user_group_related`
--

LOCK TABLES `ae_user_group_related` WRITE;
/*!40000 ALTER TABLE `ae_user_group_related` DISABLE KEYS */;
INSERT INTO `ae_user_group_related` VALUES ('565812d9c70d6793494425d3','5652a903c70d028620f6d2c4','5657d399c70db922ec0b9848','2015-11-27 16:22:49',NULL),('565bf644c70d6a05beaf9fcc','0fvakmtmn39xslumt25h','56581371c70d6793494425da','2015-11-30 15:09:56',NULL),('5658134ac70d6793494425d9','56581312c70d6793494425d6','5657d399c70db922ec0b9848','2015-11-27 16:24:42',NULL),('565bf626c70d6a05beaf9fcb','565bf613c70d6a05beaf9fc9','56581371c70d6793494425da','2015-11-30 15:09:26',NULL);
/*!40000 ALTER TABLE `ae_user_group_related` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ae_user_role_related`
--

DROP TABLE IF EXISTS `ae_user_role_related`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ae_user_role_related` (
  `pk_related` varchar(30) NOT NULL,
  `pk_user` varchar(30) NOT NULL,
  `pk_role` varchar(30) NOT NULL,
  `createtime` varchar(20) DEFAULT NULL,
  `modifytime` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`pk_related`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ae_user_role_related`
--

LOCK TABLES `ae_user_role_related` WRITE;
/*!40000 ALTER TABLE `ae_user_role_related` DISABLE KEYS */;
INSERT INTO `ae_user_role_related` VALUES ('48g7s6ke01zrmm2l7hcy','2nvr3z0th110cffgaztk','hg1pcuinerekkgmdnf8g','2015-11-20 08:48:38',NULL),('i0qjb477nuyfitzvtp83','0fvakmtmn39xslumt25h','p4il8l26yq441mnfwwke','2015-11-20 08:49:10',NULL),('565424a4c70d3f3231f55b20','565424a4c70d3f3231f55b1f','hg1pcuinerekkgmdnf8g','2015-11-24 16:49:40',NULL),('5652a903c70d028620f6d2c5','5652a903c70d028620f6d2c4','p4il8l26yq441mnfwwke','2015-11-23 13:49:55',NULL),('56581312c70d6793494425d7','56581312c70d6793494425d6','p4il8l26yq441mnfwwke','2015-11-27 16:23:46',NULL),('565bf613c70d6a05beaf9fca','565bf613c70d6a05beaf9fc9','p4il8l26yq441mnfwwke','2015-11-30 15:09:07',NULL);
/*!40000 ALTER TABLE `ae_user_role_related` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `spider_info`
--

DROP TABLE IF EXISTS `spider_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `spider_info` (
  `spider_id` varchar(30) DEFAULT NULL,
  `name` varchar(200) DEFAULT NULL,
  `tag` varchar(1000) DEFAULT NULL,
  `source_type` varchar(200) DEFAULT NULL,
  `source_url` varchar(2000) DEFAULT NULL,
  `source_site` varchar(1000) DEFAULT NULL,
  `code_path` varchar(2000) DEFAULT NULL,
  `note` varchar(1000) DEFAULT NULL,
  `creator` varchar(30) DEFAULT NULL,
  `creation_time` timestamp NULL DEFAULT NULL,
  `modifier` varchar(30) DEFAULT NULL,
  `modify_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `project` varchar(200) DEFAULT NULL,
  `result_store_desc` varchar(2000) DEFAULT NULL,
  `enable` int(11) DEFAULT NULL,
  `schedule_config` varchar(1000) DEFAULT NULL,
  `alert_receiver` varchar(1000) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `spider_info`
--

LOCK TABLES `spider_info` WRITE;
/*!40000 ALTER TABLE `spider_info` DISABLE KEYS */;
INSERT INTO `spider_info` VALUES ('56543d82c70d4716dcf691ae','csdn新闻栏目爬虫','csdn','news','csdn.net/1.html','csdn.net','/uspider_manager/DB/sql/mysql/uspider_manager.sql','测试','5652a903c70d028620f6d2c4','2015-11-24 10:37:04','2nvr3z0th110cffgaztk','2015-11-27 01:37:34','UAP支持部','news@HBase1',1,'manual','biancm@yonyou.com'),('5657c189c70d5a975fd558a3','sohu爬虫','','bbs','sohu.com/1.hml','sohu.com','sohuSpider','','2nvr3z0th110cffgaztk','2015-11-27 02:35:53','2nvr3z0th110cffgaztk','2015-11-27 02:35:53','大娘水饺','',0,'manual',''),('5657bfe5c70d5a975fd558a2','sina新闻爬虫','','ecommerce','sina.com.cn/1/2.html','sina.com.cn','sinaSpider','','2nvr3z0th110cffgaztk','2015-11-27 02:28:53','565424a4c70d3f3231f55b1f','2015-12-02 03:52:09','大娘水饺','',1,'once_a_day',''),('56581a0dc70dd2a499b4d32d','腾讯新闻爬虫','','blog','qq.com/1.html','qq.com','qqSpider','','0fvakmtmn39xslumt25h','2015-11-27 08:53:33','565424a4c70d3f3231f55b1f','2015-12-02 03:51:02','UAP支持部','',1,'once_a_day',''),('565d4c38c70dbc9c50c61a4b','bb','','stock','bb','bb','bb','','565424a4c70d3f3231f55b1f','2015-12-01 07:28:56','565424a4c70d3f3231f55b1f','2015-12-02 07:44:44','bb','',1,'once_a_day',''),('565d1377c70d7c9bf0d87b76','aa3','','bbs','aa','aa','aa','','565424a4c70d3f3231f55b1f','2015-12-01 03:26:47','565424a4c70d3f3231f55b1f','2015-12-02 07:44:58','大娘水饺','',1,'manual',''),('565d4c42c70dbc9c50c61a4c','cc2','','news','cc','cc','cc','','565424a4c70d3f3231f55b1f','2015-12-01 07:29:06','565424a4c70d3f3231f55b1f','2015-12-02 07:51:53','cc','',1,'loop',''),('565d4c4cc70dbc9c50c61a4d','dd8','','news','dd','dd','dd','','565424a4c70d3f3231f55b1f','2015-12-01 07:29:16','565424a4c70d3f3231f55b1f','2015-12-02 08:53:14','dd','',1,'once_a_day',''),('565d4c57c70dbc9c50c61a4e','ee','','news','ee','ee','ee','','565424a4c70d3f3231f55b1f','2015-12-01 07:29:27','565424a4c70d3f3231f55b1f','2015-12-02 06:28:02','ee','',0,'loop',''),('565d4c7bc70dbc9c50c61a4f','ff2','','news','ff','ff2','ff','','565424a4c70d3f3231f55b1f','2015-12-01 07:30:03','565424a4c70d3f3231f55b1f','2015-12-02 08:52:53','ff','',1,'loop',''),('565d4c8bc70dbc9c50c61a50','gg2','','news','gg','csdn.net','__init__','','565424a4c70d3f3231f55b1f','2015-12-01 07:30:19','565424a4c70d3f3231f55b1f','2015-12-03 10:29:03','gg','',1,'loop',''),('565d4c95c70dbc9c50c61a51','hh2','','news','hh','csdn.net','csdn_net_news','','565424a4c70d3f3231f55b1f','2015-12-01 07:30:29','565424a4c70d3f3231f55b1f','2015-12-03 10:22:19','hh','',1,'loop',''),('565e5c6bc70d927749f42a15','xx','','news','xx','xx','','','565424a4c70d3f3231f55b1f','2015-12-02 02:50:19','565424a4c70d3f3231f55b1f','2015-12-02 06:27:27','xx','',1,'loop',''),('565e6b32c70d927749f42a16','yy2','','news','yy','yy','yy','','565424a4c70d3f3231f55b1f','2015-12-02 03:53:22','565424a4c70d3f3231f55b1f','2015-12-02 08:33:26','yy','',1,'loop','');
/*!40000 ALTER TABLE `spider_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `spider_status`
--

DROP TABLE IF EXISTS `spider_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `spider_status` (
  `status_id` varchar(30) DEFAULT NULL,
  `spider_id` varchar(30) DEFAULT NULL,
  `last_run_time` timestamp NULL DEFAULT NULL,
  `last_run_host` varchar(200) DEFAULT NULL,
  `success` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `spider_status`
--

LOCK TABLES `spider_status` WRITE;
/*!40000 ALTER TABLE `spider_status` DISABLE KEYS */;
/*!40000 ALTER TABLE `spider_status` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-12-03 20:51:23
