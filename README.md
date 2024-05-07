# Malware URL Lookup Exercise

This simple Python application checks that responds to GET requests where the
caller passes in a URL and the service responds with some information about that URL.

## Prerequisite

Python 3
A Browser
Available HTTP port

## How to Use

Run cisco.py on commandline:

```bash
python cisco.py
...
Starting application...
Application is running...
```
Go to your browser and test http://localhost:8080/v1/urlinfo/[url in question]

If the URL is in the blacklist:
```bash
{
  "url": "theteflacademy.co.uk",
  "safe": false,
  "message": "This URL is known to contain malware."
}
```

If the URL is in the blacklist:
```bash
{
  "url": "malicious.com",
  "safe": true,
  "message": "The URL entered is not in the blacklist"
}
```

## How to Use

Press Ctrl + C