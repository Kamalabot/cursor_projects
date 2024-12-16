# Docker Setup Guide for Task Manager

## 1. Project Structure
```
task-manager/
├── docker-compose.yml
├── Dockerfile
├── .env
├── .dockerignore
├── requirements.txt
└── app/
    └── app.py
```

## 2. Dockerfile
```dockerfile
# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose port
EXPOSE 5000

# Command to run the application
CMD ["flask", "run", "--host=0.0.0.0"]
```

## 3. Docker Compose Configuration
```yaml
version: '3.8'

services:
  web:
    build: .
    container_name: task-manager
    ports:
      - "5000:5000"
    environment:
      - FLASK_APP=app.py
      - FLASK_ENV=development
      - DATABASE_URL=sqlite:///tasks.db
      - GOOGLE_CLIENT_ID=${GOOGLE_CLIENT_ID}
      - GOOGLE_CLIENT_SECRET=${GOOGLE_CLIENT_SECRET}
      - SECRET_KEY=${SECRET_KEY}
    env_file:
      - .env
    volumes:
      - .:/app
      - sqlite_data:/app/instance

volumes:
  sqlite_data:
```

## 4. Environment Configuration

### A. Create .env file
```env
# Google OAuth Configuration
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
SECRET_KEY=your-secret-key

# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
```

### B. .dockerignore
```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env
*.db
.git
.gitignore
.DS_Store
```

## 5. Build and Run Instructions

### A. Building the Container
```bash
# Build using docker-compose
docker-compose build

# Build with no cache
docker-compose build --no-cache
```

### B. Running the Application
```bash
# Start services
docker-compose up

# Run in detached mode
docker-compose up -d

# Stop services
docker-compose down
```

### C. Viewing Logs
```bash
# View logs
docker-compose logs

# Follow logs
docker-compose logs -f
```

## 6. Environment Variables

### A. Priority Order
1. Shell environment variables
2. Environment variables in .env file
3. Environment variables in docker-compose.yml

### B. Checking Configuration
```bash
# Verify environment variables
docker-compose config
```

## 7. Volume Management

### A. Persistent Storage
- sqlite_data: Stores SQLite database
- Application code mounted at /app

### B. Volume Commands
```bash
# List volumes
docker volume ls

# Clean up unused volumes
docker volume prune
```

## 8. Deployment Considerations

### A. Production Settings
- Update FLASK_ENV to 'production'
- Use proper SECRET_KEY
- Configure proper database URL
- Set up logging

### B. Security
- Never commit .env file
- Use proper file permissions
- Keep dependencies updated
- Use production-grade server

## 9. Troubleshooting

### A. Common Issues
1. Port conflicts
2. Environment variable missing
3. Volume permission issues
4. Build cache problems

### B. Debug Commands
```bash
# Check container status
docker-compose ps

# Check container logs
docker-compose logs web

# Access container shell
docker-compose exec web bash
```

## 10. Maintenance

### A. Regular Tasks
1. Update dependencies
2. Check logs
3. Monitor performance
4. Backup data

### B. Cleanup Commands
```bash
# Remove all containers
docker-compose down

# Remove containers and volumes
docker-compose down -v

# Remove unused images
docker image prune
```

## 11. Docker Hub Deployment

### A. Preparing for Docker Hub
```bash
# Login to Docker Hub
docker login

# Build the image with your Docker Hub username
docker build -t yourusername/task-manager:latest .
```

### B. Image Tags
```bash
# Tag the image for different versions
docker tag task-manager yourusername/task-manager:latest
docker tag task-manager yourusername/task-manager:v1.0.0

# List local images
docker images
```

### C. Pushing to Docker Hub
```bash
# Push the tagged images
docker push yourusername/task-manager:latest
docker push yourusername/task-manager:v1.0.0
```

### D. Version Management
1. Semantic Versioning
   - MAJOR.MINOR.PATCH (e.g., v1.0.0)
   - Latest tag for most recent stable version
   - Specific versions for production deployments

2. Tag Commands
```bash
# Remove local tag
docker rmi yourusername/task-manager:v1.0.0

# Pull specific version
docker pull yourusername/task-manager:v1.0.0
```

### E. Deployment from Docker Hub
```bash
# Pull and run from Docker Hub
docker run -d -p 5000:5000 yourusername/task-manager:latest

# Using with docker-compose
version: '3.8'
services:
  web:
    image: yourusername/task-manager:latest
    # ... rest of your compose configuration
```

### F. Best Practices
1. Image Management
   - Use specific versions in production
   - Regular updates and maintenance
   - Clean up old/unused images
   - Document version changes

2. Security
   - Scan images for vulnerabilities
   - Use multi-stage builds
   - Minimize image size
   - Keep base images updated

3. Automation
```bash
# Build and push script example
#!/bin/bash
VERSION=$1
USERNAME="yourusername"
IMAGE="task-manager"

docker build -t $USERNAME/$IMAGE:$VERSION .
docker tag $USERNAME/$IMAGE:$VERSION $USERNAME/$IMAGE:latest
docker push $USERNAME/$IMAGE:$VERSION
docker push $USERNAME/$IMAGE:latest
```
