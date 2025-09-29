document.addEventListener('DOMContentLoaded', function () {

    $('#id_beneficiary_country').selectize({
        create: false,
    });
    $('#id_proforma_invoice_issue_date').datepicker(
        {
            todayHighlight: true,
            language: 'fa',
            autoclose: true,
            weekStart: 7,
            format: 'yyyy-mm-dd',
            rtl: true,
            templates: {
                leftArrow: '<i class="fa fa-chevron-right" aria-hidden="true"></i>',
                rightArrow: '<i class="fa fa-chevron-left" aria-hidden="true"></i>'
            }
        }
    );


    $('#id_proforam_invoice_expire_date').datepicker(
        {
            todayHighlight: true,
            language: 'fa',
            autoclose: true,
            weekStart: 7,
            format: 'yyyy-mm-dd',
            rtl: true,
            templates: {
                leftArrow: '<i class="fa fa-chevron-right" aria-hidden="true"></i>',
                rightArrow: '<i class="fa fa-chevron-left" aria-hidden="true"></i>'
            },
            startDate: new Date()
        }
    );
    $('#id_supplier').change(function (e) {
        let supplierType = e.target.value;
        let url = '';
        if (supplierType == 'person') {
            url = personJsonList;
            $('.personal-seller').show();
            $('.company-seller').hide();
            $('#seller-name').val('');
            $('#last-name').val('');
            $('#produce-country').val('');
        }
        else if (supplierType == 'company') {
            url = companyJsonList;
            $('.personal-seller').hide();
            $('.company-seller').show();
            $('#company-name').val('');
            $('#registered-number').val('');
            $('#registered-country').val('');
            $('#address').val('');
            $('#phone').val('');
        }
        $.get(url, function (data, status) {
            if (status === 'success') {
                console.log(data);

                // دسترسی به Selectize
                var selectizeInstance = $('#id_related_object_id')[0]?.selectize;
                if (!selectizeInstance) {
                    console.error('Selectize instance not found!');
                    return;
                }

                // پاک کردن گزینه‌ها
                selectizeInstance.clearOptions();

                // ایجاد گزینه‌ها از داده‌ها
                let options = data.map(value => ({
                    id: value.pk, // مقدار
                    text: value.identifier // متن نمایشی
                }));

                // افزودن گزینه‌ها به Selectize
                selectizeInstance.addOption(options);

                // (اختیاری) انتخاب اولین مقدار پیش‌فرض
                if (options.length > 0) {
                    selectizeInstance.setValue(options[0].value);
                }
            } else {
                alert('خطایی در ارتباط با سرور پیش آمده است لطفاً با مدیر دمو تماس بگیرید.');
            }
        }).fail(function () {
            alert('ارتباط با سرور انجام نشد. لطفاً دوباره تلاش کنید.');
        });

    });
    document.getElementById('search-supplier').addEventListener('click', () => {
        let supplierIdentifier = document.getElementById('id_related_object_id').value;
        let supplierType = document.getElementById('id_supplier').value;
        if (!supplierIdentifier && !supplierType) {
            alert('انتخاب نوع فروشنده و شناسه فروشنده الزامی است');
        }
        let url = supplierType == 'person' ? `${mainURL}/supplier/person-json-by-identifier/${supplierIdentifier}` : `${mainURL}/supplier/company-json-by-identifier/${supplierIdentifier}`;
        $.get(url, function (data, status) {
            if (status == 'success') {
                console.log(data);
                if (supplierType == 'person') {
                    document.getElementById('seller-name').value = data.first_name;
                    document.getElementById('last-name').value = data.last_name;
                    document.getElementById('produce-country').value = data.country;
                    $('.personal-seller').show()

                } else {
                    $('#company-name').val(data.name);
                    $('#registered-number').val(data.register_number);
                    $('#registered-country').val(data.registered_country);
                    $('#address').val(data.address);
                    $('#phone').val(data.phone);
                    $('.company-seller').show()

                }
            }
            else {
                alert('مشکلی در دریافت داده‌ها پیش آمده است. لطفا با پشتیبان دموی سامانه جامع تجارت تماس بگیرید.');
            }
        })
    });
    const selectField = document.getElementById('id_order_registration_case');

    selectField.addEventListener('change', function (e) {
        e.preventDefault();  // جلوگیری از تغییر مقدار
    });

    // غیرفعال کردن کلیک راست و کشیدن (Drag)
    selectField.addEventListener('mousedown', function (e) {
        e.preventDefault();
    });
});

$('#producer_type_container').hide();

$('#id_producer_type_0').click(function () {
    $('#producer_type_container').show();
    $('#producer-type-data-text').text('شناسه کسب و کار')

})

$('#id_producer_type_1, #id_producer_type_2, #id_producer_type_3').click(function () {
    $('#producer_type_container').show();
    $('#producer-type-data-text').text('استان محل فعالیت')

})

$('#id_producer_type_4').click(function () {
    $('#producer_type_container').show();
    $('#producer-type-data-text').text('مجوز فعالیت')

})