document.addEventListener('DOMContentLoaded', function () {
    var sellerName = document.getElementById('seller-name');
    var sellerType = document.getElementById('id_supplier');
    $('.personal-seller').hide();
    $('.company-seller').hide();
    $('#id_beneficiary_country, #id_order_registration_case').selectize({
        create: false,
    });
    $('#id_beneficiary_country, #id_order_registration_case, #seller-identifier').selectize({
        create: false,
        valueField: 'id',
        labelField: 'text',

    });

    var eventHandler = function () {
        return function (e) {
            console.log(e)
            let url = e == 'person' ? `${mainURL}${personJsonList}` : `${mainURL}${companyJsonList}`;
            $.get(url, function (data, status) {
                if (status == 'success') {
                    console.log(data);
                    let options = data.map(value => ({
                        id: value.identifier,
                        text: value.identifier
                    }));
                    console.log('options:', options);
                    let shippingTypeSelectize = $('#seller-identifier')[0]?.selectize;
                    console.log(shippingTypeSelectize)
                    shippingTypeSelectize.enable();
                    shippingTypeSelectize.clear();
                    shippingTypeSelectize.clearOptions();
                    shippingTypeSelectize.addOption(options);
                    shippingTypeSelectize.refreshOptions(false);  // به‌روزرسانی Selectize

                }
                else {
                    alert('مشکلی در دریافت داده‌ها پیش آمده است. لطفا با پشتیبان دموی سامانه جامع تجارت تماس بگیرید.');
                }
            })
        };
    }
    $('#id_supplier').selectize({
        create: false,
        onChange: eventHandler()
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
        }
    );
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




    function removeSelectOptions(select) {
        let len = select.options.length;
        for (i = len - 1; i > 0; i--) {
            select.options[i] = null;
        }
        select.options[0].selected = true;
    }

    searchSeller = document.getElementById('search-seller');
    searchSeller.addEventListener('click', e => {
        $('.company-seller').hide();
        $('.personal-seller').hide();
        let ContentType = document.getElementById('id_supplier').value;
        if (!ContentType) {
            alert('انتخاب نوع فروشنده خارجی الزامی است. لطفا ابتدا نوع فروشنده خارجی را انتخاب کنید.')
            return;
        }
        let sellerIdentifier = document.getElementById('seller-identifier').value
        if (!sellerIdentifier) {
            return
        }
        let url = ContentType == 'person' ? `${mainURL}/supplier/person-json-by-identifier/${sellerIdentifier}` : `${mainURL}/supplier/company-json-by-identifier/${sellerIdentifier}`;
        let sellerNameContainer = document.getElementById('seller-name-container');
        $.get(url, function (data, status) {
            removeSelectOptions(sellerName);
            console.log(data);
            if (status == 'success') {
                let stringfyData = JSON.stringify(data);
                localStorage.setItem('sellers', stringfyData);
                let option = document.createElement('option');
                data.forEach(element => {
                    option.text = element.name || element.first_name;
                    option.value = element.pk;
                    sellerName.add(option);
                });
                sellerNameContainer.classList.remove('d-none');
            }
            else {
                alert('مشکلی در دریافت داده‌ها پیش آمده است. لطفا با پشتیبان دموی سامانه جامع تجارت تماس بگیرید.');
            }
        });
    });
    sellerName.addEventListener('change', e => {
        let sellers = JSON.parse(localStorage.getItem('sellers'));
        console.log(sellers);
        let sellerIdentifier = document.getElementById('seller-identifier').value;
        sellers.forEach(d => {
            if (d.identifier != sellerIdentifier) {


                if (sellerType.value == 'company') {
                    document.getElementById('registered-country').value = d.country_name;
                    document.getElementById('address').value = d.address;
                    document.getElementById('phone').value = d.phone;
                    document.getElementById('registered-number').value = d.register_number;
                    $('.company-seller').show();

                } else {
                    document.getElementById('last-name').value = d.last_name;
                    document.getElementById('produce-country').value = d.country_name;
                    $('.personal-seller').show();
                }
            }

        });
    })
});