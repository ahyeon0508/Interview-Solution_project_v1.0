<<<<<<< HEAD
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

function cancleForm(){
    if(confirm("이 페이지를 벗어나면 마지막 저장 후 수정된 내용은 저장되지 않습니다.")){
        // 메인 홈페이지 주소 입력하기
      window.location.href = "";
    }
    else {
        return false;
    }
  
  }
=======
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
<<<<<<< HEAD

function cancleForm(){
    if(confirm("이 페이지를 벗어나면 마지막 저장 후 수정된 내용은 저장되지 않습니다.")){
        // 메인 홈페이지 주소 입력하기
      window.location.href = "";
    }
    else {
        return false;
    }
  
  }
=======
>>>>>>> b980a489352d40603aef40585dcf40e1bcb18854
>>>>>>> 91024130cce99854c4c822c1765d49b85efab365
