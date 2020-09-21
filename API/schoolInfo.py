from bs4 import BeautifulSoup
import urllib.request

def util(url):
    request = urllib.request.urlopen(url)
    xml = request.read()
    soup = BeautifulSoup(xml, "html.parser")

    return soup

# 인증키 입력
apiKey = "6d14f6536718c067d03750f8226d2e8c"

def collect_info():
    # 시도 조회(시도는 17개)
    url = "http://career.go.kr/cnet/openapi/getOpenApi?apiKey=" + apiKey + "&svcType=api" \
        "&svcCode=SCHOOL&contentType=xml&gubun=high_list"

    soup = util(url)
    totalCount = soup.find("totalcount").text

    url = "http://career.go.kr/cnet/openapi/getOpenApi?apiKey=" + apiKey + "&svcType=api" \
          "&svcCode=SCHOOL&contentType=xml&gubun=high_list&perPage=" + totalCount

    soup = util(url)
    highSchool = soup.find_all("content")

    # 고등학교 정보 조회
    schoolName = []

    for data in highSchool:
        schoolName.append(data.find("schoolname").text)


# main
collect_info()
