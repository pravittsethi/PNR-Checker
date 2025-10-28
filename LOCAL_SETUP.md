# Local Automation Setup Guide

This guide will help you set up the PNR checker to run automatically every 2 hours on your Windows PC using Task Scheduler.

## ✅ Prerequisites

- [x] Python installed
- [x] All packages installed (`pip install -r requirements.txt`)
- [x] Gmail App Password configured in `.env`
- [x] Script tested and working locally

---

## 🚀 Step 1: Update Your `.env` File

Make sure your `.env` file has these settings:

```env
# OpenAI API Configuration
OPENAI_API_KEY=your-openai-api-key-here

# Email Configuration
SEND_EMAIL=true
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-gmail-app-password
RECEIVER_EMAIL=your-email@gmail.com
```

---

## 📝 Step 2: Test the Batch File

1. Double-click `run_pnr_checker.bat`
2. It should run the script and send you an email
3. If it works, proceed to Step 3

---

## ⏰ Step 3: Set Up Windows Task Scheduler

### Method A: Using PowerShell (Quick Setup)

1. **Open PowerShell as Administrator**:
   - Press `Win + X`
   - Click "Windows PowerShell (Admin)" or "Terminal (Admin)"

2. **Run this command** (copy and paste):

```powershell
$action = New-ScheduledTaskAction -Execute "C:\Users\pravi\Desktop\Flight Project\run_pnr_checker.bat" -WorkingDirectory "C:\Users\pravi\Desktop\Flight Project"

$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Hours 2) -RepetitionDuration ([TimeSpan]::MaxValue)

$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable

Register-ScheduledTask -TaskName "PNR Status Checker" -Action $action -Trigger $trigger -Settings $settings -Description "Checks PNR status every 2 hours and sends email notifications"
```

3. **Done!** The task is now scheduled.

---

### Method B: Using Task Scheduler GUI (Step-by-Step)

1. **Open Task Scheduler**:
   - Press `Win + R`
   - Type `taskschd.msc`
   - Press Enter

2. **Create a New Task**:
   - Click "Create Task..." (right sidebar)
   - **NOT** "Create Basic Task"

3. **General Tab**:
   - **Name**: `PNR Status Checker`
   - **Description**: `Checks PNR status every 2 hours and sends email notifications`
   - ✅ Check "Run whether user is logged on or not"
   - ✅ Check "Run with highest privileges"
   - ❌ Uncheck "Hidden"

4. **Triggers Tab**:
   - Click "New..."
   - **Begin the task**: `On a schedule`
   - **Settings**: `Daily`
   - **Recur every**: `1 days`
   - **Start**: Today's date, current time
   - ✅ Check "Repeat task every": `2 hours`
   - **For a duration of**: `Indefinitely`
   - ✅ Check "Enabled"
   - Click "OK"

5. **Actions Tab**:
   - Click "New..."
   - **Action**: `Start a program`
   - **Program/script**: 
     ```
     C:\Users\pravi\Desktop\Flight Project\run_pnr_checker.bat
     ```
   - **Start in**: 
     ```
     C:\Users\pravi\Desktop\Flight Project
     ```
   - Click "OK"

6. **Conditions Tab**:
   - ✅ Check "Start only if the following network connection is available": `Any connection`
   - ❌ Uncheck "Start the task only if the computer is on AC power"
   - ❌ Uncheck "Stop if the computer switches to battery power"

7. **Settings Tab**:
   - ✅ Check "Allow task to be run on demand"
   - ✅ Check "Run task as soon as possible after a scheduled start is missed"
   - ✅ Check "If the task fails, restart every": `10 minutes`, `3 times`
   - **If the running task does not end when requested**: `Stop the existing instance`

8. **Click "OK"**:
   - You may be prompted to enter your Windows password
   - Enter it and click "OK"

---

## 🧪 Step 4: Test the Scheduled Task

### Test Immediately:

1. In Task Scheduler, find "PNR Status Checker" in the task list
2. Right-click → "Run"
3. Check your email in 2-3 minutes
4. Check "Last Run Result" - should show `0x0` (success)

---

## 📊 Step 5: Monitor the Task

### View Task History:

1. In Task Scheduler, click on "PNR Status Checker"
2. Click the "History" tab (bottom panel)
3. You'll see every execution with timestamps

