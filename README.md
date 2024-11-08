#  Sistema de Agendamento via WhatsApp

Este é um sistema de agendamento de serviços via WhatsApp utilizando a API da Twilio e Flask. O sistema permite que os usuários escolham um serviço, uma data, um horário e o método de pagamento, com uma resposta final confirmando o agendamento.

## Tecnologias e Ferramentas Utilizadas

- **Python**: Linguagem principal utilizada para o backend.
- **Flask**: Framework Python para a criação da API.
- **Twilio API**: Para integração com o WhatsApp e envio de mensagens.
- **Twilio Messaging API**: Para enviar e responder mensagens no WhatsApp.
- **Bibliotecas de Python**:
  - `twilio`: Para interação com a API da Twilio.
  - `datetime`: Para manipulação de datas e horários.
  - `timedelta`: Para calcular datas futuras (ex: próximo dia disponível).

## Funcionalidades

- **Envio de Mensagens no WhatsApp**: O sistema envia mensagens automatizadas para o número do cliente, oferecendo serviços, horários e outros detalhes.
- **Escolha de Serviço**: O usuário pode escolher entre os seguintes serviços:
  - Consulta (R$50)
  - Massagem (R$80)
  - Terapia (R$100)
- **Escolha de Data**: O usuário escolhe uma data disponível (hoje ou o próximo dia).
- **Escolha de Horário**: O usuário escolhe um horário disponível para o serviço.
- **Escolha de Método de Pagamento**:
  - PIX
  - Cartão de Crédito
  - Dinheiro na consulta
- **Confirmação de Agendamento**: O sistema envia um resumo do agendamento com o serviço, data, horário e método de pagamento escolhido.
- **Agradecimento e Aviso de Pontualidade**: O sistema finaliza com um aviso sobre a importância de chegar pontualmente e um agradecimento.

## Estrutura do Projeto

```plaintext
.
├── chat.py               
 ````


### Explicação:

1. **Tecnologias e Ferramentas Utilizadas**: Descreve as tecnologias principais usadas, como Python, Flask e Twilio.
2. **Dependências**: Lista as bibliotecas necessárias e como instalá-las.
3. **Estrutura do Projeto**: Exibe a organização dos arquivos no repositório.
4. **Licença e Contribuição**: Orientações sobre contribuição para o projeto e a licença utilizada.

