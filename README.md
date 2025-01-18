## Project Name: Stock RCI Google Sheets Integration

This project automates the calculation of the **Rank Correlation Index (RCI)** for stock data and updates a Google Sheets document with the results. It also integrates email notifications to report the success or failure of the operation.

---

### Features

- **RCI Calculation**: Computes RCI values for a given stock over a specified time period.
- **Google Sheets Integration**: Updates a designated Google Sheets document with the calculated RCI values.
- **Email Notifications**: Sends notifications upon successful or failed updates.
- **Multi-threading**: Utilizes concurrent processing for efficient data retrieval.
- **Retry Mechanism**: Retries fetching stock data up to three times in case of transient errors.

---

### Prerequisites

- Python 3.8+
- A Google Cloud Service Account with access to Google Sheets API
- A configured `config.ini` file with the following:

```ini
[DEFAULT]
CredentialsFile = path/to/credentials.json
SheetID = your_google_sheet_id

[EMAIL]
SMTPServer = smtp.your-email-provider.com
SMTPPort = 587
Username = your_email@example.com
Password = your_email_password
From = your_email@example.com
To = recipient_email@example.com
```

---

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Aryeahhh/stock-rci-gsheet.git
   ```

2. Navigate to the project directory:
   ```bash
   cd stock-rci-gsheet
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the `config.ini` file with your credentials.

---

### Usage

Run the script with the following command:
```bash
python main.py --start_date YYYY-MM-DD --end_date YYYY-MM-DD --period N
```

#### Arguments:
- `--start_date`: Start date for fetching stock data (format: YYYY-MM-DD).
- `--end_date`: End date for fetching stock data (format: YYYY-MM-DD).
- `--period`: RCI calculation period (default: 14).

Example:
```bash
python main.py --start_date 2025-01-01 --end_date 2025-01-15 --period 14
```

---

### Key Libraries Used

- **pandas_datareader**: For fetching stock data from Yahoo Finance.
- **gspread**: For interacting with Google Sheets.
- **retrying**: For implementing retry logic.
- **concurrent.futures**: For multi-threaded processing.
- **smtplib**: For sending email notifications.
- **tqdm**: For progress visualization.

---

### Project Structure

```
stock-rci-gsheet/
├── main.py                # Main script for running the application
├── config.ini             # Configuration file (user-provided)
├── requirements.txt       # List of dependencies
└── README.md              # Project documentation
```

---

### Future Enhancements

- Add support for additional stock data sources.
- Include advanced analytics like trend analysis.
- Enable scheduling for automated updates using cron jobs.

---

### License

This project is licensed under the MIT License. See the LICENSE file for details.

---

### Contributions

Contributions are welcome! Feel free to fork this repository and submit a pull request.

---

### Contact

If you have any questions or suggestions, please contact me at aryapatel0107@gmail.com.
