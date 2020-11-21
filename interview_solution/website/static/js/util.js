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

function questionDeleteConfirm(n) {
    if (confirm("이 질문을 내 질문에서 삭제하시겠습니까?")) {
        window.location.href = "/website/myquestion/delete/" + n;
    } else {
        return false;
    }
}