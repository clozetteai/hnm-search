# User Management
# Create a new user
curl -X POST http://localhost:7600/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "newuser5", "email": "newuser5@example.com", "password": "password123"}'

# Login
curl -X POST http://localhost:7600/api/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=newuser5&password=password123"

YOUR_ACCESS_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJuZXd1c2VyNSIsImV4cCI6MTcyNDE2NTM1M30.4BqH9znJf8sh7KD0tP09KINeFMmWUUINFWdyPuO2a7Q

# Get current user info
curl -X GET http://localhost:7600/api/users/me \
  -H "Authorization: Bearer $YOUR_ACCESS_TOKEN" | jq

# Update user settings
curl -X PUT http://localhost:7600/api/users/settings \
  -H "Authorization: Bearer $YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"theme": "dark", "language": "en"}' | jq

# Chat Sessions
# Create a new chat session
curl -X POST http://localhost:7600/api/chat-sessions/ \
  -H "Authorization: Bearer $YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "New Chat 5"}'  | jq

# List chat sessions
curl -X GET http://localhost:7600/api/chat-sessions/ \
  -H "Authorization: Bearer $YOUR_ACCESS_TOKEN"  | jq

# Messages
# Create a new message in a chat session
curl -X POST http://localhost:7600/chat-sessions/1/messages/ \
  -H "Authorization: Bearer $YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "Hello, AI!", "message_type": "user"}'  | jq

# List messages in a chat session
curl -X GET http://localhost:7600/api/chat-sessions/1/messages/ \
  -H "Authorization: Bearer $YOUR_ACCESS_TOKEN"  | jq

# Bot Responses
# Create a bot response
curl -X POST http://localhost:7600/api/bot-responses/ \
  -H "Content-Type: application/json" \
  -d '{"message_id": 1, "content": "Hello, human!", "model_version": "v1.0", "tokens_used": 10}'  | jq

# Feedback
# Create feedback for a message
curl -X POST http://localhost:7600/api/messages/1/feedback \
  -H "Authorization: Bearer $YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"rating": 5, "comment": "Great response!"}'  | jq

# API Keys
# Create a new API key
curl -X POST http://localhost:7600/api/api-keys/ \
  -H "Authorization: Bearer $YOUR_ACCESS_TOKEN"

# List API keys
curl -X GET http://localhost:7600/api/api-keys/ \
  -H "Authorization: Bearer $YOUR_ACCESS_TOKEN"

# Delete an API key
curl -X DELETE http://localhost:7600/api/api-keys/1 \
  -H "Authorization: Bearer $YOUR_ACCESS_TOKEN"

# Prompt Templates
# Create a new prompt template
curl -X POST http://localhost:7600/api/prompt-templates/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Greeting", "content": "Hello, {name}!"}'

# List prompt templates
curl -X GET http://localhost:7600/api/prompt-templates/

# Subscriptions
# Create a new subscription
curl -X POST http://localhost:7600/subscriptions/ \
  -H "Authorization: Bearer $YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"plan_type": "monthly"}'

# Get current subscription
curl -X GET http://localhost:7600/subscriptions/current \
  -H "Authorization: Bearer $YOUR_ACCESS_TOKEN"

# Cancel subscription
curl -X DELETE http://localhost:7600/subscriptions/cancel \
  -H "Authorization: Bearer $YOUR_ACCESS_TOKEN"

# Delete user account
curl -X DELETE http://localhost:7600/users/me \
  -H "Authorization: Bearer $YOUR_ACCESS_TOKEN"