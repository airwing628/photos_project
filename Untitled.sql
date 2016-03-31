CREATE DATABASE  IF NOT EXISTS `photos_db` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `photos_db`;
-- MySQL dump 10.13  Distrib 5.7.9, for osx10.9 (x86_64)
--
-- Host: 127.0.0.1    Database: photos_db
-- ------------------------------------------------------
-- Server version	5.5.42

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
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `photo_id` int(11) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `comment` text,
  PRIMARY KEY (`id`),
  KEY `fk_comments_users1_idx` (`user_id`),
  KEY `fk_comments_photos1_idx` (`photo_id`),
  CONSTRAINT `fk_comments_photos1` FOREIGN KEY (`photo_id`) REFERENCES `photos` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_comments_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
INSERT INTO `comments` VALUES (1,1,20,'2016-03-30 16:38:19','2016-03-30 16:38:19','another comment test'),(2,1,22,'2016-03-30 16:39:49','2016-03-30 16:39:49','testing again'),(3,1,24,'2016-03-30 22:18:18','2016-03-30 22:18:18','My first commit'),(4,1,22,'2016-03-31 08:01:32','2016-03-31 08:01:32','I like this '),(5,1,22,'2016-03-31 08:02:18','2016-03-31 08:02:18','I really like this'),(6,1,22,'2016-03-31 08:03:27','2016-03-31 08:03:27','whats up');
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `likes`
--

DROP TABLE IF EXISTS `likes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `likes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `photo_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_likes_users1_idx` (`user_id`),
  KEY `fk_likes_photos1_idx` (`photo_id`),
  CONSTRAINT `fk_likes_photos1` FOREIGN KEY (`photo_id`) REFERENCES `photos` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_likes_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `likes`
--

