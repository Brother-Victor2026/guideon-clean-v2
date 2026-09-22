CREATE TABLE IF NOT EXISTS analytics (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  user_id TEXT NOT NULL,
  event_type TEXT,
  interaction_data JSONB,
  timestamp TIMESTAMP DEFAULT NOW(),
  response_time_ms INT,
  tokens_used INT,
  error_message TEXT,
  ip_address TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
