from urllib import response
import requests
import json
import webbrowser
from datetime import date, timedelta
import credentials

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" \
        "(KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
HOST = "ct.comprovei.com"
HEADERS = {
    'authority': HOST,
    'sec-ch-ua': "'Not;A Brand';v='99'," \
        "'Google Chrome';v='97', 'Chromium';v='97'",
    'accept': "*/*",
    'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
    'x-requested-with': "XMLHttpRequest",
    'sec-ch-ua-mobile': "?0",
    'user-agent': USER_AGENT,
    'sec-ch-ua-platform': "'Linux'",
    'origin': f"https://{HOST}",
    'sec-fetch-site': "same-origin",
    'sec-fetch-mode': "cors",
    'sec-fetch-dest': "empty",
    'accept-language': "en-US,en;q=0.9,pt;q=0.8"
}

def login():
    payload_login = f"_method=POST&data[User][code]=marfrig&data[User][username]={credentials.LOGIN}&data[User][password]={credentials.PASSWORD}"
    response = requests.post(
        url=f"https://{HOST}/Users/signIn/",
        data=payload_login,
        headers=HEADERS
    )
    return response.cookies['CAKEPHP']

def get_report():
    today = date.today().strftime('%d/%m/%Y')
    week_ago = (date.today() - timedelta(days=7)).strftime('%d/%m/%Y')
    print("data atual:", today, "7 dias atrás: ", week_ago)
    payload_report = f"_method=POST&data[Report][fields_include]=Rota%2CData%2CRegi%C3%A3o%2CMotorista%2CPlaca%2CDocumento%2CC%C3%B3digo+cliente%2CCNPJ+Cliente%2CCliente%2CEndere%C3%A7o%2CBairro%2CCidade%2CEstado%2CCEP%2CLatitude%2CLongitude%2CIn%C3%ADcio+de+Viagem%2CIn%C3%ADcio+Pausa%2CFim+Pausa%2CChegada%2CIn%C3%ADcio+de+Confer%C3%AAncia%2CFim+de+Confer%C3%AAncia%2CRegistro+da+Foto%2CRegistro+da+Anota%C3%A7%C3%A3o%2CRegistro+de+Assinatura%2CFim+da+Entrega%2CTempo+de+Perman%C3%AAncia%2CTempo+de+viagem%2CTempo+de+viagem+%2B+perman%C3%AAncia%2CSequ%C3%AAncia+original%2CSequ%C3%AAncia+realizada%2CEmbarcador%2CVolumes%2CDist%C3%A2ncia+Percorrida%2CPedido%2CBase+Origem%2CBase+Destino%2CData+Agendamento%2CData+%C3%9Alt.+Ocorr.%2CUltima+Ocorr%C3%AAncia%2CStatus+Documento%2CTransportadora%2CTempo+de+Espera%2CTempo+de+Descarga%2CTMA%2CPeso+Bruto%2CGerente%2CValor%2CVeiculo%2CJanela+Min.%2CJanela+Max.%2CAjuste+Manual%2CUsu%C3%A1rio+Ajuste%2CDia+da+semana+da+entrega%2CChegada+dentro+da+certa&data[Report][export]=documentProcessTimes&data[Report][routeDate1]={week_ago}&data[Report][routeDate2]={today}&data[Report][route_regions]=&data[Report][route_carriers]=&data[Report][route_number]=&data[Report][numberplate]=&data[Report][clients]="
    cakephp = login()
    COOKIE = f"CakeCookie[lang]=Q2FrZQ%3D%3D.89nB;CAKEPHP={cakephp};AWSELB=396F476B1097CEC4C681B8D2C8E14142F91599AF9761A8F17392C258D0614C81D9E793311AB31A19CA91326936105B429E3803B8C2F0750303D27AF64BEFBE534090C7B679;CakeCookie[is_bp]=Q2FrZQ%3D%3D.sw%3D%3D;CakeCookie[is_gf]=Q2FrZQ%3D%3D.sw%3D%3D;CakeCookie[is_sw]=Q2FrZQ%3D%3D.sw%3D%3D;"
    HEADERS['cookie'] = COOKIE
    response = requests.post(
        url=f'https://{HOST}/reports/export_documentProcessTimes',
        data=payload_report,
        headers=HEADERS,
    )

    if response.status_code == 200:
        return '' if not response.text else json.loads(response.content)

def download():
    url = get_report()['user_message']
    print(url)
    webbrowser.open(url)

if __name__ == '__main__':
    download()
