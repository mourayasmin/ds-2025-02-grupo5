#!/bin/bash
# Database initialization script
# This script can be used to initialize or reset the database

set -e

echo "Waiting for PostgreSQL to be ready..."
until PGPASSWORD=ai_olympics_password psql -h localhost -U ai_olympics_user -d postgres -c '\q' 2>/dev/null; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

echo "PostgreSQL is ready!"

echo "Running migrations..."
PGPASSWORD=ai_olympics_password psql -h localhost -U ai_olympics_user -d ai_olympics_db -f migrations/001_initial_schema.sql

echo "Applying schema updates..."
PGPASSWORD=ai_olympics_password psql -h localhost -U ai_olympics_user -d ai_olympics_db -f migrations/002_update_serie_ano_length.sql 2>/dev/null || echo "Migration 002 already applied or not needed"

echo "Database initialized successfully!"

