-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 28, 2023 at 09:05 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `task_manager`
--

-- --------------------------------------------------------

--
-- Table structure for table `task`
--

CREATE TABLE `task` (
  `id` int(11) NOT NULL,
  `title` varchar(50) DEFAULT NULL,
  `due_date` datetime DEFAULT NULL,
  `attachment` varchar(255) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `task`
--

INSERT INTO `task` (`id`, `title`, `due_date`, `attachment`, `user_id`) VALUES
(2, 'Update on current project meet with Client', '2023-12-30 23:59:59', 'E:/DS_Work/DS_Work/Datasets/Predict_BMI.csv', 5);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `public_id` varchar(255) DEFAULT NULL,
  `name` varchar(20) DEFAULT NULL,
  `email` varchar(20) NOT NULL,
  `password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `public_id`, `name`, `email`, `password`) VALUES
(2, '802b2f76-8361-4513-aa26-71c8cb38b8f3', 'Dhiraj', 'dhiraj@gmail.com', 'pbkdf2:sha256:600000'),
(3, '1fd85767-237a-4d9a-8cc7-fbeedae8b4fe', 'Pragati', 'pragati@gmail.com', 'pbkdf2:sha256:600000'),
(4, '7ebda9f1-eaf9-4c0f-bdbd-006303741a4e', 'Suraj', 'suraj@gmail.com', 'pbkdf2:sha256:600000'),
(5, '4bdb304c-cd03-494e-83ee-6929f2ddcfcc', 'Shreya', 'shreya@gmail.com', 'pbkdf2:sha256:600000$DNEXCcDoWIIeY2CS$208c6094edac36e50e1662dcdc76c83aa3af7ab40f8379aa942c578eb9e7ccfd'),
(6, '84217cc6-6152-4d0e-8a38-de70551eba04', 'Shiva', 'shiva@gmail.com', 'pbkdf2:sha256:600000$0IDXOQOdkmbDAoGs$f2d77c8d352805ee3595bcacc492fab4996b2b641dab0641d190e7ddf46289ad');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `task`
--
ALTER TABLE `task`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `public_id` (`public_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `task`
--
ALTER TABLE `task`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `task`
--
ALTER TABLE `task`
  ADD CONSTRAINT `task_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
