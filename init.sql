-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 03, 2025 at 05:55 PM
-- Server version: 11.4.7-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tohru`
--

-- --------------------------------------------------------

--
-- Table structure for table `archives_audio`
--

CREATE TABLE `archives_audio` (
  `id` int(11) NOT NULL,
  `path` varchar(255) NOT NULL,
  `original_path` varchar(255) NOT NULL,
  `caption` varchar(255) NOT NULL,
  `submitter_id` bigint(20) DEFAULT NULL,
  `submission_time` timestamp NOT NULL DEFAULT current_timestamp(),
  `colour` tinytext DEFAULT '#f76d15'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `archives_image`
--

CREATE TABLE `archives_image` (
  `id` int(11) NOT NULL,
  `path` varchar(255) NOT NULL,
  `original_path` varchar(255) NOT NULL,
  `caption` varchar(255) NOT NULL,
  `submitter_id` bigint(20) DEFAULT NULL,
  `submission_time` timestamp NOT NULL DEFAULT current_timestamp(),
  `colour` tinytext DEFAULT '#f76d15'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `pools`
--

CREATE TABLE `pools` (
  `id` tinyint(4) NOT NULL COMMENT 'Unique internal ID of the Pool.',
  `name` tinytext NOT NULL COMMENT 'The visible name of the pool.',
  `user_id` bigint(20) NOT NULL COMMENT 'Who owns this Pool and can make changes to it?',
  `visible` tinyint(1) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `pools_content`
--

CREATE TABLE `pools_content` (
  `id` int(11) NOT NULL COMMENT 'Unique internal ID of this item for management reasons.',
  `pool_id` int(11) NOT NULL COMMENT 'ID of the Pool this item is attributed to.',
  `content` text NOT NULL COMMENT 'Internal ID of the item within it''s respective database as specified by the Pool.',
  `user_id` bigint(20) NOT NULL COMMENT 'Who added this to the pool?',
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() COMMENT 'When was this added to the pool?',
  `visible` tinyint(1) NOT NULL DEFAULT 1 COMMENT 'Instead of deleting items forever, we just untick their validity, letting us revert if we make a mistake.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `quotes`
--

CREATE TABLE `quotes` (
  `id` int(11) NOT NULL,
  `content` longtext NOT NULL,
  `author` text NOT NULL DEFAULT 'Anonymous',
  `submitter_id` bigint(20) DEFAULT NULL,
  `submission_time` timestamp NOT NULL DEFAULT current_timestamp(),
  `visible` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `stuff`
--

CREATE TABLE `stuff` (
  `id` int(11) NOT NULL,
  `type` tinytext NOT NULL,
  `name` text NOT NULL,
  `description` text NOT NULL,
  `fact` text NOT NULL,
  `image` text NOT NULL,
  `submitter_id` bigint(20) NOT NULL,
  `submission_time` timestamp NOT NULL DEFAULT current_timestamp(),
  `colour` tinytext DEFAULT '#f76d15',
  `visible` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tips`
--

CREATE TABLE `tips` (
  `id` int(11) NOT NULL,
  `content` longtext NOT NULL,
  `author` text NOT NULL DEFAULT 'Anonymous',
  `submitter_id` bigint(20) DEFAULT NULL,
  `submission_time` timestamp NOT NULL DEFAULT current_timestamp(),
  `visible` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` bigint(20) NOT NULL,
  `quote` text DEFAULT NULL,
  `image` int(11) DEFAULT NULL,
  `audio` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `archives_audio`
--
ALTER TABLE `archives_audio`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `archives_image`
--
ALTER TABLE `archives_image`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `pools`
--
ALTER TABLE `pools`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `pools_content`
--
ALTER TABLE `pools_content`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `quotes`
--
ALTER TABLE `quotes`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `stuff`
--
ALTER TABLE `stuff`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tips`
--
ALTER TABLE `tips`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD UNIQUE KEY `id` (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `archives_audio`
--
ALTER TABLE `archives_audio`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `archives_image`
--
ALTER TABLE `archives_image`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `pools`
--
ALTER TABLE `pools`
  MODIFY `id` tinyint(4) NOT NULL AUTO_INCREMENT COMMENT 'Unique internal ID of the Pool.';

--
-- AUTO_INCREMENT for table `pools_content`
--
ALTER TABLE `pools_content`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique internal ID of this item for management reasons.';

--
-- AUTO_INCREMENT for table `quotes`
--
ALTER TABLE `quotes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `stuff`
--
ALTER TABLE `stuff`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tips`
--
ALTER TABLE `tips`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
