<<<<<<< HEAD
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

function secedeForm(n){
    if(confirm("정말로 탈퇴하시겠습니까?")){
        // 탈퇴 주소 입력하기
        window.location.href = "" + n;
    } else {
        return false;
    }
=======
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

function secedeForm(n){
    if(confirm("정말로 탈퇴하시겠습니까?")){
        // 탈퇴 주소 입력하기
        window.location.href = "" + n;
    } else {
        return false;
    }
>>>>>>> 91024130cce99854c4c822c1765d49b85efab365
  }