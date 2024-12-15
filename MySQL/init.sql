-- 시간대를 한국 시간(KST)으로 설정
SET time_zone = '+09:00';

-- 데이터베이스 생성
CREATE DATABASE IF NOT EXISTS CRUDPOST;

-- 데이터베이스 사용
USE CRUDPOST;

-- 게시판 테이블 생성
CREATE TABLE IF NOT EXISTS CRUD_POST (
    POST_id INT AUTO_INCREMENT PRIMARY KEY,  -- 게시판 고유 ID
    POST_title VARCHAR(50) NOT NULL,  -- 게시판 제목
    POST_contents TEXT NOT NULL,  -- 게시판 내용
    Create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 게시판 생성 시간
    Update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP -- 게시판 수정 시간
);