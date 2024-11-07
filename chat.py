from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from datetime import datetime, timedelta

import os



account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

client = Client(account_sid, auth_token)

app = Flask(__name__)

horarios_disponiveis = [
    "09:00", "10:00", "11:00", "14:00", "15:00", "16:00"
]

estado_usuario = {
    'etapa': 'inicio', 
    'servico': None,
    'data': None,
    'horario': None,
    'metodo_pagamento': None
}

def enviar_mensagem_inicial():
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body='Olá! Aqui é da Magri Service. Como posso ajudar você hoje? Digite "serviços" para ver os serviços disponíveis.',
        to='whatsapp:+5515997821338'
    )
    print(f"Mensagem inicial enviada, SID: {message.sid}")

@app.route('/whatsapp', methods=['POST'])
def whatsapp():
    global estado_usuario  
    incoming_message = request.form.get('Body').lower()
    response = MessagingResponse()
    message = response.message()

    if estado_usuario['etapa'] == 'inicio':
        if 'serviços' in incoming_message:
            message.body("Temos os seguintes serviços:\n1. Consulta - R$50\n2. Massagem - R$80\n3. Terapia - R$100\n\nDigite o número do serviço para agendar ou saber mais.")
            estado_usuario['etapa'] = 'escolhendo_servico'

    elif estado_usuario['etapa'] == 'escolhendo_servico':
        if incoming_message == '1':
            estado_usuario['servico'] = 'Consulta'
            message.body("Você escolheu 'Consulta'. O valor é R$50.\nPor favor, responda com 'data' para escolher uma data disponível.")
            estado_usuario['etapa'] = 'escolhendo_data'
        elif incoming_message == '2':
            estado_usuario['servico'] = 'Massagem'
            message.body("Você escolheu 'Massagem'. O valor é R$80.\nPor favor, responda com 'data' para escolher uma data disponível.")
            estado_usuario['etapa'] = 'escolhendo_data'
        elif incoming_message == '3':
            estado_usuario['servico'] = 'Terapia'
            message.body("Você escolheu 'Terapia'. O valor é R$100.\nPor favor, responda com 'data' para escolher uma data disponível.")
            estado_usuario['etapa'] = 'escolhendo_data'

    elif estado_usuario['etapa'] == 'escolhendo_data':
        data_hoje = datetime.now().strftime('%d/%m/%Y')
        proxima_data = (datetime.now() + timedelta(days=1)).strftime('%d/%m/%Y')
        message.body(f"Escolha uma data disponível:\n1. {data_hoje}\n2. {proxima_data}\n\nResponda com o número da data desejada.")
        estado_usuario['etapa'] = 'confirmando_data'

    elif estado_usuario['etapa'] == 'confirmando_data':
        if incoming_message == '1':
            estado_usuario['data'] = datetime.now().strftime('%d/%m/%Y')
        elif incoming_message == '2':
            estado_usuario['data'] = (datetime.now() + timedelta(days=1)).strftime('%d/%m/%Y')
        
        message.body(f"Data escolhida: {estado_usuario['data']}\nEscolha o horário:\n" + "\n".join([f"{i+1}. {hora}" for i, hora in enumerate(horarios_disponiveis)]))
        estado_usuario['etapa'] = 'escolhendo_horario'

    elif estado_usuario['etapa'] == 'escolhendo_horario':
        if incoming_message.isdigit() and int(incoming_message) - 1 in range(len(horarios_disponiveis)):
            horario_escolhido = horarios_disponiveis[int(incoming_message) - 1]
            estado_usuario['horario'] = horario_escolhido
            message.body(f"Horário escolhido: {horario_escolhido}.\nEscolha o método de pagamento:\n1. PIX\n2. Cartão de Crédito\n3. Dinheiro na consulta\n\nResponda com o número do método desejado.")
            estado_usuario['etapa'] = 'escolhendo_pagamento'

    elif estado_usuario['etapa'] == 'escolhendo_pagamento':
        if incoming_message == '1':
            estado_usuario['metodo_pagamento'] = 'PIX'
        elif incoming_message == '2':
            estado_usuario['metodo_pagamento'] = 'Cartão de Crédito'
        elif incoming_message == '3':
            estado_usuario['metodo_pagamento'] = 'Dinheiro na consulta'

        message.body(f"Resumo do seu agendamento:\n\nServiço: {estado_usuario['servico']}\nData: {estado_usuario['data']}\nHorário: {estado_usuario['horario']}\nMétodo de pagamento: {estado_usuario['metodo_pagamento']}\n\n*Lembre-se de chegar pontualmente e iremos enivar o que você deve trazêr.*\nAgradecemos pela sua escolha e nos vemos em breve!")

        estado_usuario = {'etapa': 'inicio', 'servico': None, 'data': None, 'horario': None, 'metodo_pagamento': None}

    else:
        message.body('Desculpe, não entendi sua mensagem. Pode reformular?')

    return str(response)

if __name__ == '__main__':
    enviar_mensagem_inicial()  
    app.run(port=5000)
