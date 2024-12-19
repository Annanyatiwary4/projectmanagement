# ProjectFolio

## 🚀 Features
User Authentication: Secure login system for candidates to access their personalized dashboard.
Progress Visualization:
progress chart to show overall performance.
Detailed statistics, including:
Total Projects
Completed Projects
Remaining Projects
Overall Score
Dynamic Progress Bars:
Visual representation of project completion status.
Real-time updates based on user data.
Responsive Design: Mobile and desktop-friendly user interface

## 🛠️ Tech Stack

- Django 5.1.4
- PostgreSQL
- Python 3.x
- WhiteNoise (for static files)
- Django CORS Headers
- Python-dotenv

## ⚙️ Installation & Setup

1. Clone the repository
```bash
git clone <your-repository-url>
cd projectfolio
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create a .env file in the root directory with the following variables:
```
DEBUG=True
SECRET_KEY=your-secret-key
PGDATABASE=your-database-name
PGUSER=your-database-user
PGPASSWORD=your-database-password
PGHOST=your-database-host
PGPORT=your-database-port
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-email-password
```

5. Run migrations
```bash
python manage.py migrate
```

6. Create a superuser
```bash
python manage.py createsuperuser
```

7. Run the development server
```bash
python manage.py runserver
```

## 🚀 Deployment on Vercel

1. Install Vercel CLI
```bash
npm i -g vercel
```

3. Initialize Vercel in your project
```bash
vercel init
```

4. Deploy
```bash
vercel


5. Add environment variables in the Vercel dashboard

6. Run `python manage.py collectstatic` before deployment


