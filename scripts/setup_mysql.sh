#!/bin/bash
# =====================================================================
# FACEATTEND ENTERPRISE - SCRIPT KHỞI TẠO CƠ SỞ DỮ LIỆU MYSQL
# Nạp database schema 21 bảng và dữ liệu seed mẫu
# =====================================================================

set -e

MYSQL_USER=${1:-"root"}
MYSQL_HOST=${2:-"localhost"}
MYSQL_PORT=${3:-"3306"}

echo "Đang nạp cấu trúc 21 bảng vào MySQL database 'faceattend'..."
mysql -u "$MYSQL_USER" -h "$MYSQL_HOST" -P "$MYSQL_PORT" -p < database/faceattend_schema.sql

echo "Đang nạp dữ liệu mẫu (Seed Data)..."
mysql -u "$MYSQL_USER" -h "$MYSQL_HOST" -P "$MYSQL_PORT" -p < database/seed_data.sql

echo "✅ Khởi tạo MySQL database faceattend hoàn tất!"
