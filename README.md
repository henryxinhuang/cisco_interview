# Malware URL Lookup Exercise

This simple Python application checks that responds to GET requests where the
caller passes in a URL and the service responds with some information about that URL.

## Prerequisite

Python 3 <br>
A Browser <br>
Available HTTP port

## How to Use

Run cisco.py on commandline:

```bash
python cisco.py
...
Starting application...
Application is running...
```
Go to your browser and test http://localhost:8080/v1/urlinfo/[url_in_question]

If the URL is in the blacklist, the response:
```bash
{
  "url": "theteflacademy.co.uk",
  "safe": false,
  "message": "This URL is known to contain malware."
}
```

If the URL is in the blacklist, the response:
```bash
{
  "url": "malicious.com",
  "safe": true,
  "message": "The URL entered is not in the blacklist"
}
```

## How to Exit

Press Ctrl + C

## Test 

```bash
----------------------------------------------------------------------
Ran 3 tests in 7.672s

OK
Finished running tests!
```

## Considerations Q&A 

The size of the URL list could grow infinitely, how might you scale this beyond the
memory capacity of the system?

*My answer: We could store long URL in partitions and look them up using hash values*

The number of requests may exceed the capacity of this system, how might you solve
that?

*My answer: I implemented throttling. High availability like K8s would also be useful*

What are some strategies you might use to update the service with new URLs? Updates
may be as many as 5000 URLs a day with updates arriving every 10 minutes

*My answer: We can isolate the LUT to be on Apache Cassandra or AWS DynamoDB for easy update*