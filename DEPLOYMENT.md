# Deployment Guide for Fraud Management System

This guide covers multiple deployment options for the Streamlit-based Fraud Management System.

## 📋 Table of Contents

- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Streamlit Cloud](#streamlit-cloud)
- [Heroku Deployment](#heroku-deployment)
- [Azure App Service](#azure-app-service)
- [AWS EC2](#aws-ec2)

---

## 🖥️ Local Development

### Prerequisites
- Python 3.12 or higher
- pip package manager

### Steps

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Dissertation-structured
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Access the application**
   - Open your browser and navigate to: `http://localhost:8501`

---

## 🐳 Docker Deployment

### Using Docker

1. **Build the Docker image**
   ```bash
   docker build -t aml-compliance-system .
   ```

2. **Run the container**
   ```bash
   docker run -p 8501:8501 aml-compliance-system
   ```

### Using Docker Compose

1. **Start the application**
   ```bash
   docker-compose up -d
   ```

2. **Stop the application**
   ```bash
   docker-compose down
   ```

3. **View logs**
   ```bash
   docker-compose logs -f
   ```

---

## ☁️ Streamlit Cloud

### Steps

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository, branch, and `app.py`
   - Click "Deploy"

3. **Configure secrets (if needed)**
   - In Streamlit Cloud dashboard, go to your app settings
   - Add any required secrets in the "Secrets" section

### Notes
- Free tier available
- Automatic redeployment on push to main branch
- Limited resources on free tier

---

## 🟣 Heroku Deployment

### Prerequisites
- Heroku account
- Heroku CLI installed

### Steps

1. **Login to Heroku**
   ```bash
   heroku login
   ```

2. **Create a new Heroku app**
   ```bash
   heroku create your-app-name
   ```

3. **Deploy the application**
   ```bash
   git push heroku main
   ```

4. **Scale the dyno**
   ```bash
   heroku ps:scale web=1
   ```

5. **Open the application**
   ```bash
   heroku open
   ```

### Configuration Files
- `Procfile`: Defines the command to run the app
- `runtime.txt`: Specifies Python version

---

## 🔵 Azure App Service

### Using Azure CLI

1. **Login to Azure**
   ```bash
   az login
   ```

2. **Create a resource group**
   ```bash
   az group create --name aml-rg --location eastus
   ```

3. **Create an App Service plan**
   ```bash
   az appservice plan create --name aml-plan --resource-group aml-rg --sku B1 --is-linux
   ```

4. **Create a web app**
   ```bash
   az webapp create --name your-app-name --resource-group aml-rg --plan aml-plan --runtime "PYTHON:3.12"
   ```

5. **Configure deployment**
   ```bash
   az webapp config appsettings set --name your-app-name --resource-group aml-rg --settings SCM_DO_BUILD_DURING_DEPLOYMENT=true
   ```

6. **Deploy the code**
   ```bash
   az webapp up --name your-app-name --resource-group aml-rg
   ```

### Using Docker on Azure

1. **Build and push Docker image to Azure Container Registry**
   ```bash
   az acr create --name amlregistry --resource-group aml-rg --sku Basic
   az acr build --registry amlregistry --image aml-app:v1 .
   ```

2. **Deploy container to App Service**
   ```bash
   az webapp create --name your-app-name --resource-group aml-rg --plan aml-plan --deployment-container-image-name amlregistry.azurecr.io/aml-app:v1
   ```

---

## 🟠 AWS EC2

### Steps

1. **Launch an EC2 instance**
   - Choose Ubuntu Server 22.04 LTS
   - Select instance type (t2.medium recommended)
   - Configure security group to allow port 8501

2. **Connect to your instance**
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   ```

3. **Install dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv git -y
   ```

4. **Clone and setup application**
   ```bash
   git clone <your-repo-url>
   cd Dissertation-structured
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Run with nohup (background process)**
   ```bash
   nohup streamlit run app.py --server.port=8501 --server.address=0.0.0.0 &
   ```

### Using Docker on EC2

1. **Install Docker**
   ```bash
   sudo apt install docker.io -y
   sudo systemctl start docker
   sudo systemctl enable docker
   sudo usermod -aG docker ubuntu
   ```

2. **Build and run**
   ```bash
   docker build -t aml-app .
   docker run -d -p 8501:8501 aml-app
   ```

---

## 🔐 Environment Variables & Secrets

For production deployments, consider setting:

```bash
# Streamlit configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true

# Application settings
PYTHONUNBUFFERED=1
```

---

## 🔍 Monitoring & Logs

### Docker logs
```bash
docker logs -f container-name
```

### Heroku logs
```bash
heroku logs --tail
```

### Azure logs
```bash
az webapp log tail --name your-app-name --resource-group aml-rg
```

---

## 🛠️ Troubleshooting

### Port already in use
```bash
# Find process using port 8501
lsof -ti:8501
# Kill the process
kill -9 <PID>
```

### Memory issues
- Increase instance size
- Optimize data loading (use chunking)
- Clear cache regularly

### SSL/HTTPS issues
- For production, use a reverse proxy (nginx)
- Enable SSL certificates (Let's Encrypt)

---

## 📞 Support

For deployment issues:
1. Check application logs
2. Verify all dependencies are installed
3. Ensure correct Python version (3.12+)
4. Check firewall/security group settings

---

## 📝 Additional Notes

- **Data Security**: Never commit sensitive data or credentials
- **Scalability**: Consider load balancing for high traffic
- **Backup**: Regularly backup your data and configurations
- **Updates**: Keep dependencies updated for security patches

---

**Version**: 1.0.0  
**Last Updated**: January 2026
