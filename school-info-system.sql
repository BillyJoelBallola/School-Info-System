-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 04, 2023 at 11:26 AM
-- Server version: 10.4.25-MariaDB
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `school-info-system`
--

-- --------------------------------------------------------

--
-- Table structure for table `announcement`
--

CREATE TABLE `announcement` (
  `id` int(100) NOT NULL,
  `title` varchar(100) NOT NULL,
  `audience` varchar(100) NOT NULL,
  `purpose` varchar(1000) NOT NULL,
  `place` varchar(100) NOT NULL,
  `date` date NOT NULL,
  `status` varchar(10) NOT NULL,
  `uid` int(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `announcement`
--

INSERT INTO `announcement` (`id`, `title`, `audience`, `purpose`, `place`, `date`, `status`, `uid`) VALUES
(48, 'Xmas Party Meeting', 'All grade', 'Xmas Party Meeting', 'Covered Court', '2022-12-22', 'Posted', 3),
(49, 'Examination', 'grade-six', 'Examination after christmas vacation', 'Google Meet', '2022-12-22', 'Posted', 2),
(50, 'Sample', 'grade-one', 'Sample', 'Sample', '2022-12-01', 'Archive', 2),
(51, 'Sample', 'grade-one', 'Sample', 'Sample', '2022-12-23', 'Posted', 20),
(52, 'Sample', 'teachers', 'sample', 'Sample', '2022-12-24', 'Archive', 2),
(53, 'Sample announcement', 'parents', 'Sample announcement', 'sa inyo', '2022-12-24', 'Archive', 2),
(54, 'Parent Meeting', 'grade-six', 'Binully si kano', 'Classroom', '2023-01-18', 'Archive', 2),
(55, 'Parent meeting', 'grade-four', 'Christmas Party of students', 'Classroom', '2023-01-13', 'Archive', 2),
(56, 'meeting', 'All grade', 'meeting', 'court', '2023-01-04', 'Archive', 3);

-- --------------------------------------------------------

--
-- Table structure for table `article`
--

CREATE TABLE `article` (
  `id` int(255) NOT NULL,
  `title` varchar(100) NOT NULL,
  `content` varchar(2000) NOT NULL,
  `img` varchar(255) NOT NULL,
  `date` date NOT NULL,
  `time` time NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `article`
--

INSERT INTO `article` (`id`, `title`, `content`, `img`, `date`, `time`) VALUES
(36, 'Christmas Party 2022', 'All teachers know behaviors are always crazy during classroom parties!  It is very helpful the day of the party to reteach your behavior expectations using Green and Red Choices.  During circle on the party day, read a holiday book like Llama Llama Holiday Drama or It’s Christmas, David!. As you read, talk about the choices the character is making, and if they are a green or a red choice. Talk about how that choice might make the character feel and how others would feel.  Most importantly, discuss how the character might turn a red choice into a green choice.  The holidays are HARD for kids because their home and school routines are different.  It’s important to reteach behavior expectations using visuals and to give students a chance to change their choices for the better.', '0.285208368094375christmas_party.jpg', '2022-12-16', '15:39:03'),
(46, 'Oplan Balik Eskuwela 2023', 'Magdalena, Laguna, August 16, 2022— The Department of Education (DepEd) and 17 partner agencies convened on Monday to launch the Oplan Balik Eskwela 2022 (OBE) and present updates, assistance and preparations for the upcoming opening of School Year 2022-2023 on August 22.\r\n\r\n“Thank you to our partners from other national government agencies and instrumentalities of the government, thank you for your support of the efforts of the Department of Education in opening in-person classes nationwide in August 2022,” Vice President and DepEd Secretary Sara Z. Duterte greeted.\r\n\r\nWith the theme: Kapit-bisig para sa ligtas na balik-aral, OBE 2022 is spearheaded by DepEd with the support from DOE, DILG, DOH, DND, DPWH, DSWD, DTI, DOTr, DICT, MERALCO, MWSS, MMDA, PAGASA, PNP, NDRRMC, NTC, and OPS, which compose the OBE Inter-Agency Convergence.', '0.058324110002650364Face_to_face.jpg', '2023-02-21', '14:19:01'),
(47, 'Intramurals 2021', 'Intramural sports are available for all fourth and fifth graders at all our elementary schools.  We offer these as after school activities to enrich the students\' athletic experience.\r\n\r\n \r\n\r\nIntramural activities in our district provide opportunities for competition and recreational physical activities at the elementary level. Intramural activities are conducted within our school district and do not involve events with other school districts. No physical is needed and there is no cost unless otherwise noted.  \r\n\r\n \r\n\r\nIntramural activities usually run from 3:00 pm - 4:30 pm. Students must be picked up by 4:30 pm, or they may walk or ride a bike home with written permission. Participation is optional for each season. Behavior expectations are high, and teamwork and sportsmanship are emphasized.', '0.15250619444184443intrams_orig.jpg', '2022-05-18', '14:30:48');

-- --------------------------------------------------------

--
-- Table structure for table `event`
--

CREATE TABLE `event` (
  `id` int(255) NOT NULL,
  `title` varchar(50) NOT NULL,
  `content` varchar(2000) NOT NULL,
  `date` date NOT NULL,
  `time` time NOT NULL DEFAULT current_timestamp(),
  `img` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `event`
--

INSERT INTO `event` (`id`, `title`, `content`, `date`, `time`, `img`) VALUES
(10, 'Nutrition Day', 'Nutrition Month is a health awareness campaign where the importance of making food choices as well as developing and maintaining good eating habits was given strong emphasis through the activities, like drawing contests, collage-making contests, poster making contests, coloring contests, Mommy Chefs, Little Chefs, “Baon mo, ubusin mo” program, Pinggang Pinoy, and poetry & singing contests.', '2022-07-20', '15:27:08', '0.1480866527188105nutrition.jpg'),
(11, 'Buwan ng Wika', 'Buwan ng Wikang Pambansa (Tagalog for \'National Language Month\'), simply known as Buwan ng Wika (\'Language Month\'), is a month-long annual observance in the Philippines held every August to promote the national language, Filipino.', '2022-08-16', '15:34:22', '0.2944235629465828buwan_ng_wika.png'),
(12, 'Teacher\'s Day', 'This is a special day to honor teachers and their role in molding the children, youth and adults through the life-long learning process despite of pandemic.  This year theme is “Gurong Filipino para sa Batang Filipino.”\r\n\r\n         Relative to this, our school celebrated this special day in a peculiar way and that is a virtual program, simple yet meaningful with the help of GPTA officers. It is  “A Gratitude Night for Teachers, Thanks for all you Do”. The celebration was started with a prayer. Followed by the singing of nationalistic song. ', '2022-09-05', '15:41:04', '0.053199398580419teachers_day.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `student`
--

CREATE TABLE `student` (
  `id` int(11) NOT NULL,
  `fname` varchar(50) NOT NULL,
  `lname` varchar(50) NOT NULL,
  `mname` varchar(50) NOT NULL,
  `dob` date NOT NULL,
  `age` int(3) NOT NULL,
  `LRN` bigint(12) NOT NULL,
  `grade` int(2) NOT NULL,
  `section` varchar(1) NOT NULL,
  `address` varchar(100) NOT NULL,
  `status` int(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `student`
--

INSERT INTO `student` (`id`, `fname`, `lname`, `mname`, `dob`, `age`, `LRN`, `grade`, `section`, `address`, `status`) VALUES
(15, 'Billy Jake', 'Ballola', 'Petremetre', '2022-12-16', 20, 102343070016, 1, 'A', 'Laguna', 1),
(16, 'Jayb', 'Bjay', 'Pusod', '2022-12-23', 15, 102343070014, 1, 'B', 'Laguna', 2),
(17, 'Nazh', 'Buag', 'Cupon', '2012-11-05', 11, 108343070022, 5, 'A', 'Brgy. Ilayang Butnong Magdalena, Laguna', 1),
(18, 'Bjay', 'Ballola', 'Petremetre', '2023-01-13', 21, 1093848829, 1, 'A', 'Brgy. Ilayang Butnong Magdalena, Laguna', 2);

-- --------------------------------------------------------

--
-- Table structure for table `teacher`
--

CREATE TABLE `teacher` (
  `id` int(50) NOT NULL,
  `fname` varchar(50) NOT NULL,
  `lname` varchar(50) NOT NULL,
  `dob` date NOT NULL,
  `address` varchar(100) NOT NULL,
  `emailAddress` varchar(50) NOT NULL,
  `contact` bigint(11) NOT NULL,
  `status` int(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `teacher`
--

INSERT INTO `teacher` (`id`, `fname`, `lname`, `dob`, `address`, `emailAddress`, `contact`, `status`) VALUES
(15, 'Billy', 'Ballola', '2022-12-23', 'Magdalena, Laguna', 'billyjoelballola@gmail.com', 9059347477, 1),
(16, 'Bjay', 'Ballola', '2023-01-04', 'laguna', 'sample123@gmail.com', 9059347477, 2);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `fname` varchar(50) NOT NULL,
  `lname` varchar(50) NOT NULL,
  `username` varchar(15) NOT NULL,
  `password` varchar(15) NOT NULL,
  `role` varchar(10) NOT NULL,
  `status` int(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `fname`, `lname`, `username`, `password`, `role`, `status`) VALUES
(1, 'parent', 'parent', 'parent', 'parent', 'Parent', 1),
(2, 'teacher', 'teacher', 'teacher123', 'teacher123', 'Teacher', 1),
(3, 'admin', 'admin', 'admin12', 'admin123', 'Admin', 1),
(20, 'Billy', 'Ballola', '2022-12-23-SIS', '2022-12-23-SIS', 'Teacher', 1),
(21, 'Juliusmir', 'Buag', 'jull1234', 'jull123', 'Parent', 1),
(22, 'Bjay', 'Ballola', '2023-01-04-SIS', '2023-01-04-SIS', 'Teacher', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `announcement`
--
ALTER TABLE `announcement`
  ADD PRIMARY KEY (`id`),
  ADD KEY `uid` (`uid`);

--
-- Indexes for table `article`
--
ALTER TABLE `article`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `event`
--
ALTER TABLE `event`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `student`
--
ALTER TABLE `student`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `teacher`
--
ALTER TABLE `teacher`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `announcement`
--
ALTER TABLE `announcement`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=57;

--
-- AUTO_INCREMENT for table `article`
--
ALTER TABLE `article`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- AUTO_INCREMENT for table `event`
--
ALTER TABLE `event`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `student`
--
ALTER TABLE `student`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `teacher`
--
ALTER TABLE `teacher`
  MODIFY `id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `announcement`
--
ALTER TABLE `announcement`
  ADD CONSTRAINT `announcement_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
