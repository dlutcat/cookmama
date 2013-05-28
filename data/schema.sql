--
-- Table structure for table `booking`
--

DROP TABLE IF EXISTS `booking`;
CREATE TABLE `booking` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(40) DEFAULT '',
  `summary` varchar(1000) DEFAULT '',
  `user_id` int(11) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=innodb DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `booking_item`;
CREATE TABLE `booking_item` (
  `user_id` int(11) unsigned DEFAULT NULL,
  `item_id` int(11) unsigned DEFAULT NULL,
  `created` timestamp NOT NULL DEFAULT current_timestamp,
  PRIMARY KEY (`user_id`, `item_id`)
) ENGINE=innodb DEFAULT CHARSET=utf8;


--
-- Table structure for table `item`
--

DROP TABLE IF EXISTS `item`;
CREATE TABLE `item` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(40) DEFAULT '',
  `img` varchar(250) DEFAULT '',
  `summary` varchar(1000) DEFAULT '',
  `created` timestamp NOT NULL DEFAULT current_timestamp,
  PRIMARY KEY (`id`)
) ENGINE=innodb DEFAULT CHARSET=utf8;

--
-- Table structure for table `shop`
--

DROP TABLE IF EXISTS `shop`;
CREATE TABLE `shop` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(40) DEFAULT '',
  `summary` varchar(1000) DEFAULT '',
  `tel1` varchar(20) DEFAULT '',
  `tel2` varchar(20) DEFAULT '',
  `tel3` varchar(20) DEFAULT '',
  `created` timestamp NOT NULL DEFAULT current_timestamp,
  PRIMARY KEY (`id`)
) ENGINE=innodb DEFAULT CHARSET=utf8;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(40) DEFAULT '',
  `created` timestamp NOT NULL DEFAULT current_timestamp,
  PRIMARY KEY (`id`)
) ENGINE=innodb DEFAULT CHARSET=utf8;
