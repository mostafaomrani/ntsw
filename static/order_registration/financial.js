$('#id_currency_type').selectize({
    maxItems: 1,
    create: false,

});


$('#id_bank').selectize({
    maxItems: 1,
    create: false,
    valueField: 'id',
    labelField: 'text',
    onChange: loadOptions(mainURL + `/order-registration/bank-branch-json/`, 'id_bank_branch'),

});


$('#id_curency_supply, #id_payment_type').selectize({
    create: false,
    valueField: 'id',
    labelField: 'text',
});


var selectCurrencyOperation = function () {
    return function (e) {
        loadOptions(mainURL + `/order-registration/currency-supply-json-list/`, 'id_curency_supply')(e);
        if (e === 'b') {
            $('#bank-container').show();
        }
        else {
            $('#bank-container').hide();
        }

    }
}


$('#id_currency_operation_type').selectize({
    maxItems: 1,
    create: false,
    valueField: 'id',
    labelField: 'text',
    options: [],
    onChange: selectCurrencyOperation()
});


$('#id_bank_branch').selectize({
    maxItems: 1,
    create: false,
    valueField: 'id',
    labelField: 'text',
    options: []
});

