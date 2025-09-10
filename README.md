# FastAPIBlog

A modern blog API built with FastAPI featuring AI-powered moderation, automatic replies, and comprehensive analytics.

## 🚀 Features

- **User Authentication**: JWT-based authentication system with registration and login
- **Blog Posts Management**: Create, read, update, and delete blog posts
- **Comment System**: Interactive commenting with AI moderation
- **AI Moderation**: Automatic toxicity detection using Google's Gemini AI
- **Auto-Reply**: Intelligent automatic responses to comments using AI
- **Analytics**: Comprehensive analytics for posts and comments with daily breakdowns
- **Async Architecture**: Built with async/await for high performance
- **Database Migrations**: Alembic integration for database schema management

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python 3.9+)
- **Database**: PostgreSQL with SQLAlchemy (async)
- **AI**: Google Gemini AI for moderation and auto-replies
- **Authentication**: JWT tokens with bcrypt password hashing
- **Migrations**: Alembic
- **Testing**: pytest with async support
- **Containerization**: Docker & Docker Compose

## 📋 Prerequisites

- Python 3.9+
- PostgreSQL
- Docker & Docker Compose (optional)
- Google AI API key for moderation features

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/ThreadsofDaemonS/FastAPIBlog.git
cd FastAPIBlog
```

### 2. Environment Configuration

Copy the sample environment file and configure your settings:

```bash
cp .env.sample .env
```

Edit `.env` with your configuration:

```env
# PostgreSQL
POSTGRES_DB=fastapi_blog
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/fastapi_blog

# JWT Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Google AI
GOOGLE_API_KEY=your-google-ai-api-key
```

### 3. Using Docker (Recommended)

```bash
# Start all services
docker-compose up -d --build

# View logs
docker-compose logs -f web
```

The API will be available at `http://localhost:8000`

### 4. Manual Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Start PostgreSQL database
# Make sure PostgreSQL is running and database is created

# Run migrations
alembic upgrade head

# Start the application
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 📁 Project Structure

```
FastAPIBlog/
├── app/
│   ├── core/                 # Core functionality
│   │   ├── db.py            # Database configuration
│   │   └── security.py      # Authentication & security
│   ├── models/              # SQLAlchemy models
│   │   ├── user.py          # User model
│   │   ├── post.py          # Post model
│   │   └── comment.py       # Comment model
│   ├── routers/             # API route handlers
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── post.py          # Post management endpoints
│   │   ├── comment.py       # Comment endpoints
│   │   └── analytics.py     # Analytics endpoints
│   ├── schemas/             # Pydantic schemas
│   │   ├── user.py          # User schemas
│   │   ├── post.py          # Post schemas
│   │   └── comment.py       # Comment schemas
│   ├── services/            # Business logic
│   │   ├── auth.py          # Authentication service
│   │   ├── user.py          # User service
│   │   ├── post.py          # Post service
│   │   ├── comment.py       # Comment service
│   │   ├── ai_moderation.py # AI moderation service
│   │   └── auto_reply.py    # Auto-reply service
│   └── main.py              # FastAPI application entry point
├── alembic/                 # Database migrations
├── tests/                   # Test suite
├── docker-compose.yml       # Docker services configuration
├── Dockerfile              # Docker container configuration
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔧 API Documentation

### Authentication Endpoints (`/auth`)

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "securepassword"
}
```

**Response:**
```json
{
    "id": 1,
    "email": "user@example.com"
}
```

#### Login
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=securepassword

better login through /docs/ using button Authorize
```

**Response:**
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
}
```

#### Get Current User
```http
GET /auth/me
Authorization: Bearer <token>
```

#### Get All Users
```http
GET /auth/all-users
```

### Post Endpoints (`/posts`)

#### Create Post
```http
POST /posts/
Authorization: Bearer <token>
Content-Type: application/json

{
    "content": "This is my first blog post!",
    "auto_reply_enabled": true,
    "reply_delay_sec": 5
}
```

**Response:**
```json
{
    "id": 1,
    "content": "This is my first blog post!",
    "is_blocked": false,
    "auto_reply_enabled": true,
    "reply_delay_sec": 5
}
```

#### Get My Posts
```http
GET /posts/
Authorization: Bearer <token>
```

