# Ion Scrapper API

## API Specification

POST /mediashare/

```bash
--data (JSON)
    media=[ALL|Kompas|Inilah|CNN]
    keywords=String
    begin=timestamp
    end=timestamp
```

Response example from server

```bash
{
    [
        'date':'2015-01-01',
        'data': [
                    'kompas':'100',
                    'inilah':'10',
                    'cnn':'88',
                ]
    ],
    [
        'date':'2015-01-01',
        'data': [
                    'kompas':'100',
                    'inilah':'10',
                    'cnn':'88',
                ]
    ]
}
```

POST /mediashare/summary

```bash
--data (JSON)
    media=[all/media_name]
    keywords=String
    begin=timestamp
    end=timestamp
```
Response example from server

```bash
{
    [
        'kompas':'100',
        'inilah':'1000',
        'detik':'113',
    ]   
}
```

POST /keyopinionleader/

```bash
--data (JSON)
    name=[Jokowi|Prabowo|All]
    media=[Kompas|Inilah|All]
    keywords=String
    begin=timestamp
    end=timestamp
```
Response example from server

```bash
{
    [
        'Jokowi':'100',
        'Prabowo':'1000',
        'Badrodin Haiti':'113',
        'Susilo Bambang':'113',
        'Megawati Soekarnoputri':'113',
    ]   
}
```

POST /wordfrequency

```bash
--data (JSON)
    name=[Jokowi|Prabowo|All]
    media=[Kompas|Inilah|All]
    keywords=[key1,key2]
    begin=timestamp
    end=timestamp   
```
Response example from server

```bash
{
        [
            'saya':'100',
            'mengapa':'1000',
            'dimana':'113',
            'bahkan':'113',
            'kapan':'113',
        ]   
}
```