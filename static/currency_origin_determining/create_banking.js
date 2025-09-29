document.addEventListener("DOMContentLoaded", function () {

    const randomNumber = generateRandomEightDigitNumber();

    document.getElementById('id_pay_number').value = randomNumber

    function generateMultipleCodes(count, length) {
        const codes = [];
        for (let i = 0; i < count; i++) {
            codes.push(generateRandomCode(length)); // تولید کد و اضافه کردن به آرایه
        }
        return codes;
    }

    // تولید یک کد هشت رقمی
    const codes = generateMultipleCodes(1, 8);
    options_array = []
    var options_array = codes.map(value => ({
        id: value,
        text: value
    }));

    $('#id_shipping_document').selectize({
        maxItems: 1,
        create: false,
        sortField: 'text',
        valueField: 'id',
        labelField: 'text',
        options: options_array
    })

    $('#id_origin_country').selectize()


    let EntranceEdgeSelectize = $('#id_entrance_edge').selectize({
        create: false,
        options: [],
    });

    let destinationCustomSelectise = $('#id_custom_destination').selectize({
        create: false,
        sortField: 'title',
        sortField: 'title',
        valueField: 'id',
    })


    var billingTableBody = document.getElementById('billing-body');
    var prefix = 'bilings';
    var billingTotalForms = document.getElementById("id_" + prefix + "-TOTAL_FORMS");
    var billingFormCount = parseInt(billingTotalForms.value);
    document.getElementById('add-bill').addEventListener('click', e => {
        let billingNumber = document.getElementById('billing_number');
        let billingDate = document.getElementById('billing_date');
        let date = billingDate.value
        let row = `<tr>
                        <td><input class="form-control border-0" value="${billingNumber.value}" type="text" name="${prefix}-${billingFormCount}-identifier" min="0" id="id_${prefix}-${billingFormCount}-identifier" style="background:rgba(0,0,0,0);"></td>
                        <td><input class="form-control border-0" value="${date}" type="date" name="${prefix}-${billingFormCount}-date" id="id_${prefix}-${billingFormCount}-date" style="background:rgba(0,0,0,0);"></td>
                        <td><input type="checkbox" class="form-check-input row-checkbox" name="${prefix}-${billingFormCount}-DELETE" id="id_ladingbill_set-${billingFormCount}-DELETE"></td>
                    </tr>`;
        try {
            billingTableBody.innerHTML += row;
            billingFormCount++;
            billingNumber.value = '';
            billingDate.value = '';
            billingTotalForms.value = billingFormCount;
        }
        catch (err) {
            alert(`بارنامه مورد نظر اضافه نشد. خطا:${err.message}`)
        }

    });
    document.getElementById('remove-billing').addEventListener('click', e => {
        let rows = Array.from(billingTableBody.children)

        for (let i = rows.length - 1; i >= 0; i--) {
            let checkbox = rows[i].querySelector(".row-checkbox");
            if (checkbox && checkbox.checked) {
                rows[i].remove();
                billingFormCount--;
            }
        }
        billingTotalForms.value = billingFormCount;
    });
    let wareTableBody = document.getElementById('ware-table-body');
    let checkboxes = document.querySelectorAll('.ware-checkbox');

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('click', e => {
            let rows = Array.from(wareTableBody.children);
            let fobAmount = 0;

            rows.forEach(row => {
                console.log(row);
                let checkbox = row.querySelector('.ware-checkbox');
                if (checkbox && checkbox.checked) {
                    let fobElement = row.querySelector('.ware-fob');
                    if (fobElement) {
                        let fob = parseFloat(fobElement.textContent);
                        if (!isNaN(fob)) {
                            fobAmount += fob;
                        }
                    }
                }

            });

            document.getElementById('id_fob_amount').value = fobAmount;
            document.getElementById('id_lading_bill_fob').value = fobAmount;
        });
    });


    // افزودن requred به اینپوت‌هایی که تیک آن ردیف زده شده است

    // اضافه کردن رویداد به تمام چک‌باکس‌ها
    wareTableBody.querySelectorAll('.ware-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', function () {
            // پیدا کردن ردیف جاری
            let currentRow = this.closest('tr');

            // پیدا کردن تمام input‌های عددی در ردیف جاری
            let numberInputs = currentRow.querySelectorAll('.ware-input');

            // اگر چک‌باکس تیک خورده باشد، required اضافه کنید
            if (this.checked) {
                numberInputs.forEach(input => {
                    input.setAttribute('required', true);
                });
            } else {
                // اگر تیک برداشته شد، required را حذف کنید
                numberInputs.forEach(input => {
                    input.removeAttribute('required');
                });
            }
        });
    });
    // بررسی وجود بارنامه و کالا قبل از سابمیت شدن فرم
    document.getElementById('banking-form').addEventListener('submit', e => {
        let rows = Array.from(wareTableBody.children);
        let wareFlag = false
        rows.forEach(row => {
            let checkbox = row.querySelector('.ware-checkbox');
            if (checkbox && checkbox.checked) {
                wareFlag = true
            }
        });
        if (billingTotalForms <= 0 || !wareFlag) {
            alert('تعیین منشا ارز حداقل باید یک بارنامه و یک کالا داشته باشد');
            e.preventDefault(); // Prevent form submission
        }
    });

});


