"""
Email Notification Module for PNR Status
Sends formatted HTML emails with journey and passenger details
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os


class EmailNotifier:
    def __init__(self, smtp_server="smtp.gmail.com", smtp_port=587):
        """Initialize email notifier with SMTP settings"""
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')
        self.receiver_email = os.getenv('RECEIVER_EMAIL')
        
    def create_html_email(self, pnr_number, journey_data, passenger_data):
        """Create HTML formatted email with PNR status"""
        
        html = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    padding: 20px;
                }}
                .container {{
                    background-color: white;
                    border-radius: 10px;
                    padding: 30px;
                    max-width: 800px;
                    margin: 0 auto;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 8px;
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .pnr-number {{
                    font-size: 24px;
                    font-weight: bold;
                    color: #ffd700;
                }}
                .section {{
                    margin-bottom: 30px;
                }}
                .section-title {{
                    font-size: 20px;
                    font-weight: bold;
                    color: #667eea;
                    margin-bottom: 15px;
                    border-bottom: 2px solid #667eea;
                    padding-bottom: 5px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 10px;
                }}
                th {{
                    background-color: #667eea;
                    color: white;
                    padding: 12px;
                    text-align: left;
                    font-weight: bold;
                }}
                td {{
                    padding: 12px;
                    border-bottom: 1px solid #ddd;
                }}
                tr:nth-child(even) {{
                    background-color: #f9f9f9;
                }}
                .info-row {{
                    display: flex;
                    justify-content: space-between;
                    padding: 10px 0;
                    border-bottom: 1px solid #eee;
                }}
                .info-label {{
                    font-weight: bold;
                    color: #555;
                }}
                .info-value {{
                    color: #333;
                }}
                .status-badge {{
                    display: inline-block;
                    padding: 5px 15px;
                    border-radius: 20px;
                    font-weight: bold;
                    font-size: 14px;
                }}
                .status-confirmed {{
                    background-color: #4CAF50;
                    color: white;
                }}
                .status-waiting {{
                    background-color: #FF9800;
                    color: white;
                }}
                .status-rac {{
                    background-color: #2196F3;
                    color: white;
                }}
                .footer {{
                    text-align: center;
                    color: #888;
                    margin-top: 30px;
                    font-size: 12px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                }}
                .timestamp {{
                    color: #888;
                    font-size: 14px;
                    text-align: right;
                    margin-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚂 Indian Railways PNR Status</h1>
                    <div class="pnr-number">PNR: {pnr_number}</div>
                </div>
        """
        
        # Journey Details Section
        if journey_data:
            html += """
                <div class="section">
                    <div class="section-title">📅 Journey Details</div>
                    <table>
                        <tr>
                            <th>Train Number</th>
                            <th>Train Name</th>
                            <th>Boarding Date</th>
                            <th>Class</th>
                        </tr>
                        <tr>
            """
            html += f"""
                            <td>{journey_data['train_number']}</td>
                            <td>{journey_data['train_name']}</td>
                            <td>{journey_data['boarding_date']}</td>
                            <td>{journey_data['class']}</td>
                        </tr>
                    </table>
                    
                    <div style="margin-top: 20px;">
                        <div class="info-row">
                            <span class="info-label">From:</span>
                            <span class="info-value">{journey_data['from']}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">To:</span>
                            <span class="info-value">{journey_data['to']}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Reserved Upto:</span>
                            <span class="info-value">{journey_data['reserved_upto']}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Boarding Point:</span>
                            <span class="info-value">{journey_data['boarding_point']}</span>
                        </div>
                    </div>
                </div>
            """
        
        # Passenger Details Section
        if passenger_data:
            html += """
                <div class="section">
                    <div class="section-title">👥 Passenger Details</div>
                    <table>
                        <tr>
                            <th>Passenger</th>
                            <th>Booking Status</th>
                            <th>Current Status</th>
                        </tr>
            """
            
            for passenger in passenger_data:
                current_status = passenger['current_status']
                status_class = 'status-waiting'
                if 'CNF' in current_status or 'Confirmed' in current_status:
                    status_class = 'status-confirmed'
                elif 'RAC' in current_status:
                    status_class = 'status-rac'
                
                html += f"""
                        <tr>
                            <td>{passenger['passenger_no']}</td>
                            <td>{passenger['booking_status']}</td>
                            <td><span class="status-badge {status_class}">{current_status}</span></td>
                        </tr>
                """
            
            html += """
                    </table>
                </div>
            """
        
        # Footer
        timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        html += f"""
                <div class="timestamp">
                    ⏰ Checked on: {timestamp}
                </div>
                
                <div class="footer">
                    <p>This is an automated notification from PNR Status Checker</p>
                    <p>Powered by GitHub Actions & OpenAI</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def send_email(self, subject, html_content):
        """Send email with HTML content"""
        try:
            # Validate credentials
            if not all([self.sender_email, self.sender_password, self.receiver_email]):
                print("Error: Email credentials not configured")
                print("Please set SENDER_EMAIL, SENDER_PASSWORD, and RECEIVER_EMAIL environment variables")
                return False
            
            # Create message
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = self.sender_email
            message['To'] = self.receiver_email
            
            # Attach HTML content
            html_part = MIMEText(html_content, 'html')
            message.attach(html_part)
            
            # Connect and send
            print(f"Connecting to {self.smtp_server}:{self.smtp_port}...")
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                print("Logging in...")
                server.login(self.sender_email, self.sender_password)
                print(f"Sending email to {self.receiver_email}...")
                server.send_message(message)
            
            print("✅ Email sent successfully!")
            return True
            
        except smtplib.SMTPAuthenticationError:
            print("❌ Email authentication failed!")
            print("For Gmail, you need to use an App Password:")
            print("1. Go to https://myaccount.google.com/apppasswords")
            print("2. Generate a new app password")
            print("3. Use that password in SENDER_PASSWORD")
            return False
            
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False
    
    def send_pnr_status(self, pnr_number, journey_data, passenger_data):
        """Send PNR status email"""
        
        # Determine status for subject line
        status_summary = "Status Update"
        if passenger_data and len(passenger_data) > 0:
            current_status = passenger_data[0]['current_status']
            if 'CNF' in current_status or 'Confirmed' in current_status:
                status_summary = "✅ Confirmed"
            elif 'RAC' in current_status:
                status_summary = "🔄 RAC"
            elif 'WL' in current_status:
                status_summary = "⏳ Waiting List"
        
        subject = f"🚂 PNR {pnr_number} - {status_summary}"
        
        # Create HTML content
        html_content = self.create_html_email(pnr_number, journey_data, passenger_data)
        
        # Send email
        return self.send_email(subject, html_content)
    
    def send_error_notification(self, pnr_number, error_message):
        """Send error notification email"""
        subject = f"❌ PNR {pnr_number} - Check Failed"
        
        html_content = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    padding: 20px;
                }}
                .container {{
                    background-color: #fff3cd;
                    border-left: 5px solid #ff9800;
                    padding: 20px;
                    border-radius: 5px;
                }}
                h2 {{
                    color: #d32f2f;
                }}
                .error-box {{
                    background-color: #ffebee;
                    border: 1px solid #ef5350;
                    padding: 15px;
                    border-radius: 5px;
                    margin-top: 15px;
                    font-family: monospace;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>⚠️ PNR Status Check Failed</h2>
                <p><strong>PNR Number:</strong> {pnr_number}</p>
                <p><strong>Time:</strong> {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</p>
                <div class="error-box">
                    <strong>Error:</strong><br>
                    {error_message}
                </div>
                <p style="margin-top: 20px; color: #666;">
                    The system will automatically retry on the next scheduled run.
                </p>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(subject, html_content)


# Test function
if __name__ == "__main__":
    # Test with sample data
    notifier = EmailNotifier()
    
    sample_journey = {
        'train_number': '12053',
        'train_name': 'ASR JANSHATABDI',
        'boarding_date': '5-11-2025',
        'from': 'HW',
        'to': 'ASR',
        'reserved_upto': 'ASR',
        'boarding_point': 'HW',
        'class': 'CC'
    }
    
    sample_passengers = [
        {
            'passenger_no': 'Passenger 1',
            'booking_status': 'WL/22/GN',
            'current_status': 'WL/12',
            'coach_position': ''
        },
        {
            'passenger_no': 'Passenger 2',
            'booking_status': 'WL/23/GN',
            'current_status': 'WL/13',
            'coach_position': ''
        }
    ]
    
    notifier.send_pnr_status('2244293725', sample_journey, sample_passengers)
