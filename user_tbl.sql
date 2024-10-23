CREATE TABLE `user_tbl` (
  `user_id` int(11) NOT NULL COMMENT 'ユーザ主キー',
  `email` varchar(50) NOT NULL COMMENT 'メールアドレス',
  `passwd` varchar(20) DEFAULT NULL COMMENT 'パスワード',
  `security_code` varchar(10) DEFAULT NULL COMMENT 'セキュリティコード',
  `date_of_expiry` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '有効期限',
  `auth_regist_flag` tinyint(1) DEFAULT NULL COMMENT 'auth_registフラグ'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `user_tbl` (`user_id`, `email`, `passwd`, `security_code`, `date_of_expiry`, `auth_regist_flag`) VALUES
(1, 'yamada@gmail.com', '123456', NULL, '2024-10-22 01:40:15', NULL);