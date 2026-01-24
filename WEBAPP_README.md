# Fraud Management System - Streamlit Web Application

## �️ Technologies Used

- **Streamlit** (v1.30.0+) - Interactive web application framework
- **Python** (v3.8+) - Runtime environment
- **pandas** (v2.0.0+) - Data manipulation and analysis
- **scikit-learn** (v1.3.0+) - Machine learning models
- **matplotlib** & **seaborn** - Data visualization
- **Docker** - Containerization for deployment

## �🚀 Quick Start

### Option 1: Using the Start Script (Easiest)

**Windows:**
```bash
start_app.bat
```

**Linux/Mac:**
```bash
chmod +x start_app.sh
./start_app.sh
```

### Option 2: Manual Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   streamlit run app.py
   ```

3. **Access the application:**
   - Open your browser and go to: `http://localhost:8501`

---

## 📱 Features

- **🏠 Home**: Overview of system capabilities
- **📊 Data Upload & Analysis**: Upload CSV files or use sample data
- **🔍 Transaction Risk Prediction**: Real-time risk assessment for individual transactions
- **👥 Customer Risk Profiles**: View and analyze customer risk profiles
- **📈 Dashboard & Reports**: Comprehensive visualizations and downloadable reports
- **ℹ️ About**: System information and documentation

---

## 🎯 How to Use

1. **Navigate to "Data Upload & Analysis"**
   - Upload your transaction CSV file, or
   - Use the sample data option

2. **Load and Analyze Data**
   - Click "Load Data" to import your dataset
   - Click "Run Complete Analysis" to process the data
   - Wait for the analysis to complete (may take a few minutes)

3. **Explore Results**
   - View executive summary with key metrics
   - Check dashboards and visualizations
   - Download reports (CSV and images)

4. **Test Individual Transactions**
   - Go to "Transaction Risk Prediction"
   - Enter transaction details
   - Get instant risk assessment

5. **Review Customer Profiles**
   - Navigate to "Customer Risk Profiles"
   - Search for specific accounts
   - Filter and sort by risk level

---

## 🐳 Docker Deployment

### Quick Deploy with Docker

```bash
# Build the image
docker build -t aml-app .

# Run the container
docker run -p 8501:8501 aml-app
```

### Using Docker Compose

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f
```

---

## ☁️ Cloud Deployment

### Streamlit Cloud (Free)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy!

### Heroku

```bash
heroku login
heroku create your-app-name
git push heroku main
```

### AWS/Azure/GCP

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

---

## 📋 Requirements

- Python 3.12 or higher
- 2GB RAM minimum (4GB recommended)
- Modern web browser (Chrome, Firefox, Safari, Edge)

---

## 🔧 Configuration

Streamlit configuration is stored in `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#3B82F6"
backgroundColor = "#FFFFFF"

[server]
port = 8501
enableCORS = false
```

---

## 📊 Expected Input Format

Your CSV file should contain these columns:

- `Time`: Transaction time (HH:MM:SS)
- `Date`: Transaction date (YYYY-MM-DD)
- `Sender_account`: Sender account ID
- `Receiver_account`: Receiver account ID
- `Amount`: Transaction amount
- `Payment_currency`: Currency code (e.g., USD)
- `Received_currency`: Currency code (e.g., EUR)
- `Sender_bank_location`: Location code (e.g., US-NY)
- `Receiver_bank_location`: Location code (e.g., UK-LON)
- `Payment_type`: Payment method (Wire, ACH, etc.)
- `Is_laundering`: Label (0 or 1) - if available

---

## 🎨 Screenshots

The application includes:

- Interactive data upload interface
- Real-time transaction risk prediction
- Comprehensive dashboards with multiple visualizations
- Customer risk profile analysis
- Downloadable reports and charts

---

## 🛠️ Troubleshooting

### Port already in use
```bash
# Find and kill process on port 8501
# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8501 | xargs kill -9
```

### Module not found
```bash
pip install -r requirements.txt --upgrade
```

### Data loading issues
- Ensure CSV file has the correct format
- Check that column names match expected format
- Try using sample data first to verify system works

---

## 📞 Support

For issues or questions:
1. Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment help
2. Review error messages in the terminal
3. Verify all dependencies are installed

---

## 📄 Academic Project

This project is submitted as part of the **Final Semester Dissertation Project** for the **Master of Technology (MTech) in Artificial Intelligence and Machine Learning (AIML)** degree at **Birla Institute of Technology and Science (BITS), Pilani**.

**Institution**: BITS Pilani  
**Program**: MTech in AIML  
**Project Type**: Dissertation Project  
**Academic Year**: 2025-2026

---

**Version**: 1.0.0  
**Created**: January 2026
