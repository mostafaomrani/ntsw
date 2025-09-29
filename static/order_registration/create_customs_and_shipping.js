$(document).ready(function () {

    $('#id_origin_country').selectize({
        create: false,
    });

    $('#id_incoterms').selectize({
        maxItems: 1,
        create: false,
        valueField: 'id',
        labelField: 'text',
        onChange: loadOptions(mainURL + `/order-registration/shipping-json-list/`, 'id_shipping_type'),
    })

    var shippingTypeSelectize = $('#id_shipping_type').selectize({
        create: false,
        valueField: 'id',
        labelField: 'text',
        onChange: loadOptions(mainURL + `/order-registration/entrance-json-list/`, 'id_entrance_edge')
    });

    var EntranceEdgeSelectize = $('#id_entrance_edge').selectize({
        create: false,
        valueField: 'id',
        labelField: 'text',
    });

    var destinationCustomSelectise = $('#id_destination_custom').selectize({
        create: false,
        valueField: 'id',
        labelField: 'text',
    })


    $('#id_shipping_nationality').selectize();

    var selects = [shippingTypeSelectize, EntranceEdgeSelectize, destinationCustomSelectise];
    selects.forEach(select => {
        if (select[0]?.selectize) {
            s = select[0].selectize;
            s.settings.maxItems = 1; //فعال سازی تک انتخابی پس از لود
            s.enable();
            s.refreshOptions(false); // به‌روزرسانی گزینه‌ها
        }
    });

    // ثبت رویداد change
    $('#id_shipping_period').change(function () {
        console.log('Change event triggered');
        if ($(this).is(':checked')) {
            console.log('ok');
            selects.forEach(select => {
                if (select[0]?.selectize) {
                    s = select[0].selectize;
                    s.settings.maxItems = null; // برای چند انتخابی
                    s.enable();
                    s.clear();
                    s.refreshOptions(false); // به‌روزرسانی گزینه‌ها
                }
            });
        } else {
            let selects = [shippingTypeSelectize, EntranceEdgeSelectize, destinationCustomSelectise];
            selects.forEach(select => {
                if (select[0]?.selectize) {
                    s = select[0].selectize;
                    s.settings.maxItems = 1; // برای تک انتخابی
                    s.enable();
                    s.clear();
                    s.refreshOptions(false); // به‌روزرسانی گزینه‌ها
                }
            });
        }
    });
});


