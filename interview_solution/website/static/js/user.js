function secedeForm(){
    if(confirm("정말로 탈퇴하시겠습니까?")){
        // 탈퇴 주소 입력하기
        window.location.href = "/website/secede/";
    } else {
        return false;
    }
}