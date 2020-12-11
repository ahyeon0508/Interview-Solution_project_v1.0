function f_DeleteConfirm1(n) {
    if (confirm("이 피드백을 삭제하시겠습니까?")) {
        // href 넣기
        window.location.href = "/website/teacher/studentVideo/delete1/" + n;
    }
    else {
        return false;
    }
}

function f_DeleteConfirm2(n) {
    if (confirm("이 피드백을 삭제하시겠습니까?")) {
        // href 넣기
        window.location.href = "/website/teacher/studentVideo/delete2/" + n;
    }
    else {
        return false;
    }
}

function f_DeleteConfirm3(n) {
    if (confirm("이 피드백을 삭제하시겠습니까?")) {
        // href 넣기
        window.location.href = "/website/teacher/studentVideo/delete3/" + n;
    }
    else {
        return false;
    }
}

function DeleteConfirm(n) {
    if (confirm("해당 리포트를 삭제하시겠습니까?")) {
        // href 넣기
        window.location.href = "/website/myVideo/delete/" + n;
    }
    else {
        return false;
    }
}

function Q_DeleteConfirm(n) {
    if (confirm("전송한 질문을 삭제하시겠습니까?")) {
        // href 넣기
        window.location.href = "/website/teacher/questionSend/delete/" + n;
    }
    else {
        return false;
    }
}