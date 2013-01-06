
function applyJob(job_id, login_path) {
    $.ajax({
        type:"GET",
        async:false,
        url:"/personal/apply/"+job_id,
        dataType:"json",
        success: function(data) {
            if(data){
                if (data.result == 'login_required') {
                    window.location = login_path;
                } else if(data.result == 'conflict') {
                    alert("对不起，该工作您已经申请过了。")
                } else if(data.result == 'type_error') {
                    alert("对不起，企业用户不能执行此操作。")
                } else {
                    alert("恭喜你，申请已成功发出。");
                }
            }
            else{
                alert("服务器错误，请联系网站管理员!");
            }
            return true;
        }
    });
}

function storeJob(job_id, login_path) {
    $.ajax({
        type:"GET",
        async:false,
        url:"/personal/store/"+job_id,
        dataType:"json",
        success: function(data) {
            if(data){
                if (data.result == 'login_required') {
                    window.location = login_path;
                } else if(data.result == 'conflict') {
                    alert("对不起，该工作您已经收藏过了。")
                } else if(data.result == 'type_error') {
                    alert("对不起，企业用户不能执行此操作。")
                } else {
                    alert("收藏成功。");
                }
            }
            else{
                alert("服务器错误，请联系网站管理员!");
            }
            return true;
        }
    });
}
