# Update Phishing Monitor on EC2

Follow these steps to update your deployed application with the latest code from GitHub.

## 1. Connect to your EC2 Instance
Open your terminal (or PowerShell on Windows) and SSH into your instance:
```bash
ssh -i "path/to/your-key.pem" ubuntu@your-ec2-public-ip
```
*Replace `path/to/your-key.pem` with your actual key file path and `your-ec2-public-ip` with your instance's IP address.*

## 2. Navigate to Project Directory
```bash
cd phishing_monitoring
```

## 3. Pull Latest Changes
Get the updates you just pushed to GitHub:
```bash
git pull origin main
```

## 4. Update Dependencies
In case `requirements.txt` changed:
```bash
pip install -r requirements.txt
```

## 5. Retrain the Model
**IMPORTANT**: Since the code for feature extraction changed, you MUST retrain the model on the server so it learns the new features.
```bash
python3 src/train.py
```

## 6. Restart the Application
You need to restart the running process for changes to take effect.

**Option A: If running with `nohup` (Background Process)**
1.  Find the Process ID (PID):
    ```bash
    ps aux | grep app.py
    ```
2.  Kill the old process:
    ```bash
    kill <PID>
    ```
    *(Replace `<PID>` with the number found in the previous step)*
3.  Start the new process:
    ```bash
    nohup python3 src/web/app.py > app.log 2>&1 &
    ```

**Option B: If running as a Systemd Service**
```bash
sudo systemctl restart phishing-monitor
```