LOCK TABLES `likes` WRITE;
/*!40000 ALTER TABLE `likes` DISABLE KEYS */;
/*!40000 ALTER TABLE `likes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `photos`
--

DROP TABLE IF EXISTS `photos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `photos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `category` varchar(45) DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  `small_url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `photos`
--

LOCK TABLES `photos` WRITE;
/*!40000 ALTER TABLE `photos` DISABLE KEYS */;
INSERT INTO `photos` VALUES (1,'https://s3-us-west-1.amazonaws.com/codingdojo/1001.JPG','2016-03-30 10:11:54','editorial',10,'https://s3-us-west-1.amazonaws.com/codingdojo/small/1001.jpg'),(2,'https://s3-us-west-1.amazonaws.com/codingdojo/1002.JPG','2016-03-30 10:12:48','editorial',12,'https://s3-us-west-1.amazonaws.com/codingdojo/small/1002.jpg'),(3,'https://s3-us-west-1.amazonaws.com/codingdojo/1003.JPG','2016-03-30 10:12:54','editorial',13,'https://s3-us-west-1.amazonaws.com/codingdojo/small/1003.jpg'),(4,'https://s3-us-west-1.amazonaws.com/codingdojo/1004.JPG','2016-03-30 10:13:04','editorial',14,'https://s3-us-west-1.amazonaws.com/codingdojo/small/1004.jpg'),(5,'https://s3-us-west-1.amazonaws.com/codingdojo/1005.JPG','2016-03-30 10:13:16','editorial',11,'https://s3-us-west-1.amazonaws.com/codingdojo/small/1005.jpg'),(6,'https://s3-us-west-1.amazonaws.com/codingdojo/1006.JPG','2016-03-30 10:13:55','editorial',10,'https://s3-us-west-1.amazonaws.com/codingdojo/small/1006.jpg'),(7,'https://s3-us-west-1.amazonaws.com/codingdojo/1007.JPG','2016-03-30 10:14:03','editorial',100,'https://s3-us-west-1.amazonaws.com/codingdojo/small/1007.jpg'),(8,'https://s3-us-west-1.amazonaws.com/codingdojo/1008.JPG','2016-03-30 10:14:08','editorial',100000,'https://s3-us-west-1.amazonaws.com/codingdojo/small/1008.jpg'),(9,'https://s3-us-west-1.amazonaws.com/codingdojo/1009.JPG','2016-03-30 10:14:12','editorial',8,'https://s3-us-west-1.amazonaws.com/codingdojo/small/1009.jpg'),(10,'https://s3-us-west-1.amazonaws.com/codingdojo/1010.JPG','2016-03-30 10:14:16','editorial',15,'https://s3-us-west-1.amazonaws.com/codingdojo/small/1010.jpg'),(11,'https://s3-us-west-1.amazonaws.com/codingdojo/1011.JPG','2016-03-30 10:14:22','editorial',20,'https://s3-us-west-1.amazonaws.com/codingdojo/small/1011.jpg'),(12,'https://s3-us-west-1.amazonaws.com/codingdojo/1012.JPG','2016-03-30 10:14:29','editorial',100,'https://s3-us-west-1.amazonaws.com/codingdojo/small/1012.jpg'),(13,'https://s3-us-west-1.amazonaws.com/codingdojo/2001.JPG','2016-03-30 10:15:24','landscapes',12,'https://s3-us-west-1.amazonaws.com/codingdojo/small/2001.jpg'),(14,'https://s3-us-west-1.amazonaws.com/codingdojo/2002.JPG','2016-03-30 10:15:31','landscapes',80,'https://s3-us-west-1.amazonaws.com/codingdojo/small/2002.jpg'),(15,'https://s3-us-west-1.amazonaws.com/codingdojo/2003.JPG','2016-03-30 10:15:36','landscapes',99,'https://s3-us-west-1.amazonaws.com/codingdojo/small/2003.jpg'),(16,'https://s3-us-west-1.amazonaws.com/codingdojo/2004.JPG','2016-03-30 10:15:40','landscapes',12,'https://s3-us-west-1.amazonaws.com/codingdojo/small/2004.jpg'),(17,'https://s3-us-west-1.amazonaws.com/codingdojo/2005.JPG','2016-03-30 10:15:44','landscapes',3,'https://s3-us-west-1.amazonaws.com/codingdojo/small/2005.jpg'),(18,'https://s3-us-west-1.amazonaws.com/codingdojo/2006.JPG','2016-03-30 10:15:48','landscapes',50,'https://s3-us-west-1.amazonaws.com/codingdojo/small/2006.jpg'),(19,'https://s3-us-west-1.amazonaws.com/codingdojo/2009.JPG','2016-03-30 10:16:07','landscapes',45,'https://s3-us-west-1.amazonaws.com/codingdojo/small/2009.jpg'),(20,'https://s3-us-west-1.amazonaws.com/codingdojo/3001.JPG','2016-03-30 10:16:30','sports',64,'https://s3-us-west-1.amazonaws.com/codingdojo/small/3001.jpg'),(21,'https://s3-us-west-1.amazonaws.com/codingdojo/3003.JPG','2016-03-30 10:16:35','sports',12,'https://s3-us-west-1.amazonaws.com/codingdojo/small/3003.jpg'),(22,'https://s3-us-west-1.amazonaws.com/codingdojo/3004.JPG','2016-03-30 10:16:43','sports',15,'https://s3-us-west-1.amazonaws.com/codingdojo/small/3004.jpg'),(23,'https://s3-us-west-1.amazonaws.com/codingdojo/3005.JPG','2016-03-30 10:16:59','sports',19,'https://s3-us-west-1.amazonaws.com/codingdojo/small/3005.jpg'),(24,'https://s3-us-west-1.amazonaws.com/codingdojo/3008.JPG','2016-03-30 10:17:05','sports',15,'https://s3-us-west-1.amazonaws.com/codingdojo/small/3008.jpg'),(25,'https://s3-us-west-1.amazonaws.com/codingdojo/3009.JPG','2016-03-30 10:17:16','sports',99,'https://s3-us-west-1.amazonaws.com/codingdojo/small/3009.jpg'),(26,'https://s3-us-west-1.amazonaws.com/codingdojo/3010.JPG','2016-03-30 10:17:21','sports',8,'https://s3-us-west-1.amazonaws.com/codingdojo/small/3010.jpg'),(27,'https://s3-us-west-1.amazonaws.com/codingdojo/3011.JPG','2016-03-30 10:17:25','sports',25,'https://s3-us-west-1.amazonaws.com/codingdojo/small/3011.jpg'),(28,'https://s3-us-west-1.amazonaws.com/codingdojo/3012.JPG','2016-03-30 10:17:30','sports',30,'https://s3-us-west-1.amazonaws.com/codingdojo/small/3012.jpg');
/*!40000 ALTER TABLE `photos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'sammy','dallal','sammydallal@gmail.com','$2b$12$ys94CL7fxMh2kNws2hamWOIAvD7kiphsuFvKUIhsSTxmw5EV4E1W2');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-03-31 13:49:55
