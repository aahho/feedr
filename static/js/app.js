


(function (window) {

	var SECORE = {
		
	};

    $(document).ready(function () {

        //UI Endpoint
        window.UI_ENDPOINT = '';
        if(window.location.host === "127.0.0.1:8000") {
            window.UI_ENDPOINT = 'http://platform.dev/';
        } else if(window.location.host === 'id.sourc.in') {
            window.UI_ENDPOINT = 'http://platform.sourc.in/';
        } else {
            window.UI_ENDPOINT = 'http://platform.sourceeasy.com/';
        }
        //global function for clicking hrefs
        $("[data-link]").click(function (event) {
            window.location.href = "http://" + window.location.host + $(this).attr("data-link");
        });

        $("#goBack").click(function (event) {
            window.location.href = "http://" + window.location.host;
        });

        $("[data-details]").click(function (event) {
            var ids = $(this).attr("data-details").split("_"),
            orgId = ids[0],
            classId = ids[1];
            roleId = null;
            if(ids.length == 3){
                roleId = ids[2];
            }

            var token = $('#tokVar').val();
            var type = $(this).attr("title");

            // console.log(ids, orgId, classId, token);
            if(type === 'customer'){
                window.location.assign(window.UI_ENDPOINT + "?access_token="+token+"&org_id="+orgId+"&class_id="+classId+"&customer_id="+roleId);
            } else if(type === 'vendor') {
                window.location.assign(window.UI_ENDPOINT + "?access_token="+token+"&org_id="+orgId+"&class_id="+classId+"&vendor_id="+roleId);
            } else {
                window.location.assign(window.UI_ENDPOINT + "?access_token="+token+"&org_id="+orgId+"&class_id="+classId);
            }

        });

        // csrf = $("{% csrf_token %}").attr('value');
        $.ajaxSetup({
            global: true,
            headers: {
                "Content-Type": "application/json; charset=utf-8",
                "access-token": window.localStorage.getItem('token')
                // "X-CSRFToken" : csrf
            }
        });
        function request(method, uri, data, successCallback, errorCallback, async, headers) {
            async = async || true;
            $.ajax({
                type: method,
                url: uri,
                data: JSON.stringify(data),
                headers : headers,
                dataType: "json",
                success: function(data, textStatus, xhr){
                    successCallback(data, xhr, textStatus);
                },
                failure: function(errMsg, textStatus, xhr) {
                    errorCallback(errMsg, xhr, textStatus);
                },
                async: async

            });
        }

        var locationPath = window.location.pathname;
       
       
        if(locationPath == '/admin/dashboard'){
            //window.location.href = 'org/'+organId;
            window.history.replaceState("object or string", "Title", "/admin/dashboard");
        }

        if(locationPath.match(/(\/user\/activate\/)+/g)) {
            var id = locationPath.replace(/(\/user\/activate\/)+/g, '');
            
            window.localStorage.setItem('activation_code', id);
        }

        if(locationPath.match(/(\/activate\/authcallback)+/g)) {
            var emailPath = $('#userEmail').val();
            var activationCode = window.localStorage.getItem('activation_code');
            var form = $('form')[0];

            form.setAttribute('method', 'POST');
            form.setAttribute('action', '/user/activate/google/'+activationCode);
            form.submit();
        }

        $(".app_subscription").click(function(event) {
            var app_id = event.target.getAttribute('id').replace('app_', '');
            var orgId = location.pathname.split('/').pop();
            request("POST", "/admin/org/"+orgId +"/app/"+app_id+"/register", {},
                function(data, xhr){
                    console.log(data);
                   if(xhr.status == 200){
                       location.reload(true);
                   }
                },
                function error(errMsg, xhr){
                    location.reload(true);
                    console.log(errMsg);
                }
            );
        });

        $(".class_subscription").click(function(event) {
           
            var app_id = event.target.getAttribute('app-id');
            var class_id = event.target.getAttribute('id').replace('classify_', '');
            var orgId = location.pathname.split('/').pop();
            request("POST", "/admin/class/"+class_id+"/app/"+app_id+"/register", {},
                function(data, xhr){
                    console.log(data);
                   if(xhr.status == 200){
                       location.reload(true);
                   }
                },
                function error(errMsg, xhr){
                    location.reload(true);
                    console.log(errMsg);
                }
            );
        });

        $(".edit_permissions").click(function(event) {

            var permisison_name = event.target.getAttribute('permission_name');
            var app_id = event.target.getAttribute('app_id');
            var organisation_id = event.target.getAttribute('org_id');
            var role_id = event.target.getAttribute('role_id');

            var data = {
                "toggle":permisison_name,
                "class_id":app_id
                };
            console.log('data ==== = = = =',data,organisation_id,role_id); 

             request("POST", ""+role_id+"/permission", data,
                 function(data, xhr){
                     console.log(data);
                    if(xhr.status == 200){
                       location.reload(true);
                       }
                 },
                 function error(errMsg, xhr){
                     location.reload(true);
                     console.log(errMsg);
                 }
             );
        });

        $(".delete_user").click(function(event) {

            var user_id = event.target.getAttribute('users_id');
            var role_id = event.target.getAttribute('roles_id');
            var organisation_id = event.target.getAttribute('orgs_id');
            console.log(event.target, user_id, role_id, organisation_id);
           
            var data = {
                'users':[]
            };

            data.users.push(user_id);
            
             request("POST", "/admin/org/"+organisation_id+"/role/"+role_id+"/users/delete", data,
                 function(data, xhr){
                     console.log(data);
                    if(xhr.status == 200){
                        console.log('asdfasdfasdfasdf');
                       location.reload(true);
                    }
                 },
                 function error(errMsg, xhr){
                     location.reload(true);
                     console.log(errMsg);
                 }
             );
             
             location.reload();
        });

        $(".make_admin").click(function(event) {
            var user_id = event.target.getAttribute('id').replace('admin_', '');
            var orgId = location.pathname.split('/').pop();
            request("POST", "/admin/org/"+orgId+"/user/"+user_id+"/setRole", {},
                function(data, xhr){
                    console.log(data);
                if(xhr.status !== 200){
                        console.log(xhr);
                }
                },
                function error(errMsg, xhr){
                    console.log(errMsg);
                    location.reload();
                }
            );
        });

        $(".ban_user").click(function(event) {
            var user_id = event.target.getAttribute('id').replace('admin_', '');
            var orgId = location.pathname.split('/').pop();
            request("POST", "/admin/org/"+orgId+"/user/"+user_id+"/ban", {},
                function(data, xhr){
                    console.log(data);
                if(xhr.status !== 200){
                        console.log(xhr);
                }
                },
                function error(errMsg, xhr){
                    console.log(errMsg);
                    location.reload();
                }
            );
        });

        $(".user_classifier").change(function(event) {
            var classifier = event.target.options[this.selectedIndex].text;
            if(classifier === 'customer') {
                $("#user_entity_form").css("display", "inline-block");
                $("#customer_select").attr("name", "entity").css("display", "inline-block");
                $("#vendor_select").attr("name", "entity2").css("display", "none");
            } else if(classifier === 'vendor') {
                $("#user_entity_form").css("display", "inline-block");
                $("#customer_select").attr("name", "entity1").css("display", "none");
                $("#vendor_select").attr("name", "entity").css("display", "inline-block");
            } else {
                $("#user_entity_form").css("display", "none");
                $("#customer_select").attr("name", "entity1").css("display", "none");
                $("#vendor_select").attr("name", "entity2").css("display", "none");
            }
        });
        $("#user_entity_form").css("display", "none");

        $("#logo_remove").click(function(event) {
            $("#delete_logo").val("true");
            $("#org_logo").remove();
        });

        var successIp = $('#successIp').val();
        console.log(successIp);
        if(successIp) {
            setTimeout(function () {
                location.assign('http://'+window.location.host);
            }, 3000);
            var timeLeft = 3;
            $('#timeLeft').html('Redirecting to login in ' + timeLeft);
            setInterval(function () {
                timeLeft -= 1;
                $('#timeLeft').html('Redirecting to login in ' + timeLeft);
            }, 1000);
        }

        var errorIp = $('#errorIp').val();
        console.log(errorIp);
        if(errorIp === '400') {
            setTimeout(function () {
                location.assign('http://'+window.location.host);
            }, 3000);
            var timeLeft = 3;
            $('#timeLeft').html('Redirecting in ' + timeLeft);
            setInterval(function () {
                timeLeft -= 1;
                $('#timeLeft').html('Redirecting in ' + timeLeft);
            }, 1000);
        }

        $(".edit_milestone_template").click(function(event) {
            console.log(event.target, $(this));
        });

        function messageTriggered(){
            alert('messageTriggered');
        }

        var organisationId = 'b3a8e145-cbca-46e1-8278-be1a1d0027fa';
       
        function sidebarAccordian(item_name){

            var sidebarName = localStorage.getItem("sidebar-name"),
            
            ids = $('.sidebarSubGroup').map(function() {
                return $(this).attr('id');
            });
            if(sidebarName == "null"){
                for(var i=0; i< ids.length; i++){
                    document.getElementById(ids[i]).style.display = "none";
                }
            }else{
                for(var i=0; i< ids.length; i++){
                    if(item_name == ids[i]){
                        document.getElementById(ids[i]).style.display = "block";
                    }else{
                        document.getElementById(ids[i]).style.display = "none";
                    }
                }
            }
            
        }
        var sidebarId = localStorage.getItem("sidebar-name");
        var side = JSON.parse(sidebarId);

        sidebarAccordian(side);
    

        $(".sideBarItems").click(function(event){
            
            var item_name = event.target.getAttribute('sidebar-name');
            
            if(item_name == JSON.parse(localStorage.getItem("sidebar-name"))){
                localStorage.setItem("sidebar-name", "null");
                
            }else{
                localStorage.setItem("sidebar-name", JSON.stringify(item_name));
            }
            sidebarAccordian(item_name);
        })


    });
}(window));