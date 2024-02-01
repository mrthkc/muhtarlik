var host = "https://form.tip.org.tr/";
var isValid = true;
var firstValidation = true;


$(document).ready(function() {
    $("#mahalle_select").parent().hide();
    $("#other_gender").hide();

    $.get(host + "api/ils/", (data) => {
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

        $.get(host + "api/ilces/?il_id=" + il_val, (data) => {
            for(var k in data) {
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

        var x = document.getElementById("mahalle_select");
        var option = document.createElement("option");
        option.value = "";
        option.text = "Mahalle Seçiniz";
        option.disabled = true;
        option.selected = true;
        x.add(option);
        
        $.get(host + "api/muhtarliks/?ilce_id=" + ilce_val, (data) => {
            for(var k in data) {
                var option = document.createElement("option");

                option.value = data[k].id;
                option.text = data[k].name;
                x.add(option);
            }
        });

        $("#mahalle_select").parent().show();

    });

    var oldProfession = "";
    $("#avukat").on("click", function(event) {
        if ($(this).is(':checked')) {
            oldProfession = $("#profession").val();
            $("#profession").val("Avukat");
            $("#profession").hide();
        } else {
            $("#profession").val(oldProfession);
            $("#profession").show();
        }
    });

    $("#gender").on("change", function() {
        if ($(this).val() === "diger") {
            $("#other_gender").show();
        } else {
            $("#other_gender").hide();
        }

    });    

    $("#musahit_button").on("click", function(event) {
        event.preventDefault();

        firstValidation = false;
        checkInputFormat();

        if (!isValid) {
            $('html, body').animate({scrollTop: $('.invalid-feedback:visible:first').parent().offset().top}, 1000);            
            $('#errorDetail').text("Lütfen formdaki hataları giderdikten sonra tekrar deneyiniz");
            $('#errorModal').modal('show');            
            return false;
        }

        var tc_no = $("#tc_no").val();
        var first_name = $("#first_name").val();
        var last_name = $("#last_name").val();
        var dob = $("#dob").val();

        var gender = "";
        if ($("#gender").val() === "diger") {
            if ($("#other_gender").val() === "") {
                gender = "Diğer";
            } else {
                gender = $("#other_gender").val();
            }
        } else {
            gender = $("#gender").val();
        }

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
            "sex": gender,
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
            url: host + 'api/musahit/',
            data: JSON.stringify(data),
            success: function(result) {
                $('#successModal').modal('show');
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                errorMessage = XMLHttpRequest.responseJSON.detail;
                if (errorMessage == "Invalid TC Kimlik No") {
                    $('#errorDetail').text("Geçersiz TC kimlik numarası girdiniz. Lütfen ilgili alanları kimliğinizdeki gibi yazınız.");
                }
                else if (errorMessage == "Already Existing TC Kimlik No") {
                    $('#errorDetail').text("Daha önce yaptığınız başvuru kaydedilmiştir. Lütfen il/ilçe örgütlerimizden haber bekleyiniz.");
                }
                else {
                    $('#errorDetail').text("Beklemediğimiz bir hata ile karşılaştık.");
                }
                $('#errorModal').modal('show');
            },
            contentType: "application/json",
            dataType: 'json'
        });

    });

    $("#successButton").on("click", function(event) {
        setTimeout(1500);
        window.location.reload();
    });

    function checkInputFormat() {
        isValid = true;
        if (firstValidation) {
            return;
        }

        $('.invalid-feedback').hide();

        $('input[required]').each(function() {
            if ($(this).val() === '') {
                isValid = false;
                $(this).parent().find('.invalid-feedback').show();
            }
        });

        $('select[required]').each(function() {
            if($(this).find(':selected').prop('disabled')){
                isValid = false;
                $(this).parent().find('.invalid-feedback').show();
            }
        });        

        $('#kvkk').each(function() {
            if (!$(this).is(':checked')) {
                isValid = false;
                $(this).parent().find('.invalid-feedback').show();
            }
        });

        if (tcno_dogrula($('#tc_no').val()) == false) {
             isValid = false;
             $('#tc_no').parent().find('.invalid-feedback').show();
        }

        $('form input').each(function() {
            var inputId = $(this).attr('id');
            if (inputId == 'mobile') {
                var telPattern = /^0[0-9]{10}$/;
                if (!telPattern.test($(this).val())) {
                    isValid = false;
                    $(this).parent().find('.invalid-feedback').show();
                }
            }
        });

    }

    $('input[required]').on('change keyup', function (event) {
        checkInputFormat();
    });
    $('select[required]').on('change', function (event) {
        checkInputFormat();
    });

    function tcno_dogrula(tcno) { tcno=String(tcno);if(tcno.substring(0,1)==='0'){return!1}if(tcno.length!==11){return!1} var ilkon_array=tcno.substr(0,10).split('');var ilkon_total=hane_tek=hane_cift=0; for(var i=j=0;i<9;++i){j=parseInt(ilkon_array[i],10);if(i&1){hane_cift+=j}else{hane_tek+=j}ilkon_total+=j} if((hane_tek*7-hane_cift)%10!==parseInt(tcno.substr(-2,1),10)){return!1} ilkon_total+=parseInt(ilkon_array[9],10);if(ilkon_total%10!==parseInt(tcno.substr(-1),10)){return!1} return!0 }

});
