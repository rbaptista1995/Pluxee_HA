# Pluxee Home Assistant Integration (Portugal)

[PT-PT](#pt-pt) | [ENG-US](#eng-us)

---

## PT-PT

Integração não oficial para o Home Assistant que permite consultar dados do cartão Pluxee (Portugal), incluindo saldo e transações recentes, através da API da plataforma de consumidores.

A fonte de dados desta integração é a [Pluxee Portugal](https://www.pluxee.pt/).

O autor deste projeto rejeita categoricamente qualquer responsabilidade sobre o saldo do cartão e outros dados apresentados pela integração.

### Funcionalidades

- Autenticação na conta Pluxee do utilizador.
- Sensor com informação de saldo do cartão.
- Consulta periódica de dados em cloud (`cloud_polling`).
- Configuração via interface do Home Assistant (Config Flow).

### Instalação via HACS

1. Adicione este repositório como **Custom repository** do tipo **Integration**.
2. Instale a integração **PLUXEE card integration**.
3. Confirme que os ficheiros foram instalados em:
   - `/config/custom_components/pluxee`
4. Reinicie o Home Assistant.
5. Vá a **Definições > Dispositivos e Serviços > Adicionar integração** e procure por **Pluxee**.

### Suporte

Se encontrar problemas, abra uma issue neste repositório.

### Créditos

Aplicação desenvolvida com base na integração do @ruidias:
https://github.com/netsoft-ruidias/ha-custom-component-myedenred

### Aviso legal

Este é um projeto pessoal e não está, de forma alguma, afiliado, patrocinado ou aprovado pela [Pluxee Portugal](https://www.pluxee.pt/).

Todos os nomes de produtos, marcas registadas e imagens neste repositório são propriedade dos respetivos titulares e são utilizados apenas para fins de identificação.

---

## ENG-US

Unofficial Home Assistant integration that lets users retrieve Pluxee (Portugal) card data, including balance and recent transactions, through the consumer platform API.

The data source for this integration is [Pluxee Portugal](https://www.pluxee.pt/).

The author of this project explicitly disclaims any responsibility for the card balance and any other data shown by the integration.

### Features

- User authentication with a Pluxee account.
- Card balance sensor.
- Periodic cloud data polling (`cloud_polling`).
- Home Assistant UI setup (Config Flow).

### Installation via HACS

1. Add this repository as a **Custom repository** of type **Integration**.
2. Install **PLUXEE card integration**.
3. Confirm that files are installed at:
   - `/config/custom_components/pluxee`
4. Restart Home Assistant.
5. Go to **Settings > Devices & Services > Add Integration** and search for **Pluxee**.

### Support

If you find any issues, please open an issue in this repository.

### Credits

This application was developed based on @ruidias integration:
https://github.com/netsoft-ruidias/ha-custom-component-myedenred

### Legal notice

This is a personal project and is not affiliated with, sponsored by, or endorsed by [Pluxee Portugal](https://www.pluxee.pt/).

All product names, trademarks, registered trademarks, and images in this repository are the property of their respective owners and are used for identification purposes only.
