# PNR Status Checker

Automated system to check Indian Railway PNR status using Selenium and OpenAI API for CAPTCHA solving.

## Features
- Automated browser navigation to Indian Railways PNR enquiry page
- Automatic CAPTCHA solving using OpenAI Vision API (GPT-4o)
- Result extraction and display
- Retry mechanism for CAPTCHA failures
- Screenshot capture on errors

## Prerequisites
- Python 3.8 or higher
- OpenAI API key (get from https://platform.openai.com/api-keys)
- Chrome browser installed

## Installation

1. Install required packages:
```powershell
pip install -r requirements.txt
```

2. Set your OpenAI API key:
```powershell
$env:OPENAI_API_KEY = "your-api-key-here"
```

Or for persistent setup, add to your PowerShell profile.

## Usage

### Method 1: Direct Execution
```powershell
python pnr_checker.py
```

### Method 2: As a Module
```python
from pnr_checker import PNRChecker
import os

api_key = os.getenv('OPENAI_API_KEY')
checker = PNRChecker(api_key)
result = checker.check_pnr("2244293725")
print(result)
```

## Configuration

Edit the PNR number in `pnr_checker.py`:
```python
pnr_number = "2244293725"  # Change this to your PNR
```

## How It Works

1. **Browser Automation**: Opens Chrome browser and navigates to Indian Railways website
2. **PNR Entry**: Enters the PNR number automatically
3. **CAPTCHA Detection**: Waits for CAPTCHA modal to appear
4. **Image Capture**: Screenshots the CAPTCHA image
5. **AI Solving**: Sends image to OpenAI GPT-4o to solve the math equation
6. **Answer Submission**: Enters the answer and submits
7. **Result Extraction**: Captures and displays the PNR status

## Troubleshooting

- **CAPTCHA fails**: The script retries up to 3 times automatically
- **Browser doesn't open**: Make sure Chrome is installed
- **API errors**: Check your OpenAI API key and credits
- **Screenshots**: Error screenshots are saved automatically for debugging

## Notes

- The browser window will stay open briefly to show results
- Screenshots are saved on errors for debugging
- Respects website terms of service - don't abuse the system

## Cost Estimation

Each CAPTCHA solve costs approximately $0.001-0.002 (OpenAI API pricing)
