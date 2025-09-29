let nextButton = document.getElementById('request-currency-next');
if (nextButton) {
    nextButton.addEventListener('click', e => {
        let requestForm = document.querySelector('#nav-profile-tab');
        let tab = new bootstrap.Tab(requestForm);
        document.getElementById('nav-home-tab').classList.add('processed');
        tab.show();
    });
}

let prevButton = document.getElementById('request-currency-prev');
if (prevButton) {
    prevButton.addEventListener('click', e => {
        let mainData = document.querySelector('#nav-home-tab');
        let tab = new bootstrap.Tab(mainData);
        tab.show();
    });
}

$('#id_currency').selectize();

let requestAmountByMainDataCurrency = document.getElementById('id_request_amount_by_main_data_currency');
requestAmountByMainDataCurrency.addEventListener('change', e => {
    document.getElementById('id_request_amount').value = e.target.value;
});


$('#id_transaction_type').selectize(
    {
        create: false,
        valueField: 'id',
        onChange: loadOptions(mainURL + `/currency-allocation/undertaking-json-list/`, 'id_undertaking'),


    }
);


$('#id_undertaking').selectize(
    {
        create: false,
        valueField: 'id',
        onChange: loadOptions(mainURL + `/currency-allocation/facility-location-json-list/`, 'id_facility_location'),

    }
);

$('#id_facility_location').selectize(
    {
        create: false,
        valueField: 'id',
        options: [],
        onChange: loadOptions(mainURL + `/currency-allocation/repayment-deadline-json-list/`, 'id_repayment_deadline'),

    }
);

$('#id_repayment_deadline').selectize(
    {
        create: false,
        valueField: 'id',
        options: [],
        onChange: loadOptions(mainURL + `/currency-allocation/supply-currency-place-json-list/`, 'id_supply_currency_place'),

    }
);

$('#id_supply_currency_place').selectize(
    {
        create: false,
        valueField: 'id',
        options: [],
        onChange: loadOptions(mainURL + `/currency-allocation/currency-rate-json-list/`, 'id_currency_rate'),
    }
);

$('#id_currency_rate').selectize(
    {
        create: false,
        valueField: 'id',
        options: [],
        onChange: loadOptions(mainURL + `/currency-allocation/request-type-json-list/`, 'id_request_type'),

    }
);
var changeExpirationDateLabel = function () {
    return function (e) {
        const transactionTypeSelectize = $('#id_transaction_type')[0]?.selectize;
        const requestTypeSelectize = $('#id_request_type')[0]?.selectize;
        const selectedValue = transactionTypeSelectize.getValue();
        const transactionTypeText = transactionTypeSelectize.getItem(selectedValue).text()
        const requestTypeText = requestTypeSelectize.getItem(e).text()
        const label = document.getElementById('request-expire-data');
        console.log(transactionTypeText);
        console.log(requestTypeText);
        if (transactionTypeText === 'پیش پرداخت' && requestTypeText === 'اصل') {
            label.textContent = 'مهلت انقضا (حداکثر تا ۱۸۰ روز)'
        }

    };

}
$('#id_request_type').selectize(
    {
        create: false,
        valueField: 'id',
        options: [],
        onChange: changeExpirationDateLabel()
    }
);

deleteSelectizeOption('id_undertaking');
deleteSelectizeOption('id_facility_location');
deleteSelectizeOption('id_repayment_deadline');
deleteSelectizeOption('id_supply_currency_place');
deleteSelectizeOption('id_currency_rate');
deleteSelectizeOption('id_request_type');


// Read selected file and write name in table
document.getElementById('register-document').addEventListener('click', function (event) {
    // دریافت فایل انتخاب‌شده
    // const file = event.target.files[0];
    const fullPath = document.getElementById('id_document').value
    let row = document.getElementById('file-container');
    const emptyTableAlert = document.getElementById('empty-table-alert');

    // نمایش نام فایل
    if (fullPath) {
        var startIndex = (fullPath.indexOf('\\') >= 0 ? fullPath.lastIndexOf('\\') : fullPath.lastIndexOf('/'));
        var filename = fullPath.substring(startIndex);
        if (filename.indexOf('\\') === 0 || filename.indexOf('/') === 0) {
            filename = filename.substring(1);
        }
        const lastDotIndex = filename.lastIndexOf('.'); // پیدا کردن آخرین نقطه
        let extension = filename.substring(lastDotIndex);
        let name = filename.substring(0, lastDotIndex);

        row.innerHTML = `
            <td>
            1
            </td>
            <td>
            ${name}
            </td>
            <td>
            ${extension}
            </td>
            <td>
            <button type="button" id="delete-document" class="btn btn-danger" onclick="deleteFile()">
            <i class="fa fa-trash"></i>
            <span class="ps-1">
            حذف
            </span>
            </button>
            </td>
        `;
        emptyTableAlert.classList.add('d-none');

    } else {
        emptyTableAlert.classList.remove('d-none');

        row.innerHTML = '';
    }
});

function deleteFile() {
    const emptyTableAlert = document.getElementById('empty-table-alert');
    document.getElementById('id_document').value = '';
    document.getElementById('file-container').innerHTML = '';
    emptyTableAlert.classList.remove('d-none');

}