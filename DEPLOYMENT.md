# 🚀 Deployment Guide - PNR Status Checker

This guide will help you deploy the automated PNR checker that runs every 2 hours on GitHub Actions and sends email notifications.

## 📋 Prerequisites

Before deploying, you need:

1. ✅ GitHub account (already done)
2. ✅ Code pushed to repository (already done)
3. 📧 Gmail account (or any SMTP email)
4. 🔑 OpenAI API key (you already have this)

---

## 🔧 Step 1: Set Up Gmail App Password

Since GitHub Actions will send emails on your behalf, you need to create an **App Password** for Gmail:

### For Gmail:

1. Go to your Google Account: https://myaccount.google.com/
2. Click on **Security** (left sidebar)
3. Under "How you sign in to Google", click **2-Step Verification**
   - If not enabled, enable it first
4. Scroll down and click **App passwords**
5. Select app: **Mail**
6. Select device: **Other** (type "PNR Checker")
7. Click **Generate**
8. **Copy the 16-character password** (you'll need this in Step 2)

> ⚠️ **Important**: This is different from your regular Gmail password!

---

## 🔐 Step 2: Add Secrets to GitHub Repository

GitHub Secrets keep your sensitive information secure. Here's how to add them:

1. Go to your repository: https://github.com/pravittsethi/PNR-Checker

2. Click on **Settings** tab (top right)

3. In the left sidebar, click **Secrets and variables** → **Actions**

4. Click **New repository secret** button

5. Add the following secrets one by one:

### Secret 1: OPENAI_API_KEY
- **Name**: `OPENAI_API_KEY`
- **Value**: Your OpenAI API key (starts with `sk-proj-...`)
- Click **Add secret**

### Secret 2: SENDER_EMAIL
- **Name**: `SENDER_EMAIL`
- **Value**: Your Gmail address (e.g., `youremail@gmail.com`)
- Click **Add secret**

### Secret 3: SENDER_PASSWORD
- **Name**: `SENDER_PASSWORD`
- **Value**: The 16-character App Password you generated in Step 1
- Click **Add secret**

### Secret 4: RECEIVER_EMAIL
- **Name**: `RECEIVER_EMAIL`
- **Value**: Email where you want to receive notifications (can be the same as SENDER_EMAIL)
- Click **Add secret**

---

## 📝 Step 3: Configure PNR Numbers

Edit the `config.json.example` file and save it as `config.json`:

```json
{
  "pnr_numbers": [
    "2244293725",
    "1234567890"
  ],
  "check_interval_hours": 2,
  "email_enabled": true
}
```

**Note**: The actual `config.json` is already in your repository. You can edit it to add more PNR numbers.

---

## 🎯 Step 4: Enable GitHub Actions

1. Go to your repository: https://github.com/pravittsethi/PNR-Checker

2. Click on the **Actions** tab

3. If prompted, click **I understand my workflows, go ahead and enable them**

4. You should see the workflow: **PNR Status Checker**

---

## ⏰ Step 5: Test the Workflow

Before waiting 2 hours, test it manually:

1. Go to **Actions** tab
2. Click on **PNR Status Checker** workflow (left sidebar)
3. Click **Run workflow** button (right side)
4. Click the green **Run workflow** button
5. Wait 2-3 minutes and check your email!

---

## 📧 What You'll Receive

Every 2 hours (or when you manually trigger), you'll receive a beautifully formatted HTML email with:

✅ Train details (number, name, date, class)  
✅ Journey information (from, to, boarding point)  
✅ Passenger status (booking and current status)  
✅ Color-coded status badges (Confirmed/RAC/Waiting)  
✅ Timestamp of when it was checked  

---

## 🔄 Scheduling Options

The workflow is currently set to run **every 2 hours**. To change this, edit `.github/workflows/pnr_checker.yml`:

### Every 4 hours:
```yaml
schedule:
  - cron: '0 */4 * * *'
```

### Every 6 hours:
```yaml
schedule:
  - cron: '0 */6 * * *'
```

### Twice daily (6 AM & 6 PM IST):
```yaml
schedule:
  - cron: '30 0,12 * * *'  # 6 AM & 6 PM IST = 00:30 & 12:30 UTC
```

### Every hour:
```yaml
schedule:
  - cron: '0 * * * *'
```

> **Note**: GitHub Actions times are in UTC. IST = UTC + 5:30

---

## 🐛 Troubleshooting

### Email not sending?

**Check 1**: Verify Gmail App Password
- Make sure you used the App Password, not your regular password
- The App Password should be 16 characters without spaces

**Check 2**: Verify Secrets
- Go to Settings → Secrets and variables → Actions
- Make sure all 4 secrets are added correctly

**Check 3**: Check 2-Step Verification
- Gmail App Passwords require 2-Step Verification to be enabled

### Workflow failing?

1. Go to **Actions** tab
2. Click on the failed run
3. Click on the **check-pnr** job
4. Expand the steps to see error details
5. Check if screenshots were uploaded (under Artifacts)

### CAPTCHA not solving?

- OpenAI API key might be invalid
- API might have rate limits
- The workflow will automatically retry on the next run

### Want to check logs?

1. Go to **Actions** tab
2. Click on any workflow run
3. View detailed logs for each step

---

## 💰 Cost Estimation

### GitHub Actions: **FREE**
- 2,000 minutes/month on free tier
- Each run takes ~2-3 minutes
- 12 runs/day × 3 min = 36 min/day
- Monthly: ~1,080 minutes (well within free tier!)

### OpenAI API: **~$14-15/month**
- Each CAPTCHA solve: ~$0.001-0.002
- 12 checks/day × $0.002 = $0.024/day
- Monthly: ~$0.72/month (very affordable!)

### Gmail: **FREE**
- Unlimited emails

**Total: ~$0.72-1/month** (OpenAI only)

---

## 🎉 You're All Set!

Your PNR checker will now run automatically every 2 hours and send you email notifications. You can:

- ✅ Add more PNR numbers in `config.json`
- ✅ Change the schedule in the workflow file
- ✅ Manually trigger runs anytime from Actions tab
- ✅ Check logs and screenshots if something fails

---

## 📞 Need Help?

If you encounter any issues:

1. Check the Actions tab for error logs
2. Verify all secrets are set correctly
3. Make sure Gmail App Password is generated correctly
4. Test locally first: `python pnr_checker.py`

---

## 🔄 Updating the Code

When you make changes:

```powershell
git add .
git commit -m "Updated configuration"
git push origin main
```

The next scheduled run will use your updated code automatically!

---

## 🛑 Pausing the Automation

To temporarily stop the automated checks:

1. Go to **Actions** tab
2. Click **PNR Status Checker** (left sidebar)
3. Click the **•••** menu (top right)
4. Click **Disable workflow**

To resume, click **Enable workflow**

---

Enjoy your automated PNR status updates! 🚂✨
