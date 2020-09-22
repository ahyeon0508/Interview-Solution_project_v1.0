function fn_pw_lenCheck() {
    var pw = document.getElementById("password").value; //비밀번호

    if(pw.length<8||pw.length>20){
        alert("비밀번호는 8자리 이상 20자 이하로 구성하여야 합니다.");
        return false;
    }          
    return true;
}

function fn_pw_check() {
    var pw = document.getElementById("password").value; //비밀번호
    var pw2 = document.getElementById("passwordChk").value; // 확인 비밀번호

    if(pw != pw2) {
        alert("비밀번호가 일치하지 않습니다.");
        return false;
    }

    return true;
}