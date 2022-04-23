# TrackOrder SMS
![VERSION](http://img.shields.io/static/v1?label=VERSION&message=1.0.0&color=informational&style=appveyor)
![Badge em Desenvolvimento](http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=yellow&style=appveyor)

TrackOrder SMS é uma web page para rastrear e monitorar encomendas. O sistema informa a cada 1 Hora caso ocorra uma atualização na encomenda.

![TrackOrder SMS](static/img/Track-Order-SMS.png)

## Funcionalidades

- Coleta dados sobre a encomenda pelo código de rasteio
- Armazena o código de rastreio e a cada 1 hora verifica se o status da encomenda atualizou, caso ocorra uma atualização envia um SMS e remove o código quando a encomenda é entregue

## Tecnologias Utilizadas

- Python
- Framework Flask
- TWILIO API
- Web Crawler
- CSS
- HTML
