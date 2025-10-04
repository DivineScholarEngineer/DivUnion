-- MySQL schema for the DivUnion project.
--
-- This script focuses on the project-specific tables. Core Django tables
-- (auth_*, django_*, etc.) should be created automatically by running the
-- Django migrations once the database is provisioned.
--
-- Usage:
--   1. Run this script against your MySQL server.
--   2. Update DATABASES in settings.py or via environment variables to point
--      at the MySQL instance.
--   3. Execute `python manage.py migrate` to let Django finish configuring the
--      built-in tables and apply any future migrations.
--
-- The script also demonstrates how to create a dedicated database user. Feel
-- free to adjust credentials to match your environment.

CREATE DATABASE IF NOT EXISTS `divunion`
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'divunion_app'@'localhost'
  IDENTIFIED BY 'change-me';
GRANT ALL PRIVILEGES ON `divunion`.* TO 'divunion_app'@'localhost';
FLUSH PRIVILEGES;

USE `divunion`;

-- ---------------------------------------------------------------------------
-- Custom user table (accounts.CustomUser)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `accounts_customuser` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `password` VARCHAR(128) NOT NULL,
  `last_login` DATETIME(6) NULL,
  `is_superuser` BOOLEAN NOT NULL,
  `username` VARCHAR(150) NOT NULL,
  `first_name` VARCHAR(150) NOT NULL,
  `last_name` VARCHAR(150) NOT NULL,
  `email` VARCHAR(254) NOT NULL,
  `is_staff` BOOLEAN NOT NULL,
  `is_active` BOOLEAN NOT NULL,
  `date_joined` DATETIME(6) NOT NULL,
  `is_developer` BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_customuser_username_key` (`username`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `accounts_customuser_groups` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `customuser_id` BIGINT NOT NULL,
  `group_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_customuser_groups_unique` (`customuser_id`, `group_id`),
  KEY `accounts_customuser_groups_group_id_idx` (`group_id`),
  CONSTRAINT `accounts_customuser_groups_user_fk`
    FOREIGN KEY (`customuser_id`) REFERENCES `accounts_customuser` (`id`)
    ON DELETE CASCADE,
  CONSTRAINT `accounts_customuser_groups_group_fk`
    FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
    ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `accounts_customuser_user_permissions` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `customuser_id` BIGINT NOT NULL,
  `permission_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_customuser_user_permissions_unique` (`customuser_id`, `permission_id`),
  KEY `accounts_customuser_user_permissions_permission_idx` (`permission_id`),
  CONSTRAINT `accounts_customuser_user_permissions_user_fk`
    FOREIGN KEY (`customuser_id`) REFERENCES `accounts_customuser` (`id`)
    ON DELETE CASCADE,
  CONSTRAINT `accounts_customuser_user_permissions_permission_fk`
    FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
    ON DELETE CASCADE
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------------
-- Store app tables
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `store_category` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `slug` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `store_category_slug_key` (`slug`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `store_product` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `category_id` BIGINT NULL,
  `name` VARCHAR(200) NOT NULL,
  `slug` VARCHAR(50) NOT NULL,
  `description` LONGTEXT NOT NULL,
  `price` DECIMAL(10, 2) NOT NULL,
  `image` VARCHAR(100) NULL,
  `ebay_url` VARCHAR(200) NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `store_product_slug_key` (`slug`),
  KEY `store_product_category_idx` (`category_id`),
  CONSTRAINT `store_product_category_fk`
    FOREIGN KEY (`category_id`) REFERENCES `store_category` (`id`)
    ON DELETE SET NULL
) ENGINE=InnoDB;

-- End of schema -------------------------------------------------------------
