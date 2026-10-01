# Payment Verifier

A Python program that verifies payment transactions from Telebirr and Bank of Abyssinia and stores verified transactions in an SQLite database.

## Features

* Telebirr payment verification
* Bank of Abyssinia payment verification
* Duplicate invoice detection
* SQLite transaction storage
* Transaction database viewer
* Web scraping with BeautifulSoup
* Selenium automation for Bank of Abyssinia

## Requirements

* Python 3
* Google Chrome
* Internet connection

Install the required packages:

```bash
pip install -r requirements.txt
```

## Run

```bash
python paymentverifier.py
```

The program will create `transactions.db` automatically when it is first run.

## Project Structure

```text
payment-verifier/
├── paymentverifier.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Notes

The payment and account values used by the program are configured through environment variables. Real transaction databases and sensitive payment information should not be committed to the repository.

This project was built to automate payment verification and prevent the same invoice from being used more than once.
