-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: skincare
-- ------------------------------------------------------
-- Server version	8.0.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `addresses`
--


/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `addresses` (
  `address_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `full_address` text,
  `city` varchar(100) DEFAULT NULL,
  `pincode` varchar(10) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`address_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `addresses`
--

LOCK TABLES `addresses` WRITE;
/*!40000 ALTER TABLE `addresses` DISABLE KEYS */;
/*!40000 ALTER TABLE `addresses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cart`
--


/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cart` (
  `cart_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `product_id` int DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  PRIMARY KEY (`cart_id`),
  KEY `user_id` (`user_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `cart_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart`
--

LOCK TABLES `cart` WRITE;
/*!40000 ALTER TABLE `cart` DISABLE KEYS */;
INSERT INTO `cart` VALUES (1,1,1,3),(2,1,3,1),(3,2,2,1),(4,2,5,3),(39,1,2,1),(58,1,18,1);
/*!40000 ALTER TABLE `cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `concerns`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `concerns` (
  `concern_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`concern_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `concerns`
--

LOCK TABLES `concerns` WRITE;
/*!40000 ALTER TABLE `concerns` DISABLE KEYS */;
INSERT INTO `concerns` VALUES (1,'Acne Marks'),(2,'Pigmentation / Dark Spots'),(3,'Acne / Pimple'),(4,'Acne Scars'),(5,'Open Pores'),(6,'Dry & Dull Skin'),(7,'View All Products');
/*!40000 ALTER TABLE `concerns` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `coupons`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `coupons` (
  `coupon_id` int NOT NULL AUTO_INCREMENT,
  `code` varchar(50) DEFAULT NULL,
  `discount_percent` int DEFAULT NULL,
  `active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`coupon_id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coupons`
--

LOCK TABLES `coupons` WRITE;
/*!40000 ALTER TABLE `coupons` DISABLE KEYS */;
INSERT INTO `coupons` VALUES (1,'GLOW10',10,1),(2,'SKIN20',20,1),(3,'WELCOME15',15,1);
/*!40000 ALTER TABLE `coupons` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ingredients`
--


/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ingredients` (
  `ingredient_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ingredient_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingredients`
--

LOCK TABLES `ingredients` WRITE;
/*!40000 ALTER TABLE `ingredients` DISABLE KEYS */;
INSERT INTO `ingredients` VALUES (1,'Niacinamide Range'),(2,'Salicylic Range'),(3,'Vitamin C Range'),(4,'AHA-BHA Range'),(5,'Kojic Range'),(6,'Hyaluronic Range'),(7,'View All Products');
/*!40000 ALTER TABLE `ingredients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_items`
--


/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_id` int DEFAULT NULL,
  `product_id` int DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `order_id` (`order_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`),
  CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_items`
--

LOCK TABLES `order_items` WRITE;
/*!40000 ALTER TABLE `order_items` DISABLE KEYS */;
INSERT INTO `order_items` VALUES (1,1,1,2,299.00),(2,1,3,1,349.00),(3,2,2,1,499.00),(4,2,5,1,299.00),(5,3,3,1,349.00),(6,3,5,1,299.00),(7,3,10,2,299.00),(8,3,4,1,399.00),(9,4,1,3,299.00),(10,4,2,2,499.00),(11,4,18,2,199.00),(12,4,3,1,349.00),(13,4,5,1,299.00),(14,5,2,1,499.00),(15,5,13,1,399.00),(16,5,15,2,349.00),(17,6,1,1,299.00),(18,6,2,1,499.00),(19,6,3,1,349.00),(20,7,3,1,349.00),(21,7,19,1,299.00),(22,8,1,1,299.00),(23,8,17,1,699.00),(24,8,13,1,399.00),(25,8,12,1,499.00),(26,9,9,1,259.00),(27,9,8,2,599.00),(28,9,1,1,299.00),(29,9,4,1,399.00),(30,10,3,1,349.00),(31,10,5,1,299.00),(32,11,2,1,499.00),(33,11,3,1,349.00),(34,11,4,1,399.00),(35,12,1,1,299.00),(36,12,8,1,599.00),(37,13,3,3,349.00),(38,13,4,2,399.00),(39,13,12,1,499.00),(40,13,2,1,499.00),(41,14,1,1,299.00),(42,14,4,1,399.00),(43,14,8,1,599.00),(44,14,13,1,399.00),(45,15,7,1,349.00),(46,15,17,1,699.00),(47,15,15,1,349.00),(48,15,12,1,499.00),(49,16,21,1,234.00),(50,16,9,1,259.00),(51,16,6,1,279.00),(52,16,10,1,299.00),(53,16,5,1,299.00),(54,17,1,1,299.00),(55,17,2,1,499.00),(56,17,3,1,349.00),(57,18,2,1,499.00);
/*!40000 ALTER TABLE `order_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--


/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `order_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `total_amount` decimal(10,2) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `address_id` int DEFAULT NULL,
  PRIMARY KEY (`order_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,1,1098.00,'Completed','2026-04-30 15:09:03',NULL),(2,2,799.00,'Pending','2026-04-30 15:09:03',NULL),(3,5,1645.00,'Placed','2026-05-01 10:16:43',NULL),(4,4,2941.00,'Placed','2026-05-04 04:50:01',NULL),(5,4,1596.00,'Placed','2026-05-04 04:55:46',NULL),(6,4,1147.00,'Placed','2026-05-04 04:59:06',NULL),(7,5,648.00,'Placed','2026-05-05 03:09:23',NULL),(8,5,1896.00,'Placed','2026-05-05 03:17:28',NULL),(9,4,2155.00,'Placed','2026-05-05 03:27:20',NULL),(10,5,648.00,'Placed','2026-05-05 03:37:40',NULL),(11,5,1247.00,'Placed','2026-05-05 03:42:17',NULL),(12,4,898.00,'Placed','2026-05-05 03:46:30',NULL),(13,4,2843.00,'Placed','2026-05-05 05:19:37',NULL),(14,4,1696.00,'Placed','2026-05-05 06:33:33',NULL),(15,4,1896.00,'Placed','2026-05-14 06:17:30',NULL),(16,4,1370.00,'Placed','2026-05-14 07:28:41',NULL),(17,4,1147.00,'Placed','2026-05-19 15:23:21',NULL),(18,5,499.00,'Placed','2026-05-19 15:27:41',NULL);
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments`
--


/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments` (
  `payment_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `method` varchar(50) DEFAULT NULL,
  `details` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`payment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments`
--

LOCK TABLES `payments` WRITE;
/*!40000 ALTER TABLE `payments` DISABLE KEYS */;
/*!40000 ALTER TABLE `payments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_concerns`
--


/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_concerns` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int DEFAULT NULL,
  `concern_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `product_id` (`product_id`),
  KEY `concern_id` (`concern_id`),
  CONSTRAINT `product_concerns_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`),
  CONSTRAINT `product_concerns_ibfk_2` FOREIGN KEY (`concern_id`) REFERENCES `concerns` (`concern_id`)
) ENGINE=InnoDB AUTO_INCREMENT=103 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_concerns`
--

LOCK TABLES `product_concerns` WRITE;
/*!40000 ALTER TABLE `product_concerns` DISABLE KEYS */;
INSERT INTO `product_concerns` VALUES (26,1,3),(27,2,3),(28,3,3),(29,4,3),(30,5,3),(31,6,5),(32,7,3),(33,8,5),(34,9,3),(35,10,3),(36,11,6),(37,12,2),(38,13,6),(39,14,6),(40,15,6),(41,16,2),(42,17,6),(43,18,6),(44,19,2),(45,20,6),(46,2,1),(47,12,1),(48,16,1),(49,8,5),(50,10,5),(51,21,1),(52,21,3),(53,21,6),(54,21,7),(55,2,1),(56,8,1),(57,9,1),(58,16,1),(59,12,2),(60,16,2),(61,19,2),(62,20,2),(63,1,3),(64,2,3),(65,3,3),(66,5,3),(67,6,3),(68,9,3),(69,10,3),(70,2,4),(71,8,4),(72,16,4),(73,17,4),(74,6,5),(75,8,5),(76,10,5),(77,5,5),(78,11,6),(79,13,6),(80,17,6),(81,18,6),(82,20,6),(83,1,7),(84,2,7),(85,3,7),(86,4,7),(87,5,7),(88,6,7),(89,7,7),(90,8,7),(91,9,7),(92,10,7),(93,11,7),(94,12,7),(95,13,7),(96,14,7),(97,15,7),(98,16,7),(99,17,7),(100,18,7),(101,19,7),(102,20,7);
/*!40000 ALTER TABLE `product_concerns` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_ingredients`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_ingredients` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int DEFAULT NULL,
  `ingredient_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `product_id` (`product_id`),
  KEY `ingredient_id` (`ingredient_id`),
  CONSTRAINT `product_ingredients_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`),
  CONSTRAINT `product_ingredients_ibfk_2` FOREIGN KEY (`ingredient_id`) REFERENCES `ingredients` (`ingredient_id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_ingredients`
--

LOCK TABLES `product_ingredients` WRITE;
/*!40000 ALTER TABLE `product_ingredients` DISABLE KEYS */;
INSERT INTO `product_ingredients` VALUES (1,1,1),(2,4,1),(3,7,1),(4,8,1),(5,2,2),(6,3,2),(7,5,2),(8,6,2),(9,9,2),(10,10,2),(11,12,3),(12,16,3),(13,19,3),(14,5,4),(15,10,4),(16,19,4),(17,12,5),(18,16,5),(19,19,5),(20,11,6),(21,13,6),(22,14,6),(23,15,6),(24,17,6),(25,18,6),(26,20,6),(27,2,1),(28,8,2),(29,16,6),(30,21,1),(31,21,2),(32,21,7);
/*!40000 ALTER TABLE `product_ingredients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--


/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `product_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) DEFAULT NULL,
  `description` text,
  `price` decimal(10,2) DEFAULT NULL,
  `stock` int DEFAULT NULL,
  `image_url` text,
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'Oil Control Face Wash','Removes excess oil and prevents acne',299.00,50,'oil_cleanser.jpg'),(2,'Acne Control Serum','Reduces acne and controls sebum',499.00,40,'acne_serum.jpg'),(3,'Tea Tree Face Wash','Anti-bacterial face wash for acne skin',349.00,60,'teatree.jpg'),(4,'Mattifying Moisturizer','Controls oil and hydrates skin',399.00,30,'matt_moist.jpg'),(5,'Salicylic Acid Toner','Unclogs pores and reduces breakouts',299.00,45,'salicylic_toner.jpg'),(6,'Charcoal Cleanser','Deep cleans pores and removes dirt',279.00,50,'charcoal_cleanser.jpg'),(7,'Oil Free Sunscreen SPF 50','Protects from UV without making skin oily',349.00,70,'oilfree_sunscreen.jpg'),(8,'Pore Minimizing Serum','Tightens pores and smoothens skin',599.00,25,'pore_serum.jpg'),(9,'Anti Acne Gel','Targets acne spots and reduces redness',259.00,40,'acne_gel.jpg'),(10,'Clay Face Mask','Absorbs oil and detoxifies skin',299.00,35,'clay_mask.jpg'),(11,'Hydrating Face Wash','Gentle cleanser for all skin types',299.00,60,'hydrating_fw.jpg'),(12,'Vitamin C Serum','Brightens skin and reduces pigmentation',499.00,50,'vitc.jpg'),(13,'Daily Moisturizer','Keeps skin hydrated all day',399.00,45,'daily_moist.jpg'),(14,'Gentle Cleanser','Mild cleanser suitable for daily use',279.00,55,'gentle_cleanser.jpg'),(15,'SPF 50 Sunscreen','Broad spectrum sun protection',349.00,80,'sunscreen.jpg'),(16,'Glow Serum','Enhances skin glow and radiance',599.00,30,'glow_serum.jpg'),(17,'Night Repair Cream','Repairs skin overnight',699.00,20,'night_cream.jpg'),(18,'Aloe Vera Gel','Soothes and hydrates skin',199.00,100,'aloe.jpg'),(19,'Brightening Toner','Evens skin tone and refreshes',299.00,50,'bright_toner.jpg'),(20,'Hydration Boost Serum','Deep hydration for soft skin',549.00,35,'hydration_serum.jpg'),(21,'10% niacinamide serum','helpful for acne marks ',234.00,12,'or-pr_timetable.jpeg');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--


/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `review_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `product_id` int DEFAULT NULL,
  `rating` int DEFAULT NULL,
  `comment` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`review_id`),
  KEY `user_id` (`user_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=250 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
INSERT INTO `reviews` VALUES (163,1,1,5,'Amazing face wash, controls oil perfectly!','2026-04-30 15:24:34'),(164,2,1,4,'Good for oily skin, works well','2026-04-30 15:24:34'),(165,3,1,5,'Best cleanser I have used','2026-04-30 15:24:34'),(166,4,1,4,'Removes oil without drying skin','2026-04-30 15:24:34'),(167,1,2,5,'Helped reduce my acne in few weeks','2026-04-30 15:24:34'),(168,2,2,4,'Very effective serum','2026-04-30 15:24:34'),(169,3,2,5,'Lightweight and works great','2026-04-30 15:24:34'),(170,4,2,3,'Took time but shows results','2026-04-30 15:24:34'),(171,1,3,5,'Refreshing and good for acne','2026-04-30 15:24:34'),(172,2,3,4,'Nice smell and effective','2026-04-30 15:24:34'),(173,3,3,4,'Good daily cleanser','2026-04-30 15:24:34'),(174,4,3,5,'Loved it for oily skin','2026-04-30 15:24:34'),(175,1,4,4,'Keeps skin matte all day','2026-04-30 15:24:34'),(176,2,4,5,'Perfect for oily skin','2026-04-30 15:24:34'),(177,3,4,4,'Hydrates well without oiliness','2026-04-30 15:24:34'),(178,4,4,3,'Average but okay','2026-04-30 15:24:34'),(179,1,5,5,'Reduced my breakouts quickly','2026-04-30 15:24:34'),(180,2,5,4,'Very effective toner','2026-04-30 15:24:34'),(181,3,5,5,'Clears pores nicely','2026-04-30 15:24:34'),(182,4,5,4,'Good for acne-prone skin','2026-04-30 15:24:34'),(183,1,6,5,'Deep cleans my skin','2026-04-30 15:24:34'),(184,2,6,4,'Removes dirt well','2026-04-30 15:24:34'),(185,3,6,4,'Good but slightly drying','2026-04-30 15:24:34'),(186,4,6,5,'Loved the result','2026-04-30 15:24:34'),(187,1,7,5,'No white cast, amazing','2026-04-30 15:24:34'),(188,2,7,4,'Lightweight sunscreen','2026-04-30 15:24:34'),(189,3,7,5,'Perfect for daily use','2026-04-30 15:24:34'),(190,4,7,4,'Non greasy and smooth','2026-04-30 15:24:34'),(191,1,8,5,'Pores look smaller now','2026-04-30 15:24:34'),(192,2,8,4,'Good serum','2026-04-30 15:24:34'),(193,3,8,4,'Works slowly but good','2026-04-30 15:24:34'),(194,4,8,5,'Skin feels smoother','2026-04-30 15:24:34'),(195,1,9,5,'Works instantly on pimples','2026-04-30 15:24:34'),(196,2,9,4,'Reduces redness','2026-04-30 15:24:34'),(197,3,9,5,'Must have for acne','2026-04-30 15:24:34'),(198,4,9,4,'Good spot treatment','2026-04-30 15:24:34'),(199,1,10,5,'Removes oil instantly','2026-04-30 15:24:34'),(200,2,10,4,'Good detox mask','2026-04-30 15:24:34'),(201,3,10,5,'Skin feels clean','2026-04-30 15:24:34'),(202,4,10,4,'Nice weekly mask','2026-04-30 15:24:34'),(203,1,11,5,'Very gentle and hydrating','2026-04-30 15:24:34'),(204,2,11,4,'Good for dry skin','2026-04-30 15:24:34'),(205,3,11,5,'Does not dry skin','2026-04-30 15:24:34'),(206,4,11,4,'Nice cleanser','2026-04-30 15:24:34'),(207,1,12,5,'Gives glow to skin','2026-04-30 15:24:34'),(208,2,12,4,'Brightens well','2026-04-30 15:24:34'),(209,3,12,5,'Good for pigmentation','2026-04-30 15:24:34'),(210,4,12,4,'Visible results','2026-04-30 15:24:34'),(211,1,13,5,'Perfect daily moisturizer','2026-04-30 15:24:34'),(212,2,13,4,'Hydrates well','2026-04-30 15:24:34'),(213,3,13,5,'Very lightweight','2026-04-30 15:24:34'),(214,4,13,4,'Nice product','2026-04-30 15:24:34'),(215,1,14,5,'Very mild and soothing','2026-04-30 15:24:34'),(216,2,14,4,'Good for sensitive skin','2026-04-30 15:24:34'),(217,3,14,5,'Loved it','2026-04-30 15:24:34'),(218,4,14,4,'Works well','2026-04-30 15:24:34'),(219,1,15,5,'Great protection','2026-04-30 15:24:34'),(220,2,15,4,'No irritation','2026-04-30 15:24:34'),(221,3,15,5,'Perfect sunscreen','2026-04-30 15:24:34'),(222,4,15,4,'Nice finish','2026-04-30 15:24:34'),(223,1,16,5,'Skin looks radiant','2026-04-30 15:24:34'),(224,2,16,4,'Nice glow effect','2026-04-30 15:24:34'),(225,3,16,5,'Loved the finish','2026-04-30 15:24:34'),(226,4,16,4,'Good product','2026-04-30 15:24:34'),(227,1,17,5,'Skin feels repaired overnight','2026-04-30 15:24:34'),(228,2,17,4,'Good night cream','2026-04-30 15:24:34'),(229,3,17,5,'Very nourishing','2026-04-30 15:24:34'),(230,4,17,4,'Nice texture','2026-04-30 15:24:34'),(231,1,18,5,'Very soothing','2026-04-30 15:24:34'),(232,2,18,4,'Good for irritation','2026-04-30 15:24:34'),(233,3,18,5,'Multi-use product','2026-04-30 15:24:34'),(234,4,18,4,'Nice gel','2026-04-30 15:24:34'),(235,1,19,5,'Evens skin tone','2026-04-30 15:24:34'),(236,2,19,4,'Nice toner','2026-04-30 15:24:34'),(237,3,19,5,'Gives glow','2026-04-30 15:24:34'),(238,3,19,4,'Good product','2026-04-30 15:24:34'),(239,4,19,4,'Good product','2026-04-30 15:24:34'),(240,1,20,5,'Deep hydration','2026-04-30 15:24:34'),(241,2,20,4,'Skin feels soft','2026-04-30 15:24:34'),(242,3,20,5,'Very effective','2026-04-30 15:24:34'),(243,4,20,4,'Nice serum','2026-04-30 15:24:34'),(244,4,1,3,'this is nice product','2026-05-01 09:38:11'),(245,4,10,4,'good product','2026-05-01 09:39:18'),(246,4,10,3,'face mask is very nice to use no itching\r\n','2026-05-01 09:43:22'),(247,5,17,4,'nice creame','2026-05-01 10:16:18'),(248,4,3,1,'good product','2026-05-13 06:11:48'),(249,4,3,5,'this is nice product','2026-05-19 15:22:39');
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--


/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `active` tinyint(1) NOT NULL,
  `is_admin` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Anushka','anushka123@gmail.com','scrypt:32768:8:1$C8cvT20eMSryyDyA$bcd92eeb973958ed907024ef1d3eb42bdada62819509ef69ff58e37c1b60017c03e5509774e899ee9e6a144d57429ea2a44d847be2ecce0dc7badea8911cd511','2026-04-30 14:41:47',1,0),(2,'Anushka','anu@gmail.com','1234',NULL,1,0),(3,'Nikhil','nikhil123@gmail.com','scrypt:32768:8:1$9Tqj6FTrQr35P2Q0$15e53ccc3fff2bd3237ac86daddf92d9672055eb4da70acb5863f807e109b871eb2a7e2ac232c513c0769faa3a88e4100c59eb96c9ecec55b51db49237df0e86','2026-04-30 15:23:36',1,0),(4,'shweta','shweta123@gmail.com','scrypt:32768:8:1$Kcowq4gFUpmY5Zc4$c28335077eec1eef6a5b8cdb31c24885ac285821b4401562123363ee72bb8114c269978102beef9766b43fb8b227f8864927a054a6360bf87cb1f907d006e561','2026-04-30 15:24:10',1,0),(5,'Dipa','dipa123@gmail.com','scrypt:32768:8:1$v6QYadLsHBkWARVg$7d7790bea11d509063025e290ab6bdc6816be1d589ccca39bc1e8944b0a36bd8e878bc2fabbf691f3dd11605b62ca6809692475cf99972d55d43b5d67f35227b','2026-05-01 10:15:12',1,0);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wishlist`
--


/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wishlist` (
  `wishlist_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `product_id` int DEFAULT NULL,
  PRIMARY KEY (`wishlist_id`),
  UNIQUE KEY `user_id` (`user_id`,`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wishlist`
--

LOCK TABLES `wishlist` WRITE;
/*!40000 ALTER TABLE `wishlist` DISABLE KEYS */;
INSERT INTO `wishlist` VALUES (3,1,5),(11,1,6),(13,1,11),(4,1,18),(7,4,1),(8,4,2),(6,4,3),(9,4,4),(5,4,5),(10,4,12);
/*!40000 ALTER TABLE `wishlist` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-20 12:37:08
