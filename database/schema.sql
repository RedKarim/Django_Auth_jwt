CREATE TABLE IF NOT EXISTS `user_tbl` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ユーザ主キー',
  `email` varchar(50) NOT NULL COMMENT 'メールアドレス',
  `passwd` varchar(20) DEFAULT NULL COMMENT 'パスワード',
  `security_code` varchar(10) DEFAULT NULL COMMENT 'セキュリティコード',
  `date_of_expiry` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '有効期限',
  `auth_regist_flag` tinyint(1) DEFAULT NULL COMMENT 'auth_registフラグ',
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
