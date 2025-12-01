---
description: Complete steps to deploy the phishing monitoring project on AWS EC2
---

# Deploy Phishing Monitoring System to AWS EC2

Follow these steps to deploy your Flask-based phishing detection monitoring system on an AWS EC2 instance.

## Prerequisites
- AWS account with EC2 access
- EC2 instance running Ubuntu (20.04 or 22.04)
- SSH access to your EC2 instance
- Security group allowing inbound traffic on port 5000 (or 80/443)

## Step 1: Connect to Your EC2 Instance
```bash
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

## Step 2: Update System and Install Dependencies
// turbo-all
```bash
# Update package list
sudo apt update

# Install required system packages
sudo apt install software-properties-common git -y

# Add deadsnakes PPA for Python 3.11
sudo add-apt-repository ppa:deadsnakes/ppa -y

# Update package list again
sudo apt update

# Install Python 3.11 and related packages
sudo apt install python3.11 python3.11-venv python3.11-dev python3-pip -y
```

## Step 3: Clone Your Repository
```bash
# Clone your phishing monitoring repository
git clone https://github.com/Chinmayabs224/phishing_monitoring.git

# Navigate to project directory
cd phishing_monitoring
```

## Step 4: Upload Dataset (if not in repository)
If your dataset is not in the repository, upload it from your local machine:

**On your local machine (Windows PowerShell):**
```powershell
scp -i your-key.pem d:\CLi\phishing\data\cybersecurity_extraction.csv ubuntu@your-ec2-public-ip:~/phishing_monitoring/data/
```

## Step 5: Set Up Python Virtual Environment
```bash
# Create virtual environment with Python 3.11
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

## Step 6: Install Python Dependencies
```bash
# Install all required packages
pip install -r requirements.txt
```

## Step 7: Verify Data Files Exist
```bash
# Check if dataset exists
ls -lh data/cybersecurity_extraction.csv

# Check if reference data exists
ls -lh models/reference_data.csv
```

## Step 8: Run the Flask Application
```bash
# Navigate to the web directory
cd src/web

# Run the Flask app (development mode)
python app.py
```

The application will start on `http://0.0.0.0:5000`

## Step 9: Access Your Application
Open your browser and navigate to:
```
http://your-ec2-public-ip:5000
```

## Step 10: Run in Production (Optional)
For production deployment, use Gunicorn:

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn (from project root)
gunicorn -w 4 -b 0.0.0.0:5000 src.web.app:app
```

## Step 11: Keep Application Running (Background Process)
To keep the application running after you disconnect:

```bash
# Install screen
sudo apt install screen -y

# Start a new screen session
screen -S phishing-app

# Run your application
cd ~/phishing_monitoring/src/web
source ../../venv/bin/activate
python app.py

# Detach from screen: Press Ctrl+A, then D
# Reattach later: screen -r phishing-app
```

## Security Group Configuration
Make sure your EC2 security group allows inbound traffic:
- **Port 22**: SSH access
- **Port 5000**: Flask application (or 80/443 for production)

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 5000
sudo lsof -i :5000

# Kill the process
sudo kill -9 <PID>
```

### Permission Issues
```bash
# Make sure you're in the virtual environment
source venv/bin/activate

# Check Python version
python --version
```

### Application Not Accessible
- Check security group rules in AWS Console
- Verify the application is running: `ps aux | grep python`
- Check application logs for errors

## Stopping the Application
```bash
# If running in foreground: Ctrl+C

# If running in screen:
screen -r phishing-app
# Then Ctrl+C

# If running with Gunicorn:
pkill gunicorn
```