### View Logs:

- Logs are saved in the same folder
- Check for any error screenshots (`*.png`)

---

## 🔧 Troubleshooting

### Task doesn't run?

**Check 1**: Is your PC on and connected to internet?
- Task won't run if PC is off or in sleep mode

**Check 2**: Is the path correct?
- Open Task Scheduler
- Right-click task → Properties
- Check Actions tab - path should be correct

**Check 3**: Test manually first
- Double-click `run_pnr_checker.bat`
- Does it work?

### Email not sending?

**Check 1**: `.env` file has correct credentials
**Check 2**: Gmail App Password is correct (no spaces)
**Check 3**: `SEND_EMAIL=true` in `.env`

---

## ⚙️ Customization

### Change Schedule:

**Every 1 hour**:
- In Triggers → Edit
- Repeat task every: `1 hour`

**Every 4 hours**:
- In Triggers → Edit
- Repeat task every: `4 hours`

**Specific times only (e.g., 6 AM & 6 PM)**:
- Delete existing trigger
- Create two new triggers:
  - One at 6:00 AM daily
  - One at 6:00 PM daily

### Add More PNRs:

Edit `config.json`:
```json
{
  "pnr_numbers": [
    "2244293725",
    "1234567890",
    "9876543210"
  ],
  "check_interval_hours": 2,
  "email_enabled": true
}
```

### Stop the Task:

- Open Task Scheduler
- Right-click "PNR Status Checker"
- Click "Disable" (to pause) or "Delete" (to remove)

---

## 💡 Tips

### Keep PC Awake:

If you want the task to run even when you're away:
- Go to Settings → System → Power & Sleep
- Set "Sleep" to "Never" (when plugged in)

Or use this PowerShell command to prevent sleep during task:
```powershell
powercfg /change standby-timeout-ac 0
```

### View in Startup:

To see the task in Task Scheduler quickly:
1. Press `Win + R`
2. Type: `taskschd.msc`
3. Press Enter

---

## 📧 What You'll Receive

Every 2 hours, you'll get:
- ✅ Beautifully formatted HTML email
- ✅ Train details (number, name, date)
- ✅ Journey information
- ✅ Passenger status with color-coded badges
- ✅ Timestamp

---

## 🎉 You're All Set!

Your PNR checker will now run automatically every 2 hours as long as your PC is on and connected to the internet.

**Benefits over GitHub Actions:**
- ✅ Works perfectly (no IP blocks)
- ✅ Completely FREE
- ✅ No external dependencies
- ✅ Full control

**Note**: Your PC must be ON for the task to run. If you need it to run 24/7, consider using a cloud VPS or keeping your PC on.

---

## 🎮 Managing the Scheduled Task

### Using PowerShell Commands

#### **Check Task Status:**
```powershell
Get-ScheduledTask -TaskName "PNR Status Checker"
```
Shows if the task is Ready, Running, or Disabled.

#### **Check Last Run Status:**
```powershell
Get-ScheduledTaskInfo -TaskName "PNR Status Checker"
```
Shows:
- **LastRunTime** - When it last executed
- **LastTaskResult** - Success (0) or error code
- **NextRunTime** - When it will run next
- **NumberOfMissedRuns** - If any runs were missed

**Example Output:**
```
LastRunTime        : 10/29/2025 3:30:15 PM
LastTaskResult     : 0         # 0 means success
NextRunTime        : 10/29/2025 5:30:15 PM
NumberOfMissedRuns : 0
```

**Error Codes:**
- `0` or `0x0` = Success ✅
- `0x1` = Incorrect function
- `0x41301` = Task not running
- Other codes = Errors (Google the code for details)

#### **View Detailed Task Information:**
```powershell
Get-ScheduledTask -TaskName "PNR Status Checker" | Format-List *
```
Shows all task properties including triggers, actions, and settings.

#### **Disable the Task** (Pause automation):
```powershell
Disable-ScheduledTask -TaskName "PNR Status Checker"
```
The task will stop running until you enable it again. Use this if you want to temporarily pause the automation without deleting it.

**To verify it's disabled:**
```powershell
(Get-ScheduledTask -TaskName "PNR Status Checker").State
```
Should show: `Disabled`

