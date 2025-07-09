---
type: Page
title: sportsclub Database Queries & Data Visualizations
description: null
icon: null
createdAt: '2025-01-24T12:54:03.49Z'
creationDate: 2025-01-24 06:54
modificationDate: 2025-06-11 20:15
tags: [Sportsclub, Data, Database, analytics]
coverImage: null
---

# sportsclub Database Queries & Data Visualizations

### Creating Schema

```sql
-- Recreate Players Table
CREATE TABLE IF NOT EXISTS players (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  username TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Recreate Seasons Table
CREATE TABLE IF NOT EXISTS seasons (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL
);

-- Recreate Wallets Table
CREATE TABLE IF NOT EXISTS wallets (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  player_id BIGINT REFERENCES players (id),
  season_id BIGINT REFERENCES seasons (id),
  balance BIGINT DEFAULT 100000,
  UNIQUE (player_id, season_id)
);

-- Recreate Sports Table
CREATE TABLE IF NOT EXISTS sports (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  name TEXT UNIQUE NOT NULL
);

-- Recreate Events Table
CREATE TABLE IF NOT EXISTS events (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  sport_id BIGINT REFERENCES sports (id),
  season_id BIGINT REFERENCES seasons (id),
  event_date DATE NOT NULL,
  odds TEXT NOT NULL,
  winner TEXT
);

-- Recreate Picks Table
CREATE TABLE IF NOT EXISTS picks (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  player_id BIGINT REFERENCES players (id),
  event_id BIGINT REFERENCES events (id),
  amount BIGINT CHECK (amount % 1000 = 0),
  prediction TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Recreate Leaderboard View
CREATE OR REPLACE VIEW leaderboard AS
SELECT
  p.id AS player_id,
  p.username,
  w.balance + COALESCE(
    SUM(
      CASE
        WHEN e.winner IS NULL THEN pk.amount
        ELSE 0
      END
    ),
    0
  ) AS total_coins
FROM
  players p
  JOIN wallets w ON p.id = w.player_id
  LEFT JOIN picks pk ON p.id = pk.player_id
  LEFT JOIN events e ON pk.event_id = e.id
GROUP BY
  p.id,
  w.balance
ORDER BY
  total_coins DESC;

-- Insert sample players
INSERT INTO
  players (username, email)
VALUES
  ('player1', 'player1@example.com'),
  ('player2', 'player2@example.com'),
  ('player3', 'player3@example.com');

-- Insert a current season
INSERT INTO
  seasons (start_date, end_date)
VALUES
  ('2023-10-01', '2023-10-31');

-- Insert sample sports
INSERT INTO
  sports (name)
VALUES
  ('Football'),
  ('Basketball'),
  ('Baseball'),
  ('Soccer'),
  ('Tennis'),
  ('Golf'),
  ('Hockey'),
  ('Cricket'),
  ('Rugby'),
  ('Boxing'),
  ('MMA'),
  ('Cycling');

-- Insert wallets for players for the current season
INSERT INTO
  wallets (player_id, season_id)
VALUES
  (1, 1),
  (2, 1),
  (3, 1);

-- Insert sample events
INSERT INTO
  events (sport_id, season_id, event_date, odds)
VALUES
  (1, 1, '2023-10-05', '+150'),
  (2, 1, '2023-10-10', '-200'),
  (3, 1, '2023-10-15', '+250');

-- Insert sample picks
INSERT INTO
  picks (player_id, event_id, amount, prediction)
VALUES
  (1, 1, 1000, 'Team A'),
  (2, 2, 2000, 'Team B'),
  (3, 3, 3000, 'Team C');

-- Fetch the top 3 players and a specific player (assuming player_id = 1 for the current user) from the leaderboard
SELECT
  *
FROM
  leaderboard
WHERE
  player_id = 1
  OR player_id IN (
    SELECT
      player_id
    FROM
      leaderboard
    ORDER BY
      total_coins DESC
    LIMIT
      3
  );
;

-- Check if the team_stats table exists
SELECT
  EXISTS (
    SELECT
    FROM
      information_schema.tables
    WHERE
      table_name = 'team_stats'
  );

-- Create a mock team_stats table
CREATE TABLE team_stats (
  team_id BIGINT PRIMARY KEY,
  team_name TEXT,
  games_played INT,
  wins INT,
  losses INT,
  points_scored INT,
  points_allowed INT,
  field_goal_percentage DECIMAL(5, 2),
  turnovers INT
);

-- Insert sample data for a team
INSERT INTO
  team_stats (
    team_id,
    team_name,
    games_played,
    wins,
    losses,
    points_scored,
    points_allowed,
    field_goal_percentage,
    turnovers
  )
VALUES
  (1, 'Team A', 10, 6, 4, 950, 870, 45.5, 120);

;

-- Insert sample data for a second team
INSERT INTO
  team_stats (
    team_id,
    team_name,
    games_played,
    wins,
    losses,
    points_scored,
    points_allowed,
    field_goal_percentage,
    turnovers
  )
VALUES
  (2, 'Team B', 10, 7, 3, 980, 860, 47.0, 110);

-- Fetch stats for both teams
SELECT
  *
FROM
  team_stats
WHERE
  team_id IN (1, 2);
```

### Top 3 and Me

```sql
-- Fetch the top 3 players and a specific player (assuming player_id = 1 for the current user) from the leaderboard
SELECT
  *
FROM
  leaderboard
WHERE
  player_id = 1
  OR player_id IN (
    SELECT
      player_id
    FROM
      leaderboard
    ORDER BY
      total_coins DESC
    LIMIT
      3
  );
```

### Top 3 and Me Chart

[[image]]

### Comparative Analysis

[image](Images/image.md%20(1))
