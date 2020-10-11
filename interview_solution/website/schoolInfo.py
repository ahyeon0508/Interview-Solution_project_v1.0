from bs4 import BeautifulSoup
import urllib.request
from .models import SchoolInfo
from django.shortcuts import render

def util(url):
    request = urllib.request.urlopen(url)
    xml = request.read()
    soup = BeautifulSoup(xml, "html.parser")

    return soup

# 인증키 입력
apiKey = "6d14f6536718c067d03750f8226d2e8c"

def collect_info():
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
        schoolName.append("(" + data.find("region").text + ") " + data.find("schoolname").text)

    print(schoolName)
    for i in schoolName:
        SchoolInfo.objects.filter(name=i).delete()
        SchoolInfo(name=i).save()

# main
def schoolInfo_db(request):
    collect_info()
    return render(request,'schooldb.html')