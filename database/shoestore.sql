-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: shoestore
-- ------------------------------------------------------
-- Server version	8.0.35

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Chọn cơ sở dữ liệu shoestore
USE shoestore;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `name` varchar(20) NOT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES ('Adidas',1),('Converse ',2),('Nike',3),('Vans',5);
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comment` (
  `content` varchar(255) NOT NULL,
  `product_id` int NOT NULL,
  `user_id` int NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `product_id` (`product_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`),
  CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
INSERT INTO `comment` VALUES ('Nice!!',3,1,'2023-12-17 21:05:24',1),('Good!!',3,1,'2023-12-17 21:05:24',2),('Tuyệt vời~~',4,1,'2023-12-17 21:05:24',3),('Quá đỉnh!',4,1,'2023-12-17 21:05:24',4);
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product` (
  `name` varchar(50) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `price` float DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  `category_id` int NOT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `product_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES ('Vans Old Skool','Vans Old Skool Classic trắng đen kinh điển',1665000,'images/vans.jpg',1,'2023-12-17 20:37:43',5,3),('Vans Checkerboard','Vans Old Skool Checkerboard được cách điệu từ dòng Classic ',1225000,'images/vans1.jpg',1,'2023-12-17 20:37:43',5,4),('Vans UA Old Skool','Vans Old Skool đã trở lại với thiết kế kinh điển của nhà Vans cùng tông màu All Black mạnh mẽ',1200000,'images/vans2.jpg',1,'2023-12-17 20:37:43',5,5),('Vans Authentic','Vans Authentic cổ điển xuất hiện hơn 50 năm nhưng vẫn chưa có dấu hiệu hạ nhiệt trong giới trẻ.',1305000,'images/vans3.jpg',1,'2023-12-17 20:37:43',5,6),('Adidas Ultraboost','Giày Adidas Ultraboost Light siêu phẩm giày thể thao mới nhất đến từ nhà Adidas',3990000,'images/adidas.jpg',1,'2023-12-17 20:37:43',1,7),('Adidas Tracefinder','Giày Adidas Tracefinder Trail mẫu giày dã ngoại cao cấp của Adidas',1790000,'images/adidas1.jpg',1,'2023-12-17 21:05:23',1,8),('Adidas Superstar','Giày Adidas Superstar mẫu giày sneaker huyền thoại nổi tiếng bậc nhất của Adidas.',2090000,'images/adidas2.jpg',1,'2023-12-17 21:05:23',1,9),('Adidas Ultrabounce','Giày Adidas Ultrabounce là mẫu giày thể thao mới nhất của Adidas',1990000,'images/adidas3.jpg',1,'2023-12-17 21:05:23',1,10),('Converse Lift Platform Canvas','Converse Lift Platform Canvas thiết kế đế Platform cao su dày dặn, với khuôn khổ và đường nét hài hòa.',1440000,'images/converse.jpg',1,'2023-12-17 21:05:23',2,11),('Converse Denim Fashion','Converse đã mang chất liệu denim cổ điển quay trở lại và thổi hồn vào thiết kế Converse Chuck Taylor All Star Denim Fashion.',1485000,'images/converse1.jpg',1,'2023-12-17 21:05:23',2,12),('Converse Lift Canvas','Phối màu cơ bản dễ mang, dễ diện, dễ phối đồ Đệm lót êm ái, tạo sự thoải mái và hỗ trợ di chuyển linh hoạt.',1530000,'images/converse2.jpg',1,'2023-12-17 21:05:23',2,13),('Converse Valentine\'s Day','Trở lại vào một dịp rất đặc biệt với phiên bản Chuck 70s trong BST Converse Valentine’s Day, các nhà thiết kế đã truyền đi thông điệp yêu thương qua lời nhắn “Made With Love” được thêu nổi bật trên thân giày.',1400000,'images/converse3.jpg',1,'2023-12-17 21:05:23',2,14),('Nike Revolution','Nike Revolution mẫu giày thể thao đến từ thương hiệu nổi tiếng của Mỹ được nhiều tín đồ thể thao ưa chuộng.',1350000,'images/nike.jpg',1,'2023-12-17 21:05:23',3,15),('Nike Downshifter ','Nike Downshifter phiên bản giày mới ra mắt của Nike với thiết kế hiện đại vô cùng thời trang.',1650000,'images/nike1.jpg',1,'2023-12-17 21:05:23',3,16),('Nike Running Shoes','Nike Running Shoes là mẫu giày thể thao được thiết kế mang nét trẻ trung, khỏe khắn.',1750000,'images/nike2.jpg',1,'2023-12-17 21:05:23',3,17),('Nike White Pink','Nike Air Force 1 White Pink là mẫu giày thể thao với thiết kế năng động.',2450000,'images/nike3.jpg',1,'2023-12-17 21:05:23',3,18);
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `receipt`
--

DROP TABLE IF EXISTS `receipt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receipt` (
  `create_date` datetime DEFAULT NULL,
  `user_id` int NOT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `receipt_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receipt`
--

LOCK TABLES `receipt` WRITE;
/*!40000 ALTER TABLE `receipt` DISABLE KEYS */;
INSERT INTO `receipt` VALUES ('2023-12-17 20:37:44',1,1),('2023-12-17 21:05:24',2,2);
/*!40000 ALTER TABLE `receipt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `receipt_detail`
--

DROP TABLE IF EXISTS `receipt_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receipt_detail` (
  `receipt_id` int NOT NULL,
  `product_id` int NOT NULL,
  `quantity` int DEFAULT NULL,
  `unit_price` float DEFAULT NULL,
  PRIMARY KEY (`receipt_id`,`product_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `receipt_detail_ibfk_1` FOREIGN KEY (`receipt_id`) REFERENCES `receipt` (`id`),
  CONSTRAINT `receipt_detail_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receipt_detail`
--

LOCK TABLES `receipt_detail` WRITE;
/*!40000 ALTER TABLE `receipt_detail` DISABLE KEYS */;
INSERT INTO `receipt_detail` VALUES (1,3,1,1665000),(1,4,4,1225000),(1,5,5,1200000),(2,4,1,1225000),(2,5,1,1200000),(2,6,4,1305000),(2,9,2,2090000),(2,12,2,1485000);
/*!40000 ALTER TABLE `receipt_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `name` varchar(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `avatar` varchar(100) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `joined_date` datetime DEFAULT NULL,
  `user_role` enum('ADMIN','USER') DEFAULT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('Admin','admin','$2b$12$dd4SQhoxKJa6MEZuxZFp0OO/F5F2tM6UeDy4gZ9nj2Ocss.meBJie',NULL,'admin@gmail.com',1,'2023-12-17 20:30:17','ADMIN',1),('thanhhien','thanhhien','$2b$12$e2NrqM6Hem.dIINkYLWqk.ZOU4aivzTn388mcERGukbWuZ4DVpxKK','https://res.cloudinary.com/dwgmes935/image/upload/v1702824836/ljwevggucwnblafycilu.jpg','thanhhien@gmail.com',1,'2023-12-17 21:05:24','USER',2);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-17 21:58:46
