-- Drop database if exists (be careful with this in production!)
IF EXISTS (SELECT * FROM sys.databases WHERE name = 'recovery_db')
DROP DATABASE recovery_db;

-- Create database
CREATE DATABASE recovery_db;

-- Connect to the recovery_db
USE recovery_db;

-- Create tables
CREATE TABLE users (
    user_id INT IDENTITY(1,1) PRIMARY KEY,
    email NVARCHAR(255) UNIQUE NOT NULL,
    username NVARCHAR(255) UNIQUE NOT NULL,
    created_at DATETIME2 DEFAULT GETDATE(),
    updated_at DATETIME2 DEFAULT GETDATE()
);

CREATE TABLE goals (
    goal_id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT FOREIGN KEY REFERENCES users(user_id),
    goal_type NVARCHAR(50) NOT NULL,
    target_value FLOAT,
    current_value FLOAT DEFAULT 0.0,
    start_date DATE NOT NULL,
    target_date DATE NOT NULL,
    status NVARCHAR(20) DEFAULT 'not_started'
);

CREATE TABLE tracking_data (
    tracking_id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT FOREIGN KEY REFERENCES users(user_id),
    date DATE NOT NULL,
    consumption_amount FLOAT,
    money_saved FLOAT,
    associated_habits NVARCHAR(MAX),
    mood_score INT,
    triggers_encountered NVARCHAR(MAX),
    coping_strategies_used NVARCHAR(MAX)
);

CREATE TABLE buddy_matches (
    match_id INT IDENTITY(1,1) PRIMARY KEY,
    user1_id INT FOREIGN KEY REFERENCES users(user_id),
    user2_id INT FOREIGN KEY REFERENCES users(user_id),
    created_at DATETIME2 DEFAULT GETDATE(),
    is_active BIT DEFAULT 1,
    chat_enabled BIT DEFAULT 1
);

CREATE TABLE buddy_preferences (
    preference_id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT FOREIGN KEY REFERENCES users(user_id),
    addiction_type NVARCHAR(255),
    recovery_stage NVARCHAR(255),
    preferred_contact_frequency NVARCHAR(255),
    timezone NVARCHAR(50)
);

CREATE TABLE chat_messages (
    message_id INT IDENTITY(1,1) PRIMARY KEY,
    match_id INT FOREIGN KEY REFERENCES buddy_matches(match_id),
    sender_id INT FOREIGN KEY REFERENCES users(user_id),
    content NVARCHAR(MAX),
    timestamp DATETIME2 DEFAULT GETDATE()
);

CREATE TABLE relapses (
    relapse_id INT IDENTITY(1,1) PRIMARY KEY,
    goal_id INT FOREIGN KEY REFERENCES goals(goal_id),
    initial_quit_date DATE,
    last_relapse_date DATE,
    total_sober_days INT,
    longest_streak INT,
    notes NVARCHAR(MAX)
);