#### **Enable the Task** (Resume automation):
```powershell
Enable-ScheduledTask -TaskName "PNR Status Checker"
```
Resumes the scheduled task. It will run at the next scheduled time.

**To verify it's enabled:**
```powershell
(Get-ScheduledTask -TaskName "PNR Status Checker").State
```
Should show: `Ready`

#### **Run Task Immediately** (Manual trigger):
```powershell
Start-ScheduledTask -TaskName "PNR Status Checker"
```
Runs the task right now, regardless of the schedule. Useful for testing.

#### **Delete the Task** (Remove completely):
```powershell
Unregister-ScheduledTask -TaskName "PNR Status Checker" -Confirm:$false
```
Permanently removes the scheduled task. You'll need to recreate it if you want to use it again.

**Warning:** This cannot be undone! If you just want to pause it temporarily, use `Disable-ScheduledTask` instead.

---

### Using Task Scheduler GUI

#### **Open Task Scheduler:**
1. Press `Win + R`
2. Type: `taskschd.msc`
3. Press Enter
4. Find "PNR Status Checker" in the task list

#### **View Task History:**
1. Select the task
2. Click the "History" tab at the bottom
3. See all executions with timestamps and results

**Common Event IDs:**
- **100** = Task Started
- **102** = Task Completed (check result code)
- **103** = Action started
- **107** = Task triggered by schedule
- **201** = Action completed successfully

#### **Disable Task (GUI):**
1. Right-click "PNR Status Checker"
2. Select "Disable"
3. Task will show as "Disabled" in the State column

#### **Enable Task (GUI):**
1. Right-click "PNR Status Checker"
2. Select "Enable"
3. Task will show as "Ready" in the State column

#### **Run Task Manually (GUI):**
1. Right-click "PNR Status Checker"
2. Select "Run"
3. Watch the status change to "Running" then back to "Ready"

#### **Delete Task (GUI):**
1. Right-click "PNR Status Checker"
2. Select "Delete"
3. Confirm the deletion

#### **Edit Task Settings (GUI):**
1. Right-click "PNR Status Checker"
2. Select "Properties"
3. Modify triggers, actions, conditions, or settings
4. Click "OK" to save

---

## 📊 Monitoring Task Performance

### **Check if Task is Running Successfully:**

```powershell
# Get the last 5 runs
Get-ScheduledTaskInfo -TaskName "PNR Status Checker" | Select-Object LastRunTime, LastTaskResult, NextRunTime, NumberOfMissedRuns
```

### **View Task Execution History (Last 7 days):**

```powershell
Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-TaskScheduler/Operational'; ID=102,201} | Where-Object {$_.Message -like "*PNR Status Checker*"} | Select-Object TimeCreated, Message -First 10
```

### **Troubleshooting Failed Runs:**

If `LastTaskResult` is not `0`:

1. **Check the batch file manually:**
   ```powershell
   cd "C:\Users\pravi\Desktop\Flight Project"
   .\run_pnr_checker.bat
   ```

2. **Look for error screenshots:**
   - Check for `*.png` files in the project folder

3. **View Task History in GUI:**
   - Open Task Scheduler
   - Select task → History tab
   - Look for errors (red X icons)

4. **Check if Python is accessible:**
   ```powershell
   python --version
   ```

5. **Verify .env file exists and is correct:**
   ```powershell
   Get-Content .env
   ```

---

## 🔄 Recreating the Task

If you delete the task and want to recreate it:

```powershell
$action = New-ScheduledTaskAction -Execute "C:\Users\pravi\Desktop\Flight Project\run_pnr_checker.bat" -WorkingDirectory "C:\Users\pravi\Desktop\Flight Project"

$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(5) -RepetitionInterval (New-TimeSpan -Hours 2)

$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable

Register-ScheduledTask -TaskName "PNR Status Checker" -Action $action -Trigger $trigger -Settings $settings -Description "Checks PNR status every 2 hours and sends email notifications"
```

---

## 📞 Need Help?

If something doesn't work:
1. Test `run_pnr_checker.bat` manually first
2. Check Task Scheduler History tab for errors
3. Look for error screenshots in the folder
4. Make sure `.env` file has correct credentials
5. Use `Get-ScheduledTaskInfo` to check the last run status

Enjoy your automated PNR status updates! 🚂✨
