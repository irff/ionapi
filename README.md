# Ion Scrapper API

## API Specification

POST /mediashare/

```bash
{
  "media": ["cnnindonesia.com","rmol.com"],
  "keyword": "presiden",
  "begin": "2015-04-01 01:00:00",
  "end": "2015-04-04 01:00:00"
}
```

Response example from server

```bash
{
    "result": [
        {
            "date": "2015-04-01",
            "media": {
                "cnnindonesia.com": 0,
                "rmol.com": 0
            }
        },
        {
            "date": "2015-04-02",
            "media": {
                "cnnindonesia.com": 0,
                "rmol.com": 0
            }
        },
        {
            "date": "2015-04-03",
            "media": {
                "cnnindonesia.com": 0,
                "rmol.com": 0
            }
        },
        {
            "date": "2015-04-04",
            "media": {
                "cnnindonesia.com": 0,
                "rmol.com": 0
            }
        }
    ]
}
```

POST /mediashare/summary

```bash
{
  "media": ["cnnindonesia.com","rmol.co"],
  "keyword": "presiden",
  "begin": "2015-04-01 01:00:00",
  "end": "2015-04-04 01:00:00"
}
```
Response example from server

```bash
{
    "result": [
        {
            "media": {
                "cnnindonesia.com": 0,
                "rmol.co": 9
            }
        }
    ]
}
```

POST /keyopinionleader/

```bash
{
  "media": ["cnnindonesia.com","rmol.co"],
  "name": ["jokowi","prabowo"],
  "keyword": "presiden",
  "begin": "2015-04-01 01:00:00",
  "end": "2015-04-04 01:00:00"
}
```
Response example from server

```bash
{
    "result": [
        {
            "jokowi": 5,
            "prabowo": 0
        }
    ]
}
```

POST /wordfrequency

```bash
{
  "media": ["cnnindonesia.com","rmol.co"],
  "limit" : 20,
  "keyword": "presiden",
  "begin": "2015-04-01 01:00:00",
  "end": "2015-04-04 01:00:00"
}  
```
Response example from server

```bash
{
    "result": [
        {
            "words": {
                "2": 8,
                "4": 8,
                "ada": 6,
                "adalah": 4,
                "akan": 4,
                "dalam": 6,
                "dan": 9,
                "dari": 7,
                "dengan": 7,
                "di": 9,
                "hanya": 5,
                "ini": 9,
                "itu": 5,
                "jakarta": 5,
                "kamis": 7,
                "karena": 6,
                "kata": 6,
                "rmol": 9,
                "saat": 6,
                "yang": 9
            }
        }
    ]
}
```
if not set limit, then limit set to 100.

if list media not set, then all media will proceed.