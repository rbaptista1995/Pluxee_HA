# Pluxee Home Assistant Integration (Portugal)

Integração não oficial para o Home Assistant que permite consultar dados do cartão Pluxee (Portugal), incluindo saldo e transações recentes, através da API da plataforma de consumidores.

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
