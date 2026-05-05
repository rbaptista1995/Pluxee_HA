# Pluxee Home Assistant Integration (Portugal)

Integração não oficial para o Home Assistant que permite consultar dados do cartão Pluxee (Portugal), incluindo saldo e transações recentes, através da API da plataforma de consumidores.

The data source for this integration is the [Pluxee Portugal](https://www.pluxee.pt/).

The author of this project categorically rejects any and all responsibility for the card balance and other data that were presented by the integration.

## Funcionalidades

- Autenticação na conta Pluxee do utilizador.
- Sensor com informação de saldo do cartão.
- Consulta periódica de dados em cloud (`cloud_polling`).
- Configuração via UI do Home Assistant (Config Flow).

## Instalação via HACS

1. Adicione este repositório como **Custom repository** do tipo **Integration**.
2. Instale a integração **PLUXEE card integration**.
3. Confirme que os ficheiros são instalados em:
   - `/config/custom_components/pluxee`
4. Reinicie o Home Assistant.
5. Vá a **Definições > Dispositivos e Serviços > Adicionar integração** e procure por **Pluxee**.

## Suporte

Se encontrar problemas, abra uma issue no repositório.

## Créditos

Aplicação desenvolvida com base na integração do @ruidias https://github.com/netsoft-ruidias/ha-custom-component-myedenred


## Legal notice
This is a personal project and isn't in any way affiliated with, sponsored or endorsed by [Pluxee Portugal](https://www.pluxee.pt/).

All product names, trademarks and registered trademarks in (the images in) this repository, are property of their respective owners. All images in this repository are used by the project for identification purposes only.
