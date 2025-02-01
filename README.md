# Multilingual FAQ System

A robust backend system for managing Frequently Asked Questions (FAQs) with automatic multi-language translation support, built using Django REST Framework. The system features WYSIWYG editor integration, Redis caching, and comprehensive API endpoints for FAQ management.

## Features

- 🌐 Multi-language support with automatic translation
- 📝 WYSIWYG editor for rich text answers
- ⚡ Redis caching for improved performance
- 🔄 Real-time translation using Google Translate API
- 🎨 Interactive UI for API testing
- 🔒 Admin interface for FAQ management
- ✅ Comprehensive test coverage

## Project Structure
```
faq_project/          # Main project directory
├── faq/              # FAQ application
├── faq_project/      # Project settings directory
├── requirements.txt
├── manage.py
└── README.md
```

## Supported Languages

The system supports translation to the following languages:
- Hindi (hi)
- Bengali (bn)
- Tamil (ta)
- Telugu (te)
- Malayalam (ml)
- Gujarati (gu)
- Kannada (kn)
- Marathi (mr)
- Punjabi (pa)
- Odia (or)

## Live Demo

You can test the API at: [https://bharatfd-backend-7u4w.onrender.com/](https://bharatfd-backend-7u4w.onrender.com/)

## Installation

### Method 1: Traditional Setup

1. Clone the repository
2. Navigate to the project directory:
   ```bash
   cd faq_project
   ```
3. Set up environment variables:
   ```bash
   REDIS_URL=Your_redis_cloud_url
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run migrations:
   ```bash
   python manage.py makemigrations faq
   python manage.py migrate
   ```
6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
7. Start the development server:
   ```bash
   python manage.py runserver
   ```

### Method 2: Docker Setup

1. Build the Docker image:
   ```bash
   docker build -t faq-system .
   ```
2. Run the container:
   ```bash
   docker run -p 8000:8000 -e REDIS_URL=Your_redis_cloud_url faq-system
   ```

## API Documentation

### Endpoints

#### List/Create FAQs
- `GET /api/faqs/` - Fetch all FAQs
- `GET /api/faqs/?lang=hi` - Fetch all FAQs in specified language
- `POST /api/faqs/` - Create new FAQ

Example POST request:
```json
{
    "question": "What is the sun?",
    "answer": "<p>The sun is a star at the center of our solar system.</p>"
}
```
Note: Only English content is required - translations are generated automatically.

#### Single FAQ Operations
- `GET /api/faqs/{id}/` - Fetch specific FAQ
- `GET /api/faqs/{id}/?lang=hi` - Fetch specific FAQ in desired language
- `PATCH /api/faqs/{id}/` - Update FAQ
- `DELETE /api/faqs/{id}/` - Delete FAQ

### Admin Interface

1. Access the admin panel at `/admin`
2. Log in using your superuser credentials
3. Navigate to the FAQs section to manage entries

## Testing

Run the test suite:
```bash
python manage.py test faq
```

## Technical Details

- **WYSIWYG Editor**: Implemented using RichTextField for rich text formatting
- **Caching**: Redis implementation for improved performance
- **Translation**: Automated using googletrans library
- **API Framework**: Django REST Framework
- **Testing**: Comprehensive test suite included

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m 'feat: Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Submit a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
