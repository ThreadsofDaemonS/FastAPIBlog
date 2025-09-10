# FastAPIBlog

A modern FastAPI-based blog application with AI-powered content moderation and automatic reply features.

## Features

- **Post Management**: Create and manage blog posts
- **Comment System**: Users can comment on posts with automatic moderation
- **AI Moderation**: Automatic detection of toxic/inappropriate content using Google's Gemini AI
- **Auto-Reply**: AI-generated automatic replies to comments (in Ukrainian)
- **Analytics**: Daily breakdown of comments and moderation statistics
- **User Authentication**: Secure user registration and login system
- **PostgreSQL Database**: Robust data storage with async support
- **Database Migrations**: Alembic-powered schema management

## Technology Stack

- **Backend**: FastAPI (Python 3.12+)
- **Database**: PostgreSQL with async support (asyncpg)
- **ORM**: SQLAlchemy 2.0 (async)
- **AI Integration**: Google Gemini AI for moderation and auto-replies
- **Authentication**: JWT tokens with bcrypt password hashing
- **Migrations**: Alembic
- **Testing**: pytest with async support
- **Code Quality**: Black formatter, Ruff linter

## Prerequisites

- Python 3.12 or higher
- PostgreSQL database
- Google AI API key (for Gemini integration)

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/ThreadsofDaemonS/FastAPIBlog.git
cd FastAPIBlog
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the project root based on `.env.sample`:

```bash
cp .env.sample .env
```

Configure the following environment variables in `.env`:

```env
# Database Configuration
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=fastapiblog

# Google AI Configuration
GOOGLE_API_KEY=your_gemini_api_key

# JWT Configuration  
SECRET_KEY=your_secret_key_for_jwt
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Database Setup

#### Using Docker (Recommended)

```bash
docker-compose up -d
```

#### Manual PostgreSQL Setup

1. Install PostgreSQL
2. Create a database:
```sql
CREATE DATABASE fastapiblog;
```

3. Run migrations:
```bash
alembic upgrade head
```

### 5. Run the Application

#### Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The application will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:

- **Interactive API docs**: `http://localhost:8000/docs`
- **ReDoc documentation**: `http://localhost:8000/redoc`

## Project Structure

```
FastAPIBlog/
├── app/
│   ├── core/          # Core configurations (database, security)
│   ├── models/        # SQLAlchemy models
│   ├── routers/       # API route handlers
│   ├── schemas/       # Pydantic schemas
│   ├── services/      # Business logic services
│   └── main.py        # FastAPI application entry point
├── alembic/           # Database migration files
├── tests/             # Test suite
├── requirements.txt   # Python dependencies
└── docker-compose.yml # Docker configuration
```

## Key Features Explained

### AI Content Moderation

The application uses Google's Gemini AI to automatically moderate comments:

- **Manual Filtering**: First checks against a predefined list of inappropriate words
- **AI Analysis**: Uses Gemini AI to detect toxic or inappropriate content
- **Automatic Blocking**: Toxic comments are automatically marked as blocked

### Auto-Reply System

- Posts can be configured to automatically reply to comments
- Replies are generated using AI and are contextually relevant
- Configurable delay before sending replies
- Authors don't receive auto-replies to their own comments

### Analytics

Track engagement with detailed analytics:
- Daily comment counts
- Moderation statistics
- Blocked vs. approved comments

## API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login

### Posts
- `GET /posts/` - List all posts
- `POST /posts/` - Create a new post
- `GET /posts/{id}` - Get specific post

### Comments
- `GET /posts/{id}/comments` - Get comments for a post
- `POST /comments/` - Create a new comment

### Analytics
- `GET /analytics/comments-daily-breakdown` - Get daily comment statistics

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black .
```

### Linting

```bash
ruff check .
```

### Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

## Docker Deployment

The application includes Docker support for easy deployment:

```bash
docker-compose up -d
```

This will start:
- FastAPI application
- PostgreSQL database
- Automatic database migrations

## Configuration Notes

### AI Integration

- The AI moderation and auto-reply features are configured to work with Ukrainian text
- The system maintains Ukrainian prompts for optimal AI performance with Ukrainian content
- Auto-replies are generated in Ukrainian language

### Security

- Passwords are hashed using bcrypt
- JWT tokens are used for authentication
- Database relationships include proper CASCADE constraints
- Input validation using Pydantic schemas

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions, please use the GitHub issue tracker.
