# Authentication Implementation Guide for Task Manager

## 1. Authentication Methods
### A. Google OAuth Integration
1. Google Cloud Console Setup
   - Create/select project at [Google Cloud Console](https://console.cloud.google.com/)
   - Enable "Google People API"
   - Configure OAuth consent screen as "External"
   - Add scopes: email, profile
   - Add test users for development

2. OAuth Credentials Setup
   - Create OAuth 2.0 Client ID
   - Application type: Web application
   - Authorized redirect URIs:
     ```
     http://localhost:5000/auth/google
     http://127.0.0.1:5000/auth/google
     ```
   - Note: Authorized domains not needed for testing

### B. Regular Authentication
1. User Model Structure
   ```python
   class User(UserMixin, db.Model):
       id = db.Column(db.Integer, primary_key=True)
       email = db.Column(db.String(100), unique=True)
       name = db.Column(db.String(100))
       password_hash = db.Column(db.String(200))
       google_id = db.Column(db.String(100))
       profile_pic = db.Column(db.String(200))
       created_at = db.Column(db.DateTime)
       last_login = db.Column(db.DateTime)

       def set_password(self, password):
           self.password_hash = generate_password_hash(password)

       def check_password(self, password):
           return check_password_hash(self.password_hash, password)
   ```

## 2. Environment Configuration
1. Create .env file:
   ```env
   # Flask Configuration
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-here

   # Google OAuth Configuration
   GOOGLE_CLIENT_ID=your-client-id
   GOOGLE_CLIENT_SECRET=your-client-secret
   
   # Database Configuration
   DATABASE_URL=sqlite:///tasks.db
   ```

2. Required Packages:
   ```txt
   Flask-Login==0.6.3
   authlib==1.3.0
   requests==2.31.0
   python-dotenv==1.0.0
   ```

## 3. Authentication Endpoints

### A. Google OAuth Routes
```python
@app.route('/login/google')
def google_login():
    redirect_uri = url_for('google_auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/auth/google')
def google_auth():
    try:
        token = oauth.google.authorize_access_token()
        resp = oauth.google.get('https://www.googleapis.com/oauth2/v3/userinfo')
        user_info = resp.json()
        
        user = User.query.filter_by(email=user_info['email']).first()
        if not user:
            user = User(
                name=user_info['name'],
                email=user_info['email'],
                google_id=user_info['sub'],
                profile_pic=user_info.get('picture')
            )
            db.session.add(user)
            db.session.commit()
        
        login_user(user)
        flash(f'Welcome, {user.name}!', 'success')
        return redirect(url_for('dashboard'))
    except Exception as e:
        flash('Failed to log in with Google.', 'error')
        return redirect(url_for('login'))
```

### B. Regular Authentication Routes
```python
@app.route('/')
def landing():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('landing.html')

@app.route('/dashboard')
@login_required
def dashboard():
    tasks = Task.query.filter_by(user_id=current_user.id)\
                     .order_by(Task.created_at.desc()).all()
    return render_template('index.html', tasks=tasks)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
            
        flash('Invalid credentials', 'error')
    return render_template('auth/login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        user = User(
            email=request.form.get('email'),
            name=request.form.get('name')
        )
        user.set_password(request.form.get('password'))
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('auth/signup.html')
```

### C. Route Structure
1. Public Routes
   - '/' (landing page)
   - '/login'
   - '/signup'
   - '/login/google'
   - '/auth/google'

2. Protected Routes
   - '/dashboard' (main application interface)
   - All task-related routes
   - All category-related routes

## 4. Security Implementation

### A. Password Security
- Passwords hashed using Werkzeug's security functions
- No plain text passwords stored
- Password validation on signup

### B. Session Management
- Flask-Login for session handling
- Secure session configuration
- Proper logout implementation

### C. OAuth Security
- Token handling in memory only
- Secure client credentials storage
- Proper scope limitations

## 5. Error Handling
1. Authentication Errors
   - Invalid credentials
   - OAuth failures
   - Session timeouts

2. User Feedback
   - Flash messages for errors
   - Success notifications
   - Clear error messages

## 6. Testing Procedures
1. Development Testing
   ```bash
   # Initialize database
   python init_db.py
   
   # Run application
   flask run
   ```

2. Test Scenarios
   - Regular signup/login
   - Google OAuth flow
   - Password validation
   - Session persistence
   - Error handling

## 7. Production Considerations
1. Security Measures
   - HTTPS enforcement
   - Secure cookie settings
   - Rate limiting
   - Input validation

2. Deployment Steps
   - Environment configuration
   - Database migrations
   - SSL certificate setup
   - Domain verification

## 8. Maintenance Tasks
1. Regular Updates
   - Security patches
   - Dependency updates
   - OAuth compliance

2. Monitoring
   - Authentication attempts
   - Error logs
   - Session management
   - User activity

3. Backup Procedures
   - Database backups
   - Configuration backups
   - Recovery testing
