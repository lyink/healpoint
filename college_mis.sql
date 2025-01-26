-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 29, 2023 at 06:20 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `college_mis`
--

-- --------------------------------------------------------

--
-- Table structure for table `app1_announcements`
--

CREATE TABLE `app1_announcements` (
  `id` bigint(20) NOT NULL,
  `heading` varchar(200) NOT NULL,
  `title` varchar(200) NOT NULL,
  `date_registered` date NOT NULL,
  `file` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `app1_announcements`
--

INSERT INTO `app1_announcements` (`id`, `heading`, `title`, `date_registered`, `file`) VALUES
(1, 'SECOND YEAR', 'SECOND YEAR', '2022-12-31', 'announcements/SECOND_YEAR.pdf'),
(2, 'Regulations for Undergraduate   Programmes_Final', 'Regulations for Undergraduate   Programmes_Final', '2022-12-31', 'announcements/Regulations_for_Undergraduate___Programmes_Final.pdf'),
(3, 'CERTIFICATE OF APPRECIATION 2', 'CERTIFICATE OF APPRECIATION 2', '2022-12-31', 'announcements/CERTIFICATE_OF_APPRECIATION_2.pdf'),
(4, 'TANGAZO ACCOMODATAION', 'TANGAZO ACCOMODATAION', '2022-12-31', 'announcements/TANGAZO_ACCOMODATAION.pdf'),
(5, 'undergraduate_curriculum_guidebook_2021_2022', 'undergraduate_curriculum_guidebook_2021_2022', '2022-12-31', 'announcements/undergraduate_curriculum_guidebook_2021_2022.pdf'),
(6, 'Teaching Matrix', 'Teaching Matrix', '2022-12-31', 'announcements/Teaching_Matrix.pdf'),
(7, 'FYP Supervission form', 'FYP Supervission form', '2022-12-31', 'announcements/FYP_Supervission_form.pdf'),
(8, 'Announcement to All Students', 'Announcement to All Students _ Registration for Semester Two 2021-2022 Academic Year', '2022-12-31', 'announcements/Announcement_to_All_Students___Registration_for_Semester_Two_2021-2022_Aca_NlKeU16.pdf'),
(9, 'ALMANAC_notice_21', 'ALMANAC_notice', '2022-12-31', 'announcements/ALMANAC_notice_21.pdf'),
(10, 'mkutano', 'mkutano today', '2022-12-31', 'announcements/Weekly-study-timetable.pdf');

-- --------------------------------------------------------

--
-- Table structure for table `app1_course`
--

CREATE TABLE `app1_course` (
  `id` bigint(20) NOT NULL,
  `course_name` varchar(200) NOT NULL,
  `program_id` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `app1_department`
--

CREATE TABLE `app1_department` (
  `department_name` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `app1_department`
--

INSERT INTO `app1_department` (`department_name`) VALUES
('Academic Affairs'),
('Academic Success Center'),
('Accountability and Assessment'),
('Accounting, Economics & Finance'),
('Administration and Finance'),
('Admissions Undergraduate'),
('Education, Health and Human Svcs (School of)'),
('Environmental Health and Safety'),
('EOC Business and Info Technology'),
('EOC Community Relations'),
('Human Resource');

-- --------------------------------------------------------

--
-- Table structure for table `app1_herroes`
--

CREATE TABLE `app1_herroes` (
  `id` bigint(20) NOT NULL,
  `full_name` varchar(200) NOT NULL,
  `heading` varchar(200) NOT NULL,
  `title` varchar(100) NOT NULL,
  `image` varchar(100) NOT NULL,
  `date_registered` date NOT NULL,
  `department_id` varchar(200) NOT NULL,
  `program_id` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `app1_herroes`
--

INSERT INTO `app1_herroes` (`id`, `full_name`, `heading`, `title`, `image`, `date_registered`, `department_id`, `program_id`) VALUES
(1, 'Nicole Lea Green', 'Most innovative', 'Best_Student', 'herroes/6f4c178c12d79514d2f32d9fb09d6a16.jpg', '2022-12-31', 'EOC Business and Info Technology', 'Department of Civil & Environmental Engineering'),
(2, 'Benjamin James Adams', 'Most innovative', 'Best_Staff', 'herroes/istockphoto-1196211150-170667a.jpg', '2022-12-31', 'EOC Business and Info Technology', 'Bachelor of Accounting Sciences in Financial Accounting . (98302 – FAC)'),
(3, 'Philip John Bontrager', 'Most innovative', 'Best_Footbal_Winner', 'herroes/Steven-Wambua-e1655995248680.jpg', '2022-12-31', 'Accounting, Economics & Finance', 'Department of Mechanical Engineering'),
(4, 'Bianca Magali Brambila', 'Most innovative', 'Best_Leader', 'herroes/Rosalynn-Nankya-Photo.jpg', '2022-12-31', 'Accounting, Economics & Finance', 'Advanced Diploma in Accounting Sciences Internal Auditing (98230 – AUI)'),
(5, 'Elizabeth L. Core', 'Most innovative', 'Best_Student', 'herroes/Ewura-Photo.jpg', '2022-12-31', 'EOC Business and Info Technology', 'Diploma in Agricultural Management (90097)'),
(6, 'Hayden Joel Goerzen', 'Most innovative /Researcher', 'Best_Student', 'herroes/Patrick-Cobbinah-796x1024.jpg', '2022-12-31', 'EOC Business and Info Technology', 'Diploma in Agricultural Management (90097)'),
(7, 'Erica Rose Grasse', 'Most innovative', 'Best_Staff', 'herroes/OREOLUWAS-PICTURE-scaled-p8zqdr1trxqm0mas9rjjmz63l6buat3wjbbegstdfk.jpg', '2022-12-31', 'EOC Business and Info Technology', 'Diploma in Agricultural Management (90097)'),
(8, 'Joseph Roman Gunden', 'Most innovative', 'Best_Staff', 'herroes/passport.jpg', '2022-12-31', 'Accounting, Economics & Finance', 'Advanced Diploma in Accounting Sciences Internal Auditing (98230 – AUI)'),
(9, 'Mia Carlene Engle', 'Most innovative', 'Best_Staff', 'herroes/Uwizeye_Glorieuse_web_.jpg', '2022-12-31', 'Environmental Health and Safety', 'Bachelor of Accounting Sciences in Financial Accounting . (98302 – FAC)'),
(10, 'samir said', 'Most innovative', 'Best_Leader', 'herroes/herro.jpg', '2022-12-31', 'Accounting, Economics & Finance', 'Advanced Diploma in Accounting Sciences Internal Auditing (98230 – AUI)'),
(11, 'Akiba', 'Most innovative', 'Best_Student', 'herroes/istockphoto-1196211150-170667a_ph8LWwj.jpg', '2022-12-31', 'EOC Business and Info Technology', 'Bachelor of Accounting Sciences in Financial Accounting . (98302 – FAC)');

-- --------------------------------------------------------

--
-- Table structure for table `app1_programs`
--

CREATE TABLE `app1_programs` (
  `program_name` varchar(200) NOT NULL,
  `program_duration` int(11) NOT NULL,
  `program_fee_currency` varchar(3) NOT NULL,
  `program_fee` decimal(14,2) NOT NULL,
  `date_registered` date NOT NULL,
  `department_id` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `app1_programs`
--

INSERT INTO `app1_programs` (`program_name`, `program_duration`, `program_fee_currency`, `program_fee`, `date_registered`, `department_id`) VALUES
('Advanced Diploma in Accounting Sciences Financial Accounting (98230 – FAC)', 3, 'TZS', '1200000.00', '2022-12-31', 'Accounting, Economics & Finance'),
('Advanced Diploma in Accounting Sciences Internal Auditing (98230 – AUI)', 3, 'TZS', '1200000.00', '2022-12-31', 'Accountability and Assessment'),
('Bachelor of Accounting Sciences in Financial Accounting . (98302 – FAC)', 3, 'TZS', '1200000.00', '2022-12-31', 'Accountability and Assessment'),
('Bachelor of Accounting Sciences in Internal Auditing . (98303 – AUI)', 3, 'TZS', '12000000.00', '2022-12-31', 'Accounting, Economics & Finance'),
('Communication and Media', 3, 'TZS', '1200000.00', '2022-12-31', 'EOC Business and Info Technology'),
('Community Development', 3, 'TZS', '1200000.00', '2022-12-31', 'Academic Success Center'),
('Dan F. Smith Department of Chemical and Biomolecular Engineering', 3, 'TZS', '1200000.00', '2022-12-31', 'Accounting, Economics & Finance'),
('Deaf Studies and Deaf Education', 3, 'TZS', '1200000.00', '2022-12-31', 'EOC Business and Info Technology'),
('Department of Civil & Environmental Engineering', 3, 'TZS', '200000.00', '2022-12-31', 'EOC Business and Info Technology'),
('Department of Industrial and Systems Engineering', 4, 'TZS', '1300000.00', '2022-12-31', 'Environmental Health and Safety'),
('Department of Mechanical Engineering', 2, 'TZS', '1200000.00', '2022-12-31', 'EOC Business and Info Technology'),
('Diploma in Accounting Sciences (98200)', 3, 'TZS', '1200000.00', '2022-12-31', 'Academic Success Center'),
('Diploma in Administrative Management (98216)', 3, 'TZS', '1200000.00', '2022-12-31', 'Academic Success Center'),
('Diploma in Agricultural Management (90097)', 3, 'TZS', '1200000.00', '2022-12-31', 'EOC Business and Info Technology'),
('Phillip M. Drayer Department of Electrical Engineering', 3, 'TZS', '1200000.00', '2022-12-31', 'Academic Success Center');

-- --------------------------------------------------------

--
-- Table structure for table `app1_student`
--

CREATE TABLE `app1_student` (
  `regno` varchar(200) NOT NULL,
  `full_name` varchar(200) NOT NULL,
  `passport_size` varchar(100) NOT NULL,
  `application_form` varchar(100) NOT NULL,
  `date_registered` date NOT NULL,
  `resident` varchar(100) NOT NULL,
  `program_id` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `app1_student`
--

INSERT INTO `app1_student` (`regno`, `full_name`, `passport_size`, `application_form`, `date_registered`, `resident`, `program_id`) VALUES
('2023/2024/t/001', 'hafsa said', 'passports/8612d8a0f64d6ac4e39094cf19709d0a.jpg', 'applications/Admission_Form.pdf', '2022-12-31', 'Tabora', 'Bachelor of Accounting Sciences in Internal Auditing . (98303 – AUI)'),
('2023/2024/t/0012', 'Benjamin James Adams', 'passports/4d403dd5f6242ce549d9ea6707988fab602e70865932a.jpg', 'applications/Admission_Form_RLu0urN.pdf', '2022-12-31', 'Tanga', 'Bachelor of Accounting Sciences in Financial Accounting . (98302 – FAC)'),
('2023/2024/t/00123', 'Corine Alise Alvarez', 'passports/doreen.jpg', 'applications/Admission_Form_3232JeM.pdf', '2022-12-31', 'Tanga', 'Bachelor of Accounting Sciences in Financial Accounting . (98302 – FAC)'),
('2023/2024/t/001231', 'Oscar Amaro-Renteria', 'passports/6f4c178c12d79514d2f32d9fb09d6a16.jpg', 'applications/Admission_Form_VPZQeSp.pdf', '2022-12-31', 'Dodoma', 'Advanced Diploma in Accounting Sciences Internal Auditing (98230 – AUI)'),
('2023/2024/t/0012310', 'Emily Ann Fretz', 'passports/Jumanne_Mwita.jpg', 'applications/Admission_Form_1Qz4PK6.pdf', '2022-12-31', 'Dodoma', 'Bachelor of Accounting Sciences in Financial Accounting . (98302 – FAC)'),
('2023/2024/t/00123411', 'Benjamin Eli Breckbill', 'passports/Joseph.jpg', 'applications/Admission_Form_HhbNiBn.pdf', '2022-12-31', 'Arusha', 'Advanced Diploma in Accounting Sciences Internal Auditing (98230 – AUI)'),
('2023/2024/t/0012366', 'Kathryn Ellen Friesen', 'passports/Uwizeye_Glorieuse_web_.jpg', 'applications/Admission_Form_yzYmqx6.pdf', '2022-12-31', 'Tanga', 'Bachelor of Accounting Sciences in Financial Accounting . (98302 – FAC)'),
('2023/2024/t/0012455', 'Nicole Lea Green', 'passports/Patrick-Cobbinah-796x1024.jpg', 'applications/Admission_Form_afyV4F1.pdf', '2022-12-31', 'Tanga', 'Diploma in Administrative Management (98216)'),
('2023/2024/t/00134', 'Jackson William Beck', 'passports/istockphoto-1196211150-170667a.jpg', 'applications/Admission_Form_PYnFTfo.pdf', '2022-12-31', 'Dodoma', 'Advanced Diploma in Accounting Sciences Internal Auditing (98230 – AUI)'),
('2023/2024/t/001444', 'Nicole Lea Green', 'passports/Tulari.jpg', 'applications/Admission_Form_IZ0nJCz.pdf', '2022-12-31', 'Tabora', 'Communication and Media');

-- --------------------------------------------------------

--
-- Table structure for table `app2_formmessage`
--

CREATE TABLE `app2_formmessage` (
  `id` bigint(20) NOT NULL,
  `message` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `application_closed` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `app2_formmessage`
--

INSERT INTO `app2_formmessage` (`id`, `message`, `created_at`, `application_closed`) VALUES
(1, 'online Application for 2022/2023 is now open – Apply Now,', '2023-01-28 21:24:49.187313', '2023-01-28');

-- --------------------------------------------------------

--
-- Table structure for table `app2_messagetoform`
--

CREATE TABLE `app2_messagetoform` (
  `id` bigint(20) NOT NULL,
  `message` varchar(200) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `closed_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `app2_messagetoform`
--

INSERT INTO `app2_messagetoform` (`id`, `message`, `created_at`, `closed_date`) VALUES
(1, 'Application window is opened, Apply now', '2023-01-29 13:51:06.935738', '2023-01-31'),
(2, 'Application window is opened for 2nd selection, Apply now', '2023-01-29 13:51:30.417171', '2023-03-29'),
(3, 'Application window is opened for Undergraduate applicants', '2023-01-29 13:59:39.749488', '2023-01-24');

-- --------------------------------------------------------

--
-- Table structure for table `app2_registration`
--

CREATE TABLE `app2_registration` (
  `id` bigint(20) NOT NULL,
  `firstname` varchar(200) NOT NULL,
  `lastname` varchar(200) NOT NULL,
  `resident` varchar(100) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `email` varchar(200) NOT NULL,
  `tutorial_session` varchar(100) NOT NULL,
  `accomodation` varchar(250) NOT NULL,
  `disability` longtext NOT NULL,
  `certificate` longtext NOT NULL,
  `marital` varchar(100) NOT NULL,
  `passport_size` varchar(100) NOT NULL,
  `certificates` varchar(100) NOT NULL,
  `date_of_birth` date NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `message` longtext NOT NULL,
  `program_id` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_group`
--

INSERT INTO `auth_group` (`id`, `name`) VALUES
(1, 'staffs'),
(2, 'view_only');

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_group_permissions`
--

INSERT INTO `auth_group_permissions` (`id`, `group_id`, `permission_id`) VALUES
(3, 1, 36),
(1, 1, 40),
(2, 1, 44),
(6, 2, 8),
(8, 2, 12),
(4, 2, 36),
(5, 2, 40),
(7, 2, 44),
(9, 2, 48);

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add announcements', 7, 'add_announcements'),
(26, 'Can change announcements', 7, 'change_announcements'),
(27, 'Can delete announcements', 7, 'delete_announcements'),
(28, 'Can view announcements', 7, 'view_announcements'),
(29, 'Can add department', 8, 'add_department'),
(30, 'Can change department', 8, 'change_department'),
(31, 'Can delete department', 8, 'delete_department'),
(32, 'Can view department', 8, 'view_department'),
(33, 'Can add programs', 9, 'add_programs'),
(34, 'Can change programs', 9, 'change_programs'),
(35, 'Can delete programs', 9, 'delete_programs'),
(36, 'Can view programs', 9, 'view_programs'),
(37, 'Can add student', 10, 'add_student'),
(38, 'Can change student', 10, 'change_student'),
(39, 'Can delete student', 10, 'delete_student'),
(40, 'Can view student', 10, 'view_student'),
(41, 'Can add herroes', 11, 'add_herroes'),
(42, 'Can change herroes', 11, 'change_herroes'),
(43, 'Can delete herroes', 11, 'delete_herroes'),
(44, 'Can view herroes', 11, 'view_herroes'),
(45, 'Can add course', 12, 'add_course'),
(46, 'Can change course', 12, 'change_course'),
(47, 'Can delete course', 12, 'delete_course'),
(48, 'Can view course', 12, 'view_course'),
(49, 'Can add registration', 13, 'add_registration'),
(50, 'Can change registration', 13, 'change_registration'),
(51, 'Can delete registration', 13, 'delete_registration'),
(52, 'Can view registration', 13, 'view_registration'),
(53, 'Can add form message', 14, 'add_formmessage'),
(54, 'Can change form message', 14, 'change_formmessage'),
(55, 'Can delete form message', 14, 'delete_formmessage'),
(56, 'Can view form message', 14, 'view_formmessage'),
(57, 'Can add message to form', 15, 'add_messagetoform'),
(58, 'Can change message to form', 15, 'change_messagetoform'),
(59, 'Can delete message to form', 15, 'delete_messagetoform'),
(60, 'Can view message to form', 15, 'view_messagetoform');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$390000$k4N3cbp1QPZPaUocSJWRTe$xiR0D3man/dmYeZJ5jn+unPPtUfhQ7ZbiNTxbsgedgA=', '2023-01-26 18:33:05.343301', 1, 'samir', '', '', '', 1, 1, '2022-12-31 11:31:00.943376'),
(2, 'pbkdf2_sha256$390000$MsI1BH8QvCKCLgptEHdxRu$maAJSz3N6axRr7IZmVGzx6mAPqVqR2bRkcbOVtIXHm8=', '2022-12-31 12:25:08.973532', 0, 'maria', 'maria maria', 'alice', 'anisha@gmail.com', 1, 1, '2022-12-31 12:24:04.000000'),
(3, 'pbkdf2_sha256$390000$9E3Wkvt5hI4Iyer5oZPnqa$y/v6Gfi4ZwMYQ+B66LF49vDdSlGbuL+brTsxx28wEOQ=', '2022-12-31 14:55:50.729191', 0, 'kim', 'kim', 'kim', 'kim@gmail.com', 1, 1, '2022-12-31 14:48:16.000000'),
(4, 'pbkdf2_sha256$390000$vacnRYo0tp21zMnu9eqAZS$BTvMLEfqwjcjxgtbot097ET2b/DtF6hOsiLhDK6IB58=', '2022-12-31 14:54:24.571850', 0, 'user1', '', '', '', 1, 1, '2022-12-31 14:53:48.000000'),
(5, 'pbkdf2_sha256$390000$4CgmxbSbohHd7FcE8iBb8d$NKJraLTubuqf/OVG9eREq5BVx5HVUTOOsmcDzlsPX6s=', '2022-12-31 15:38:58.666387', 0, 'alice', 'zxzx', 'zxzxzx', '', 1, 1, '2022-12-31 15:37:59.000000');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_user_groups`
--

INSERT INTO `auth_user_groups` (`id`, `user_id`, `group_id`) VALUES
(1, 2, 1),
(3, 3, 2),
(2, 4, 2);

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_user_user_permissions`
--

INSERT INTO `auth_user_user_permissions` (`id`, `user_id`, `permission_id`) VALUES
(1, 2, 35),
(2, 2, 44),
(6, 3, 25),
(7, 3, 29),
(3, 3, 33),
(4, 3, 37),
(5, 3, 45),
(12, 5, 9),
(13, 5, 11),
(15, 5, 29),
(8, 5, 34),
(9, 5, 36),
(10, 5, 38),
(11, 5, 39),
(14, 5, 47);

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2022-12-31 11:50:59.167779', 'Human Resource', 'Human Resource', 1, '[{\"added\": {}}]', 8, 1),
(2, '2022-12-31 11:51:41.081787', 'Academic Affairs', 'Academic Affairs', 1, '[{\"added\": {}}]', 8, 1),
(3, '2022-12-31 11:51:46.668282', 'Academic Success Center', 'Academic Success Center', 1, '[{\"added\": {}}]', 8, 1),
(4, '2022-12-31 11:51:54.998182', 'Accountability and Assessment', 'Accountability and Assessment', 1, '[{\"added\": {}}]', 8, 1),
(5, '2022-12-31 11:52:01.396403', 'Accounting, Economics & Finance', 'Accounting, Economics & Finance', 1, '[{\"added\": {}}]', 8, 1),
(6, '2022-12-31 11:52:11.787398', 'Administration and Finance', 'Administration and Finance', 1, '[{\"added\": {}}]', 8, 1),
(7, '2022-12-31 11:52:18.426325', 'Admissions Undergraduate', 'Admissions Undergraduate', 1, '[{\"added\": {}}]', 8, 1),
(8, '2022-12-31 11:52:30.999083', 'Education, Health and Human Svcs (School of)', 'Education, Health and Human Svcs (School of)', 1, '[{\"added\": {}}]', 8, 1),
(9, '2022-12-31 11:52:38.588557', 'Environmental Health and Safety', 'Environmental Health and Safety', 1, '[{\"added\": {}}]', 8, 1),
(10, '2022-12-31 11:52:45.817956', 'EOC Business and Info Technology', 'EOC Business and Info Technology', 1, '[{\"added\": {}}]', 8, 1),
(11, '2022-12-31 11:52:53.613557', 'EOC Community Relations', 'EOC Community Relations', 1, '[{\"added\": {}}]', 8, 1),
(12, '2022-12-31 11:54:25.004227', 'Community Development', 'Community Development', 1, '[{\"added\": {}}]', 9, 1),
(13, '2022-12-31 11:55:26.669595', 'Dan F. Smith Department of Chemical and Biomolecular Engineering', 'Dan F. Smith Department of Chemical and Biomolecular Engineering', 1, '[{\"added\": {}}]', 9, 1),
(14, '2022-12-31 11:55:44.009807', 'Department of Civil & Environmental Engineering', 'Department of Civil & Environmental Engineering', 1, '[{\"added\": {}}]', 9, 1),
(15, '2022-12-31 11:56:07.205184', 'Phillip M. Drayer Department of Electrical Engineering', 'Phillip M. Drayer Department of Electrical Engineering', 1, '[{\"added\": {}}]', 9, 1),
(16, '2022-12-31 11:56:27.685198', 'Department of Industrial and Systems Engineering', 'Department of Industrial and Systems Engineering', 1, '[{\"added\": {}}]', 9, 1),
(17, '2022-12-31 11:56:42.204108', 'Department of Mechanical Engineering', 'Department of Mechanical Engineering', 1, '[{\"added\": {}}]', 9, 1),
(18, '2022-12-31 11:56:57.830387', 'Communication and Media', 'Communication and Media', 1, '[{\"added\": {}}]', 9, 1),
(19, '2022-12-31 11:57:12.007938', 'Deaf Studies and Deaf Education', 'Deaf Studies and Deaf Education', 1, '[{\"added\": {}}]', 9, 1),
(20, '2022-12-31 11:57:44.433266', '1', 'Bachelor of Arts in American Sign Language', 1, '[{\"added\": {}}]', 12, 1),
(21, '2022-12-31 11:58:07.023329', '2', 'Master of Science in Deaf Studies Deaf Education', 1, '[{\"added\": {}}]', 12, 1),
(22, '2022-12-31 11:58:12.248032', '3', 'Master of Arts in Deaf Studies', 1, '[{\"added\": {}}]', 12, 1),
(23, '2022-12-31 11:58:22.878346', '4', 'Doctor of Education in Deaf Studies and Deaf Education', 1, '[{\"added\": {}}]', 12, 1),
(24, '2022-12-31 11:59:35.403371', '5', 'Higher Certificate in Accounting Sciences (98201)', 1, '[{\"added\": {}}]', 12, 1),
(25, '2022-12-31 11:59:47.087173', '6', 'Higher Certificate in Adult Basic Education and Training (98615)', 1, '[{\"added\": {}}]', 12, 1),
(26, '2022-12-31 11:59:54.311566', '7', 'Higher Certificate in Animal Welfare (90098)', 1, '[{\"added\": {}}]', 12, 1),
(27, '2022-12-31 12:00:04.094931', '8', 'Higher Certificate in Archives and Records Management (98577)', 1, '[{\"added\": {}}]', 12, 1),
(28, '2022-12-31 12:00:36.575007', 'Diploma in Accounting Sciences (98200)', 'Diploma in Accounting Sciences (98200)', 1, '[{\"added\": {}}]', 9, 1),
(29, '2022-12-31 12:00:49.527359', 'Diploma in Administrative Management (98216)', 'Diploma in Administrative Management (98216)', 1, '[{\"added\": {}}]', 9, 1),
(30, '2022-12-31 12:01:01.666409', 'Diploma in Agricultural Management (90097)', 'Diploma in Agricultural Management (90097)', 1, '[{\"added\": {}}]', 9, 1),
(31, '2022-12-31 12:01:18.480549', 'Advanced Diploma in Accounting Sciences Financial Accounting (98230 – FAC)', 'Advanced Diploma in Accounting Sciences Financial Accounting (98230 – FAC)', 1, '[{\"added\": {}}]', 9, 1),
(32, '2022-12-31 12:01:34.427899', 'Advanced Diploma in Accounting Sciences Internal Auditing (98230 – AUI)', 'Advanced Diploma in Accounting Sciences Internal Auditing (98230 – AUI)', 1, '[{\"added\": {}}]', 9, 1),
(33, '2022-12-31 12:01:48.251791', 'Bachelor of Accounting Sciences in Financial Accounting . (98302 – FAC)', 'Bachelor of Accounting Sciences in Financial Accounting . (98302 – FAC)', 1, '[{\"added\": {}}]', 9, 1),
(34, '2022-12-31 12:02:00.664084', 'Bachelor of Accounting Sciences in Internal Auditing . (98303 – AUI)', 'Bachelor of Accounting Sciences in Internal Auditing . (98303 – AUI)', 1, '[{\"added\": {}}]', 9, 1),
(35, '2022-12-31 12:02:15.618069', '8', 'Higher Certificate in Archives and Records Management (98577)', 3, '', 12, 1),
(36, '2022-12-31 12:02:15.680034', '7', 'Higher Certificate in Animal Welfare (90098)', 3, '', 12, 1),
(37, '2022-12-31 12:02:15.712014', '6', 'Higher Certificate in Adult Basic Education and Training (98615)', 3, '', 12, 1),
(38, '2022-12-31 12:02:15.786972', '5', 'Higher Certificate in Accounting Sciences (98201)', 3, '', 12, 1),
(39, '2022-12-31 12:02:15.811956', '4', 'Doctor of Education in Deaf Studies and Deaf Education', 3, '', 12, 1),
(40, '2022-12-31 12:02:15.842940', '3', 'Master of Arts in Deaf Studies', 3, '', 12, 1),
(41, '2022-12-31 12:02:15.870926', '2', 'Master of Science in Deaf Studies Deaf Education', 3, '', 12, 1),
(42, '2022-12-31 12:02:15.893911', '1', 'Bachelor of Arts in American Sign Language', 3, '', 12, 1),
(43, '2022-12-31 12:04:53.837367', '9', 'AUE1501 - Introduction to Auditing', 1, '[{\"added\": {}}]', 12, 1),
(44, '2022-12-31 12:05:00.820118', '10', 'BNU1501 - Basic Numeracy', 1, '[{\"added\": {}}]', 12, 1),
(45, '2022-12-31 12:05:09.905713', '11', 'CAS1501 - Perspectives on Accountancy', 1, '[{\"added\": {}}]', 12, 1),
(46, '2022-12-31 12:05:20.363809', '12', 'CLA1503 - Commercial Law IC', 1, '[{\"added\": {}}]', 12, 1),
(47, '2022-12-31 12:05:28.586054', '13', 'ENN1504 - Practising Workplace English', 1, '[{\"added\": {}}]', 12, 1),
(48, '2022-12-31 12:05:39.684567', '14', 'FAC1501 - Introductory Financial Accounting', 1, '[{\"added\": {}}]', 12, 1),
(49, '2022-12-31 12:05:49.454425', '15', 'FAC1502 - Financial Accounting Principles, Concepts and Procedures', 1, '[{\"added\": {}}]', 12, 1),
(50, '2022-12-31 12:05:57.472452', '16', 'MAC1501 - Introduction to Management Accounting', 1, '[{\"added\": {}}]', 12, 1),
(51, '2022-12-31 12:06:24.046622', '17', 'MNB1501 - Business Management IA', 1, '[{\"added\": {}}]', 12, 1),
(52, '2022-12-31 12:07:22.812517', '2023/2024/t/001', '2023/2024/t/001', 1, '[{\"added\": {}}]', 10, 1),
(53, '2022-12-31 12:08:39.858863', '2023/2024/t/0012', '2023/2024/t/0012', 1, '[{\"added\": {}}]', 10, 1),
(54, '2022-12-31 12:09:08.065403', '2023/2024/t/00123', '2023/2024/t/00123', 1, '[{\"added\": {}}]', 10, 1),
(55, '2022-12-31 12:09:42.578097', '2023/2024/t/001231', '2023/2024/t/001231', 1, '[{\"added\": {}}]', 10, 1),
(56, '2022-12-31 12:10:30.613994', '2023/2024/t/00134', '2023/2024/t/00134', 1, '[{\"added\": {}}]', 10, 1),
(57, '2022-12-31 12:10:58.939186', '2023/2024/t/0012312', '2023/2024/t/0012312', 1, '[{\"added\": {}}]', 10, 1),
(58, '2022-12-31 12:12:15.007964', '2023/2024/t/00123411', '2023/2024/t/00123411', 1, '[{\"added\": {}}]', 10, 1),
(59, '2022-12-31 12:12:34.687407', '2023/2024/t/0012310', '2023/2024/t/0012310', 1, '[{\"added\": {}}]', 10, 1),
(60, '2022-12-31 12:13:00.070360', '2023/2024/t/0012366', '2023/2024/t/0012366', 1, '[{\"added\": {}}]', 10, 1),
(61, '2022-12-31 12:13:39.017998', '2023/2024/t/0012455', '2023/2024/t/0012455', 1, '[{\"added\": {}}]', 10, 1),
(62, '2022-12-31 12:14:22.048614', '1', 'Nicole Lea Green', 1, '[{\"added\": {}}]', 11, 1),
(63, '2022-12-31 12:14:52.721729', '2', 'Benjamin James Adams', 1, '[{\"added\": {}}]', 11, 1),
(64, '2022-12-31 12:15:25.353703', '3', 'Philip John Bontrager', 1, '[{\"added\": {}}]', 11, 1),
(65, '2022-12-31 12:15:47.608020', '4', 'Bianca Magali Brambila', 1, '[{\"added\": {}}]', 11, 1),
(66, '2022-12-31 12:16:16.554409', '5', 'Elizabeth L. Core', 1, '[{\"added\": {}}]', 11, 1),
(67, '2022-12-31 12:16:54.035974', '6', 'Hayden Joel Goerzen', 1, '[{\"added\": {}}]', 11, 1),
(68, '2022-12-31 12:17:14.504837', '7', 'Erica Rose Grasse', 1, '[{\"added\": {}}]', 11, 1),
(69, '2022-12-31 12:17:47.415289', '8', 'Joseph Roman Gunden', 1, '[{\"added\": {}}]', 11, 1),
(70, '2022-12-31 12:18:18.612248', '9', 'Mia Carlene Engle', 1, '[{\"added\": {}}]', 11, 1),
(71, '2022-12-31 12:19:15.761837', '1', 'SECOND YEAR', 1, '[{\"added\": {}}]', 7, 1),
(72, '2022-12-31 12:19:30.859965', '2', 'Regulations for Undergraduate   Programmes_Final', 1, '[{\"added\": {}}]', 7, 1),
(73, '2022-12-31 12:19:47.850609', '3', 'CERTIFICATE OF APPRECIATION 2', 1, '[{\"added\": {}}]', 7, 1),
(74, '2022-12-31 12:20:09.938017', '4', 'TANGAZO ACCOMODATAION', 1, '[{\"added\": {}}]', 7, 1),
(75, '2022-12-31 12:20:35.726688', '5', 'undergraduate_curriculum_guidebook_2021_2022', 1, '[{\"added\": {}}]', 7, 1),
(76, '2022-12-31 12:20:48.704627', '6', 'Teaching Matrix', 1, '[{\"added\": {}}]', 7, 1),
(77, '2022-12-31 12:21:05.983061', '7', 'FYP Supervission form', 1, '[{\"added\": {}}]', 7, 1),
(78, '2022-12-31 12:21:27.744773', '8', 'Announcement to All Students _ Registration for Semester Two 2021-2022 Academic Year', 1, '[{\"added\": {}}]', 7, 1),
(79, '2022-12-31 12:22:33.510327', '9', 'ALMANAC_notice_21', 1, '[{\"added\": {}}]', 7, 1),
(80, '2022-12-31 12:23:29.794198', '1', 'staffs', 1, '[{\"added\": {}}]', 3, 1),
(81, '2022-12-31 12:24:05.214161', '2', 'maria', 1, '[{\"added\": {}}]', 4, 1),
(82, '2022-12-31 12:24:49.495463', '2', 'maria', 2, '[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\", \"Staff status\", \"Groups\", \"User permissions\"]}}]', 4, 1),
(83, '2022-12-31 12:47:38.518156', '2023/2024/t/00134', '2023/2024/t/00134', 2, '[]', 10, 1),
(84, '2022-12-31 13:00:45.311238', '17', 'MNB1501 - Business Management IA', 2, '[{\"changed\": {\"fields\": [\"Program\"]}}]', 12, 1),
(85, '2022-12-31 13:01:50.794180', '9', 'ALMANAC_notice', 2, '[{\"changed\": {\"fields\": [\"Title\"]}}]', 7, 1),
(86, '2022-12-31 13:33:12.103155', '10', 'samir said', 1, '[{\"added\": {}}]', 11, 1),
(87, '2022-12-31 14:08:41.237685', '10', 'samir said', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 11, 1),
(88, '2022-12-31 14:48:16.964856', '3', 'kim', 1, '[{\"added\": {}}]', 4, 1),
(89, '2022-12-31 14:49:25.529942', '3', 'kim', 2, '[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\", \"Staff status\", \"User permissions\"]}}]', 4, 1),
(90, '2022-12-31 14:50:41.204682', '10', 'mkutano today', 1, '[{\"added\": {}}]', 7, 3),
(91, '2022-12-31 14:51:58.618081', '2023/2024/t/001444', '2023/2024/t/001444', 1, '[{\"added\": {}}]', 10, 3),
(92, '2022-12-31 14:53:24.767382', '2', 'view_only', 1, '[{\"added\": {}}]', 3, 1),
(93, '2022-12-31 14:53:49.301039', '4', 'user1', 1, '[{\"added\": {}}]', 4, 1),
(94, '2022-12-31 14:54:07.390499', '4', 'user1', 2, '[{\"changed\": {\"fields\": [\"Staff status\", \"Groups\"]}}]', 4, 1),
(95, '2022-12-31 14:55:31.055633', '3', 'kim', 2, '[{\"changed\": {\"fields\": [\"Groups\"]}}]', 4, 1),
(96, '2022-12-31 14:56:43.240734', '11', 'Akiba', 1, '[{\"added\": {}}]', 11, 1),
(97, '2022-12-31 15:24:05.787967', '2023/2024/t/001444', '2023/2024/t/001444', 2, '[]', 10, 1),
(98, '2022-12-31 15:37:12.790981', '2023/2024/t/001444', '2023/2024/t/001444', 2, '[{\"changed\": {\"fields\": [\"Program\"]}}]', 10, 1),
(99, '2022-12-31 15:38:00.277015', '5', 'alice', 1, '[{\"added\": {}}]', 4, 1),
(100, '2022-12-31 15:38:28.601592', '5', 'alice', 2, '[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"User permissions\"]}}]', 4, 1),
(101, '2022-12-31 15:38:37.997581', '5', 'alice', 2, '[{\"changed\": {\"fields\": [\"Staff status\"]}}]', 4, 1),
(102, '2023-01-18 16:37:09.109704', '11', 'Akiba', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 11, 1),
(103, '2023-01-18 17:23:43.526971', 't/1233', 't/1233', 1, '[{\"added\": {}}]', 10, 1),
(104, '2023-01-26 19:18:26.306878', '11', 'Akiba', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 11, 1),
(105, '2023-01-28 21:24:49.206301', '1', 'FormMessage object (1)', 1, '[{\"added\": {}}]', 14, 1),
(106, '2023-01-29 10:18:07.890800', '11', 'Akiba', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 11, 1),
(107, '2023-01-29 10:18:41.129533', '11', 'Akiba', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 11, 1),
(108, '2023-01-29 13:51:06.982719', '1', 'MessageToForm object (1)', 1, '[{\"added\": {}}]', 15, 1),
(109, '2023-01-29 13:51:30.437159', '2', 'MessageToForm object (2)', 1, '[{\"added\": {}}]', 15, 1),
(110, '2023-01-29 13:59:39.785454', '3', 'MessageToForm object (3)', 1, '[{\"added\": {}}]', 15, 1),
(111, '2023-01-29 15:15:53.007308', 'shamirisaidiselemani@gmail.com', 'Registration object (shamirisaidiselemani@gmail.com)', 3, '', 13, 1),
(112, '2023-01-29 15:15:53.067282', 'shamirisaidiselemani@gmail.com', 'Registration object (shamirisaidiselemani@gmail.com)', 3, '', 13, 1),
(113, '2023-01-29 15:15:53.091261', 'shamirisaidiselemani@gmail.com', 'Registration object (shamirisaidiselemani@gmail.com)', 3, '', 13, 1),
(114, '2023-01-29 15:15:53.148228', 'shamirisaidiselemani@gmail.com', 'Registration object (shamirisaidiselemani@gmail.com)', 3, '', 13, 1),
(115, '2023-01-29 15:15:53.202196', 'shamirisaidiselemani@gmail.com', 'Registration object (shamirisaidiselemani@gmail.com)', 3, '', 13, 1),
(116, '2023-01-29 15:15:53.239174', 'shamirisaidiselemani@gmail.com', 'Registration object (shamirisaidiselemani@gmail.com)', 3, '', 13, 1),
(117, '2023-01-29 15:15:53.267159', 'shamirisaidiselemani@gmail.com', 'Registration object (shamirisaidiselemani@gmail.com)', 3, '', 13, 1),
(118, '2023-01-29 15:15:53.348114', 'shamirisaidiselemani@gmail.com', 'Registration object (shamirisaidiselemani@gmail.com)', 3, '', 13, 1),
(119, '2023-01-29 15:16:04.240780', 'arrrlice@gmail.com', 'Registration object (arrrlice@gmail.com)', 3, '', 13, 1),
(120, '2023-01-29 15:16:04.266763', 'arrfrlice@gmail.com', 'Registration object (arrfrlice@gmail.com)', 3, '', 13, 1),
(121, '2023-01-29 15:16:04.290750', 'arlice@gmail.com', 'Registration object (arlice@gmail.com)', 3, '', 13, 1),
(122, '2023-01-29 15:16:04.317740', 'alice@gmail.com', 'Registration object (alice@gmail.com)', 3, '', 13, 1),
(123, '2023-01-29 15:16:04.350715', 'alice2@gmail.com', 'Registration object (alice2@gmail.com)', 3, '', 13, 1),
(124, '2023-01-29 15:19:54.011034', 'alice2@gmail.com', 'Registration object (alice2@gmail.com)', 3, '', 13, 1),
(125, '2023-01-29 15:22:04.346521', 'alice2@gmail.com', 'Registration object (alice2@gmail.com)', 3, '', 13, 1),
(126, '2023-01-29 15:25:15.251888', 'alice2@gmail.com', 'Registration object (alice2@gmail.com)', 3, '', 13, 1),
(127, '2023-01-29 15:28:40.146913', 'alice@gmail.com', 'Registration object (alice@gmail.com)', 3, '', 13, 1),
(128, '2023-01-29 15:29:37.391900', '2023/2024/t/0012312', '2023/2024/t/0012312', 3, '', 10, 1),
(129, '2023-01-29 15:36:59.620962', 't/1233', 't/1233', 3, '', 10, 1);

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(7, 'APP1', 'announcements'),
(12, 'APP1', 'course'),
(8, 'APP1', 'department'),
(11, 'APP1', 'herroes'),
(9, 'APP1', 'programs'),
(10, 'APP1', 'student'),
(14, 'APP2', 'formmessage'),
(15, 'APP2', 'messagetoform'),
(13, 'APP2', 'registration'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'APP1', '0001_initial', '2023-01-18 16:18:13.213062'),
(2, 'APP1', '0002_alter_programs_program_fee_currency', '2023-01-18 16:18:13.246258'),
(3, 'contenttypes', '0001_initial', '2023-01-18 16:18:13.869665'),
(4, 'auth', '0001_initial', '2023-01-18 16:18:22.922015'),
(5, 'admin', '0001_initial', '2023-01-18 16:18:24.702460'),
(6, 'admin', '0002_logentry_remove_auto_add', '2023-01-18 16:18:24.742058'),
(7, 'admin', '0003_logentry_add_action_flag_choices', '2023-01-18 16:18:24.776229'),
(8, 'contenttypes', '0002_remove_content_type_name', '2023-01-18 16:18:25.407919'),
(9, 'auth', '0002_alter_permission_name_max_length', '2023-01-18 16:18:26.854926'),
(10, 'auth', '0003_alter_user_email_max_length', '2023-01-18 16:18:26.972443'),
(11, 'auth', '0004_alter_user_username_opts', '2023-01-18 16:18:27.019308'),
(12, 'auth', '0005_alter_user_last_login_null', '2023-01-18 16:18:27.603374'),
(13, 'auth', '0006_require_contenttypes_0002', '2023-01-18 16:18:27.656385'),
(14, 'auth', '0007_alter_validators_add_error_messages', '2023-01-18 16:18:27.722303'),
(15, 'auth', '0008_alter_user_username_max_length', '2023-01-18 16:18:27.927336'),
(16, 'auth', '0009_alter_user_last_name_max_length', '2023-01-18 16:18:28.071831'),
(17, 'auth', '0010_alter_group_name_max_length', '2023-01-18 16:18:28.201687'),
(18, 'auth', '0011_update_proxy_permissions', '2023-01-18 16:18:28.251480'),
(19, 'auth', '0012_alter_user_first_name_max_length', '2023-01-18 16:18:29.035478'),
(20, 'sessions', '0001_initial', '2023-01-18 16:18:29.775890'),
(21, 'APP2', '0001_initial', '2023-01-28 14:22:50.600668'),
(22, 'APP2', '0002_alter_registration_resident', '2023-01-28 15:17:42.201194'),
(23, 'APP2', '0003_alter_registration_accomodation_and_more', '2023-01-28 19:47:23.194151'),
(24, 'APP2', '0004_alter_registration_phone', '2023-01-28 20:20:15.772344'),
(25, 'APP2', '0005_registration_program', '2023-01-28 20:39:03.963441'),
(26, 'APP2', '0006_formmessage', '2023-01-28 21:18:40.224088'),
(27, 'APP2', '0002_messagetoform', '2023-01-29 13:48:20.160774');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('9t67aaptpzqhz4kucel0felf83s5htd2', '.eJxVjDEOwjAMRe-SGUVxS6yWkZ0zRLbjkAJKpKadKu4OlTrA-t97fzOB1iWHtekcpmguBszpd2OSp5YdxAeVe7VSyzJPbHfFHrTZW436uh7u30Gmlr-1RFIAB6qOk5IkSNgNwHT2PY7onHdAooN4EBq1Q-TeeyViTBoJzfsDCdU4_g:1pIBAn:_ftg1BG23ZLfTmmfNBLLvmKm-hQSPmJ1V9c8pHsANY8', '2023-02-01 16:20:25.631165'),
('mb4owyr6kb04jaf28cajnvzjnywph2hs', '.eJxVjDEOwjAMRe-SGUVxS6yWkZ0zRLbjkAJKpKadKu4OlTrA-t97fzOB1iWHtekcpmguBszpd2OSp5YdxAeVe7VSyzJPbHfFHrTZW436uh7u30Gmlr-1RFIAB6qOk5IkSNgNwHT2PY7onHdAooN4EBq1Q-TeeyViTBoJzfsDCdU4_g:1pBfvB:_PFpQ6Isw-rGwzwWI1HvuDo6UuLFdIEADR5O55nKyLI', '2023-01-14 17:45:25.589005'),
('wj6foggtaqk4fg7j26t8kczqxvs71vqq', '.eJxVjDEOwjAMRe-SGUVxS6yWkZ0zRLbjkAJKpKadKu4OlTrA-t97fzOB1iWHtekcpmguBszpd2OSp5YdxAeVe7VSyzJPbHfFHrTZW436uh7u30Gmlr-1RFIAB6qOk5IkSNgNwHT2PY7onHdAooN4EBq1Q-TeeyViTBoJzfsDCdU4_g:1pL73Z:ypw7LITiU1JfQ3d22s9FHWl6MSbNTKMLrSEdkxRZ6pE', '2023-02-09 18:33:05.369287');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `app1_announcements`
--
ALTER TABLE `app1_announcements`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `app1_course`
--
ALTER TABLE `app1_course`
  ADD PRIMARY KEY (`id`),
  ADD KEY `APP1_course_program_id_92076c7f_fk_APP1_programs_program_name` (`program_id`);

--
-- Indexes for table `app1_department`
--
ALTER TABLE `app1_department`
  ADD PRIMARY KEY (`department_name`);

--
-- Indexes for table `app1_herroes`
--
ALTER TABLE `app1_herroes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `APP1_herroes_department_id_4769d1fb_fk_APP1_depa` (`department_id`),
  ADD KEY `APP1_herroes_program_id_d43fb888_fk_APP1_programs_program_name` (`program_id`);

--
-- Indexes for table `app1_programs`
--
ALTER TABLE `app1_programs`
  ADD PRIMARY KEY (`program_name`),
  ADD KEY `APP1_programs_department_id_d3194a38_fk_APP1_depa` (`department_id`);

--
-- Indexes for table `app1_student`
--
ALTER TABLE `app1_student`
  ADD PRIMARY KEY (`regno`),
  ADD KEY `APP1_student_program_id_9f2b5d3c_fk_APP1_programs_program_name` (`program_id`);

--
-- Indexes for table `app2_formmessage`
--
ALTER TABLE `app2_formmessage`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `app2_messagetoform`
--
ALTER TABLE `app2_messagetoform`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `app2_registration`
--
ALTER TABLE `app2_registration`
  ADD PRIMARY KEY (`id`),
  ADD KEY `APP2_registration_program_id_68f00573_fk_APP1_prog` (`program_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `app1_announcements`
--
ALTER TABLE `app1_announcements`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `app1_course`
--
ALTER TABLE `app1_course`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `app1_herroes`
--
ALTER TABLE `app1_herroes`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `app2_formmessage`
--
ALTER TABLE `app2_formmessage`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `app2_messagetoform`
--
ALTER TABLE `app2_messagetoform`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `app2_registration`
--
ALTER TABLE `app2_registration`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=57;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=130;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `app1_course`
--
ALTER TABLE `app1_course`
  ADD CONSTRAINT `APP1_course_program_id_92076c7f_fk_APP1_programs_program_name` FOREIGN KEY (`program_id`) REFERENCES `app1_programs` (`program_name`);

--
-- Constraints for table `app1_herroes`
--
ALTER TABLE `app1_herroes`
  ADD CONSTRAINT `APP1_herroes_department_id_4769d1fb_fk_APP1_depa` FOREIGN KEY (`department_id`) REFERENCES `app1_department` (`department_name`),
  ADD CONSTRAINT `APP1_herroes_program_id_d43fb888_fk_APP1_programs_program_name` FOREIGN KEY (`program_id`) REFERENCES `app1_programs` (`program_name`);

--
-- Constraints for table `app1_programs`
--
ALTER TABLE `app1_programs`
  ADD CONSTRAINT `APP1_programs_department_id_d3194a38_fk_APP1_depa` FOREIGN KEY (`department_id`) REFERENCES `app1_department` (`department_name`);

--
-- Constraints for table `app1_student`
--
ALTER TABLE `app1_student`
  ADD CONSTRAINT `APP1_student_program_id_9f2b5d3c_fk_APP1_programs_program_name` FOREIGN KEY (`program_id`) REFERENCES `app1_programs` (`program_name`);

--
-- Constraints for table `app2_registration`
--
ALTER TABLE `app2_registration`
  ADD CONSTRAINT `APP2_registration_program_id_68f00573_fk_APP1_prog` FOREIGN KEY (`program_id`) REFERENCES `app1_programs` (`program_name`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
