# SQL Master - Interactive SQL Learning Platform

An interactive web application for learning SQL fundamentals with hands-on examples and real-time query execution. Built with Flask backend and modern vanilla JavaScript frontend, designed for deployment on Vercel's free tier.

![SQL Master](https://img.shields.io/badge/SQL-Learning-blue) ![Flask](https://img.shields.io/badge/Flask-3.0.0-green) ![License](https://img.shields.io/badge/license-MIT-blue)

## ✨ Features

- **10 Comprehensive Lessons** covering SQL fundamentals:
  - Introduction to SQL
  - Relational Databases
  - SQL Statements
  - CREATE TABLE
  - INSERT INTO
  - SELECT Statement
  - ALTER TABLE
  - UPDATE
  - DELETE
  - SQL Constraints

- **Interactive SQL Editor** with real-time query execution
- **Safe Sandbox Environment** - Each query runs in an isolated in-memory database
- **Beautiful Dark Theme** with modern UI/UX
- **Responsive Design** - Works on desktop and mobile
- **Pre-loaded Examples** - Click to try example queries instantly
- **Syntax Highlighting** - Easy-to-read SQL code
- **Instant Feedback** - See query results immediately

## 🚀 Quick Start

### Local Development

1. **Clone or navigate to the project directory:**
   ```bash
   cd "c:\Users\somay\Documents\Python Projects\SQL Learning APP"
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask development server:**
   ```bash
   python api/index.py
   ```

4. **Open your browser:**
   Navigate to `http://localhost:5000`

### Deploy to Vercel

1. **Install Vercel CLI (if not already installed):**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel:**
   ```bash
   vercel login
   ```

3. **Deploy:**
   ```bash
   vercel
   ```

4. **Follow the prompts:**
   - Set up and deploy: Yes
   - Which scope: Select your account
   - Link to existing project: No
   - Project name: sql-learning-app (or your choice)
   - Directory: ./ (current directory)
   - Override settings: No

5. **Production deployment:**
   ```bash
   vercel --prod
   ```

Your app will be live at the provided Vercel URL!

## 📁 Project Structure

```
SQL Learning APP/
├── api/
│   ├── index.py          # Flask backend with SQL execution engine
│   └── lessons.py        # Lesson content and data
├── index.html            # Main HTML structure
├── styles.css            # Dark theme styling
├── script.js             # Frontend JavaScript logic
├── vercel.json           # Vercel deployment configuration
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## 🛠️ Technology Stack

### Backend
- **Flask 3.0.0** - Python web framework
- **Flask-CORS** - Cross-origin resource sharing
- **SQLite3** - In-memory database for safe query execution

### Frontend
- **HTML5** - Semantic structure
- **CSS3** - Modern dark theme with glassmorphism
- **Vanilla JavaScript** - No frameworks, pure JS
- **Inter Font** - Clean, modern typography

### Deployment
- **Vercel** - Serverless deployment platform
- **Python Runtime** - Serverless functions

## 🔒 Security Features

- **SQL Injection Prevention** - Query validation and sanitization
- **Sandboxed Execution** - Each query runs in isolated environment
- **Stateless Architecture** - Fresh database per request
- **Allowed Operations Only** - Only SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER
- **Dangerous Operations Blocked** - DROP DATABASE, EXEC, file operations, etc.

## 📖 Usage Guide

1. **Navigate Lessons** - Click on any lesson in the left sidebar
2. **Read Theory** - Learn concepts in the main content area
3. **Try Examples** - Click "Try It" buttons to load example queries
4. **Write Queries** - Type your own SQL in the editor panel
5. **Execute** - Click "Run Query" or press Ctrl+Enter
6. **View Results** - See query results in the results panel below the editor

## 🎨 Design Features

- **Dark Mode** - Easy on the eyes for extended learning sessions
- **Gradient Accents** - Purple/blue gradient for modern look
- **Smooth Animations** - Polished transitions and hover effects
- **Responsive Layout** - Three-panel layout adapts to screen size
- **Syntax Highlighting** - Color-coded SQL for better readability

## 🤝 Contributing

This is a learning project. Feel free to fork and customize for your own use!

## 📝 License

MIT License - Feel free to use this project for learning and teaching SQL.

## 🐛 Troubleshooting

### Local Development Issues

**Port already in use:**
```bash
# Change port in api/index.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

**CORS errors:**
- Make sure Flask-CORS is installed
- Check that the API_BASE_URL in script.js matches your setup

### Vercel Deployment Issues

**Build fails:**
- Ensure `requirements.txt` is in the root directory
- Check that Python version is compatible (3.9+)

**API routes not working:**
- Verify `vercel.json` configuration
- Check that `api/index.py` exists and is correct

## 🎯 Future Enhancements

- User progress tracking
- More advanced SQL topics (JOINs, subqueries, etc.)
- Code challenges and quizzes
- Certificate of completion
- Multiple database support (PostgreSQL, MySQL)
- Saved queries and history

## 📧 Support

For issues or questions, please open an issue on the project repository.

---

**Happy Learning! 🚀**
