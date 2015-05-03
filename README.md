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

POST /news

```bash
{
  "media": ["cnnindonesia.com","rmol.co"],
  "keyword": "presiden",
  "from_page" : 0,
  "page_size" : 10,
  "begin": "2015-04-01 01:00:00",
  "end": "2015-04-04 01:00:00"
}
```
Response example from server

```bash
{
    "result": [
        {
            "news": [
                {
                    "author": "Laporan: Wahyu Sabda Kuncahyo",
                    "content": "RMOL. Kuasa hukum Golkar Munas Bali, Yusril Ihza Mahendra menegaskan, kepengurusan ...",
                    "date_crawl": "2015-04-06T11:13:28.395000",
                    "location": " ",
                    "privider": "rmol.co",
                    "publish": "2015-04-01T12:52:00",
                    "title": "Yusril: Agung Cs Tak Berhak Lagi Bertindak Atas Nama DPP Golkar",
                    "url": "http://www.rmol.co/read/2015/04/01/197651/Yusril:-Agung-Cs-Tak-Berhak-Lagi-Bertindak-Atas-Nama-DPP-Golkar-"
                },
                {
                    "author": "Laporan: Ihsan Dalimunthe",
                    "content": "RMOL. Sebelum resmi digadang sebagai capres dari PDI Perjuangan, sosok Jokowi tak ...",
                    "date_crawl": "2015-04-06T11:12:46.514000",
                    "location": " ",
                    "privider": "rmol.co",
                    "publish": "2015-04-02T18:52:00",
                    "title": "Wajarlah, Ini Semua Akibat Kabinet Kerja Tanpa Mikir...",
                    "url": "http://politik.rmol.co/read/2015/04/03/197820/Wajarlah,-Ini-Semua-Akibat-Kabinet-Kerja-Tanpa-Mikir...-"
                },
                {
                    "author": "Laporan: Ujang Sunda",
                    "content": "RMOL. Jumlah staf di Kantor Staf Kepresidenan bisa mencapai 70 orang. Meski terlihat ...",
                    "date_crawl": "2015-04-06T11:14:55.216000",
                    "location": " ",
                    "privider": "rmol.co",
                    "publish": "2015-04-02T12:27:00",
                    "title": "Punya Staf 70 Orang, Luhut Panjaitan Ngomong Begini",
                    "url": "http://www.rmol.co/read/2015/04/02/197787/Punya-Staf-70-Orang,-Luhut-Panjaitan-Ngomong-Begini-"
                },
                {
                    "author": "Laporan: Ihsan Dalimunthe",
                    "content": "RMOL. Ekspektasi publik soal Jusuf Kalla yang diyakini akan bisa menjadi mentor ...",
                    "date_crawl": "2015-04-06T11:17:17.947000",
                    "location": " ",
                    "privider": "rmol.co",
                    "publish": "2015-04-03T08:45:00",
                    "title": "Ternyata, Umur JK Saja yang Lebih Banyak",
                    "url": "http://politik.rmol.co/read/2015/04/03/197875/Ternyata,-Umur-JK-Saja-yang-Lebih-Banyak-"
                },
                {
                    "author": "Laporan: Ihsan Dalimunthe",
                    "content": "RMOL. Politisi PDIP Effendi Simbolon mengaku akan mendapatkan banyak hikmah ...",
                    "date_crawl": "2015-04-06T11:14:14.357000",
                    "location": " ",
                    "privider": "rmol.co",
                    "publish": "2015-04-03T00:25:00",
                    "title": "Effendi Simbolon Tuding Istana Tak Ngerti Esensi Negara",
                    "url": "http://politik.rmol.co/read/2015/04/03/197826/Effendi-Simbolon-Tuding-Istana-Tak-Ngerti-Esensi-Negara-"
                }
            ]
        }
    ]
}
```
if not set page_size, then size set to 20.
if not set page_from, then page_from set to 0.
if not set limit, then limit set to 100.
if list media not set, then all media will proceed.