#### Get Specific Post
```http
GET /posts/{post_id}
Authorization: Bearer <token>
```

### Comment Endpoints (`/comments`)

#### Create Comment
```http
POST /comments/
Authorization: Bearer <token>
Content-Type: application/json

{
    "post_id": 1,
    "content": "Great post! Thanks for sharing."
}
```

**Response:**
```json
{
    "id": 1,
    "post_id": 1,
    "user_id": 2,
    "content": "Great post! Thanks for sharing.",
    "is_blocked": false,
    "created_at": "2024-01-15T10:30:00.000Z"
}
```

#### Get Post Comments
```http
GET /comments/post/{post_id}
```

### Analytics Endpoints (`/api`)

#### Comments Daily Breakdown
```http
GET /api/comments-daily-breakdown?date_from=2024-01-01&date_to=2024-01-31
```

**Response:**
```json
[
    {
        "date": "2024-01-15",
        "total_comments": 25,
        "blocked_comments": 2
    },
    {
        "date": "2024-01-16",
        "total_comments": 18,
        "blocked_comments": 1
    }
]
```

## 🤖 AI Features

### Content Moderation

The application uses Google's Gemini AI to automatically detect toxic, offensive, or inappropriate content in posts and comments. Blocked content is flagged and can be reviewed by administrators.

**Features:**
- Automatic toxicity detection
- Manual blacklist for immediate blocking
- Configurable moderation thresholds

### Auto-Reply System

When enabled on a post, the system automatically generates relevant replies to comments using AI:

**Features:**
- Contextual replies based on post content and comment
- Configurable delay before reply
- Automatic activation per post
- Prevents self-replies (post author won't get auto-replies on their own posts)

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_analytics.py

# Run with verbose output
pytest -v
```

better through docker-compose

```bash

docker-compose exec web pytest -v tests/

```


### Test Coverage

The project includes comprehensive test coverage for:
- Authentication flows
- CRUD operations
- Analytics endpoints
- Error handling

## 🐳 Docker Usage

### Development Environment

```bash
# Start services in development mode
docker-compose up -d --build

# View logs
docker-compose logs -f web

# Stop services
docker-compose down

# Use -v if you want clear database
docker-compose down -v

# Rebuild after changes
docker-compose up -d --build
```

### Production Deployment

The application is containerized and ready for production deployment. Update environment variables appropriately for your production environment.

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: bcrypt for secure password storage
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection
- **Input Validation**: Pydantic schemas validate all inputs
- **Content Moderation**: AI-powered toxic content detection

## 📊 Database Schema

### Users Table
- `id`: Primary key
- `email`: Unique user email
- `hashed_password`: Bcrypt hashed password

### Posts Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `content`: Post content
- `is_blocked`: Moderation flag
- `auto_reply_enabled`: Auto-reply setting
- `reply_delay_sec`: Delay before auto-reply

### Comments Table
- `id`: Primary key
- `post_id`: Foreign key to posts
- `user_id`: Foreign key to users
- `content`: Comment content
- `is_blocked`: Moderation flag
- `created_at`: Timestamp

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `POSTGRES_DB` | PostgreSQL database name | - |
| `POSTGRES_USER` | PostgreSQL username | - |
| `POSTGRES_PASSWORD` | PostgreSQL password | - |
| `POSTGRES_HOST` | PostgreSQL host | localhost |
| `POSTGRES_PORT` | PostgreSQL port | 5432 |
| `SECRET_KEY` | JWT secret key | - |
| `ALGORITHM` | JWT algorithm | HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | 30 |
| `GOOGLE_API_KEY` | Google AI API key | - |

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify PostgreSQL is running
   - Check DATABASE_URL configuration
   - Ensure database exists

2. **Migration Issues**
   ```bash
   # Reset migrations (development only)
   alembic downgrade base
   alembic upgrade head
   ```

3. **AI Moderation Not Working**
   - Verify GOOGLE_API_KEY is set correctly
   - Check Google AI API quota and billing

4. **Authentication Errors**
   - Verify SECRET_KEY is set
   - Check token expiration settings

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check existing documentation
- Review the troubleshooting section

---

**Note**: This application is designed for educational and development purposes. Ensure proper security measures are implemented before deploying to production.
