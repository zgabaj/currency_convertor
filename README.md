# Currency convertor:
Run web api in docker 
```
docker-compose build
docker-compose up
```
expose on loacalhost:8080 , parameters - amount, input_currency, output_currency(not required):
```
localhost:8080/currency_converter?amount=0.9&input_currency=¥&output_currency=AUD
```
