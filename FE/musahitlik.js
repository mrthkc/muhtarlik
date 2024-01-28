$(document).ready(function() {
    $("#mahalle_select").parent().hide();

    $.get("https://form.tip.org.tr/api/ils/", (data) => {
        for(var k in data) {

            var x = document.getElementById("il_select");
            var option = document.createElement("option");

            option.value = data[k].id;
            option.text = data[k].name;
            x.add(option);
        }
    });

    $("#il_select").on("change", function() {
        var il_val= $(this).val();
        $("#ilce_select").empty();

        var x = document.getElementById("ilce_select");
        var option = document.createElement("option");
        option.value = "";
        option.text = "İlçe Seçiniz";
        option.disabled = true;
        option.selected = true;
        x.add(option);

        $.get("https://form.tip.org.tr/api/ilces/?il_id=" + il_val, (data) => {
            for(var k in data) {

                var x = document.getElementById("ilce_select");
                var option = document.createElement("option");

                option.value = data[k].id;
                option.text = data[k].name;
                x.add(option);
            }
        });
    });

    $("#ilce_select").on("change", function() {
        var ilce_val= $(this).val();
        $("#mahalle_select").empty();
        
        $.get("https://form.tip.org.tr/api/muhtarliks/?ilce_id=" + ilce_val, (data) => {
            for(var k in data) {

                var x = document.getElementById("mahalle_select");
                var option = document.createElement("option");

                option.value = data[k].id;
                option.text = data[k].name;
                x.add(option);
            }
        });

        $("#mahalle_select").parent().show();

    });

    $("#musahit_button").on("click", function() {

        var tc_no = $("#tc_no").val();
        var first_name = $("#first_name").val();
        var last_name = $("#last_name").val();
        var dob = $("#dob").val();
        var sex = $("#sex").val();
        var mobile = $("#mobile").val();
        var mail = $("#mail").val();
        var il_id = $("#il_select").val();
        var ilce_id = $("#ilce_select").val();
        var muhtar_id = $("#mahalle_select").val();
        var profession = $("#profession").val();
        var education = $("#education").val();
        var extra = $("#extra").val();

        var data = { 
            "tc_no": tc_no,
            "first_name": first_name,
            "last_name": last_name,

            "dob": dob,
            "sex": sex,
            "mobile": mobile,
            "mail": mail,

            "il_id": parseInt(il_id),
            "ilce_id": parseInt(ilce_id),
            "muhtarlik_id": parseInt(muhtar_id),

            "education": education,
            "profession": profession,
            "extra": extra
        };

        $.ajax({
            type: 'POST',
            url: 'https://form.tip.org.tr/api/musahit/',
            data: JSON.stringify(data),
            success: function(result) {
                $('#successModal').modal('show');
            },
            contentType: "application/json",
            dataType: 'json'
        });

    });

    function checkInputFormat(){
        var isValid = true;

        $(this).find(':input[required]').each(function() {
            if ($(this).val() === '') {
                isValid = false;
            }
        });

        if (!$("#kvkk").is(':checked')) {
            isValid = false;
        }

        $('form input').each(function() {
            var inputType = $(this).attr('type');
            if (inputType == 'tel') {
                var telPattern = /^0[0-9]{10}$/;
                if (!telPattern.test($(this).val())) {
                    isValid = false;
                }
            } else if (inputType == 'id'){
                var idPattern = /^[0-9]{11}$/;
                if (!idPattern.test($(this).val())) {
                    isValid = false;
                }
            }
        });

        $('#musahit_button').prop('disabled', !isValid);
    }
    $('form input').on('change keyup', checkInputFormat);
    checkInputFormat();

});