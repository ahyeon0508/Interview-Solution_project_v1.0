function fn_pw_check() {
    var pw = document.getElementById("pw").value; //비밀번호
    var pw2 = document.getElementById("pwChk").value; // 확인 비밀번호

    if(pw != pw2) {
        alert("비밀번호가 일치하지 않습니다.");
        return false;
    }

   if(pw.length<8||pw.length>20){
        alert("비밀번호는 8자리 이상 20자 이하로 구성하여야 합니다.");
        return false;
    }          

    return true;
}

// 참고 : https://tonhnegod.tistory.com/7
function onlyNumber(event){
    event = event || window.event;
    var keyID = (event.which) ? event.which : event.keyCode;
    if ( (keyID >= 48 && keyID <= 57) || (keyID >= 96 && keyID <= 105) || keyID == 8 || keyID == 46 || keyID == 37 || keyID == 39 ) 
        return;
    else
        return false;
}

function removeChar(event) {
    event = event || window.event;
    var keyID = (event.which) ? event.which : event.keyCode;
    if ( keyID == 8 || keyID == 46 || keyID == 37 || keyID == 39 ) 
        return;
    else
        event.target.value = event.target.value.replace(/[^0-9]/g, "");
}
