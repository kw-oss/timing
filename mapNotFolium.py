from PIL import Image
import requests
import io
import subprocess as sp # 쉘 명령어를 실행하기 위한 모듈
import re # 정규표현식 사용
import json

# 정확도 조절 - 높은 값으로 설정할수록 속도가 빨라지나 정확도가 떨어짐
accuracy = 1
commd = 'add-type -assemblyname system.device; '\
        '$loc = new-object system.device.location.geocoordinatewatcher;'\
        '$loc.start(); '\
        'while(($loc.status -ne "Ready") -and ($loc.permission -ne "Denied")) '\
        '{start-sleep -milliseconds 100}; '\
        '$acc = %d; '\
        'while($loc.position.location.horizontalaccuracy -gt $acc) '\
        '{start-sleep -milliseconds 100; $acc = [math]::Round($acc*1.5)}; '\
        '$loc.position.location.latitude; '\
        '$loc.position.location.longitude; '\
        '$loc.position.location.horizontalaccuracy; '\
        '$loc.stop()' %(accuracy)

pshellcomm = ['powershell', commd]

# 쉘 명령어 실행 및 결과값 저장
p = sp.Popen(pshellcomm, stdin = sp.PIPE, stdout = sp.PIPE, stderr = sp.STDOUT, text=True)
(out, err) = p.communicate()

# 전체 출력 문자열에서 개행문자를 기준으로 분리 
out = re.split('\n', out)

lat = float(out[0])
long = float(out[1])
radius = int(out[2])

print(lat, long, radius)

def addr_to_lat_lon(addr):
    api_key = "82e74383a81e76a453aed30fac79cef2"
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query={address}'.format(address=addr)
    headers = {"Authorization": "KakaoAK " + api_key}
    result = json.loads(str(requests.get(url, headers=headers).text))
    match_first = result['documents'][0]['address']
    return float(match_first['x']), float(match_first['y'])

def lat_lon_to_addr(lon ,lat):
        url = 'https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?x={longitude}&y={latitude}'.format(longitude=lon,latitude=lat)
        headers = {"Authorization": "KakaoAK " + "82e74383a81e76a453aed30fac79cef2"}
        result = json.loads(str(requests.get(url, headers=headers).text))
        match_first = result['documents'][0]['address_name']
        return str(match_first)

# NCP 콘솔에서 복사한 클라이언트ID와 클라이언트Secret 값
client_id = "c5g1xuzoiy"
client_secret = "r35jPUaeT5KiDCTIW7uecAqN4Aq7jkKxo4eKqllR"

# 좌표 (경도, 위도)
endpoint = "https://naveropenapi.apigw.ntruss.com/map-static/v2/raster"
headers = {
    "X-NCP-APIGW-API-KEY-ID": client_id,
    "X-NCP-APIGW-API-KEY": client_secret,
}
# 중심 좌표
#myAddress = lat_lon_to_addr(long,lat)
#myLocation = addr_to_lat_lon(myAddress)
markerCenter = f"""type:n|size:small|pos:{long} {lat}|color:green|viewSizeRatio:0.5"""
_center = f"{long},{lat}"
# 줌 레벨 - 0 ~ 20
_level = 14
# 가로 세로 크기 (픽셀)
_w, _h = 500, 300
# 지도 유형 - basic, traffic, satellite, satellite_base, terrain
_maptype = "basic"
# 반환 이미지 형식 - jpg, jpeg, png8, png
_format = "png"
# 고해상도 디스펠레이 지원을 위한 옵션 - 1, 2
_scale = 2
# 마커
#_markers = f"""type:n|size:mid|pos:{lon} {lat}|color:red|viewSizeRatio:0.5|label:1"""

foodLocation = addr_to_lat_lon("서울 노원구 광운로 37 1층")
_markers1 = f"""type:n|size:mid|pos:{foodLocation[0]} {foodLocation[1]}|color:red|viewSizeRatio:0.5|label:1"""
foodLocation = addr_to_lat_lon("서울 노원구 광운로 133")
_markers2 = f"""type:n|size:mid|pos:{foodLocation[0]} {foodLocation[1]}|color:red|viewSizeRatio:0.5|label:2"""
foodLocation = addr_to_lat_lon("서울 노원구 광운로1길 26")
_markers3 = f"""type:n|size:mid|pos:{foodLocation[0]} {foodLocation[1]}|color:red|viewSizeRatio:0.5|label:3"""
foodLocation = addr_to_lat_lon("서울 노원구 광운로 61 2층")
_markers4 = f"""type:n|size:mid|pos:{foodLocation[0]} {foodLocation[1]}|color:red|viewSizeRatio:0.5|label:4"""
foodLocation = addr_to_lat_lon("서울 노원구 광운로2길 6 1층")
_markers5 = f"""type:n|size:mid|pos:{foodLocation[0]} {foodLocation[1]}|color:red|viewSizeRatio:0.5|label:5"""
foodLocation = addr_to_lat_lon("서울 노원구 광운로 132 월계역신도브래뉴 B동 1층 103호")
_markers6 = f"""type:n|size:mid|pos:{foodLocation[0]} {foodLocation[1]}|color:red|viewSizeRatio:0.5|label:6"""
foodLocation = addr_to_lat_lon("서울 노원구 광운로 29 2층")
_markers7 = f"""type:n|size:mid|pos:{foodLocation[0]} {foodLocation[1]}|color:red|viewSizeRatio:0.5|label:7"""
foodLocation = addr_to_lat_lon("서울 노원구 광운로 46")
_markers8 = f"""type:n|size:mid|pos:{foodLocation[0]} {foodLocation[1]}|color:red|viewSizeRatio:0.5|label:8"""
foodLocation = addr_to_lat_lon("서울 노원구 광운로 35 2층")
_markers9 = f"""type:n|size:mid|pos:{foodLocation[0]} {foodLocation[1]}|color:red|viewSizeRatio:0.5|label:9"""
foodLocation = addr_to_lat_lon("서울 노원구 광운로 52")
_markers10 = f"""type:n|size:mid|pos:{foodLocation[0]} {foodLocation[1]}|color:red|viewSizeRatio:0.5|label:10"""



_lang = "ko"
# 대중교통 정보 노출 - Boolean
_public_transit = True
# 서비스에서 사용할 데이터 버전 파라미터 전달 CDN 캐시 무효화
_dataversion = ""

# URL
url = f"{endpoint}?center={_center}&level={_level}&w={_w}&h={_h}&maptype={_maptype}&format={_format}&scale={_scale}&markers={markerCenter}&markers={_markers1}&markers={_markers2}&markers={_markers3}&markers={_markers4}&markers={_markers5}&markers={_markers6}&markers={_markers7}&markers={_markers8}&markers={_markers9}&markers={_markers10}&lang={_lang}&public_transit={_public_transit}&dataversion={_dataversion}"
res = requests.get(url, headers=headers)

image_data = io.BytesIO(res.content)
image = Image.open(image_data)

image.save("map.png")