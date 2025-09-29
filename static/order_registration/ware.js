document.addEventListener('DOMContentLoaded', function () {
    const exampleModal = document.getElementById('exampleModal')
    if (exampleModal) {
        let url = `${mainURL}/order-registration/create-ware/${mainDataPK}`
        $.ajax({
            url: url,
            type: 'get',
            success: function (data) {
                $('#ware-form-container').html('')
                $('#ware-form-container').html(data)
            }
        })
    }


    $(document).on('submit', '#create-ware-form', function(event) {
        event.preventDefault(); // جلوگیری از رفتار پیش‌فرض فرم
        
        let form = $(this); // انتخاب فرم
        let submitBtn = form.find('button[type="submit"]'); // یافتن دکمه سابمیت
        
        // ذخیره محتوای اصلی دکمه
        submitBtn.data('original-html', submitBtn.html());
        
        // غیرفعال کردن دکمه و نمایش اسپینر
        submitBtn.prop('disabled', true);
        submitBtn.html(`
            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            در حال ارسال...
        `);
        
        // اعتبارسنجی فیلدها
        if (!$('#id_technical_specifications').val() && !$('#id_standard').val()) {
            alert('مشخصات فنی و استاندارد نمی‌تواند همزمان خالی باشد. یکی از فیلدها را باید تکمیل نمایید.');
            
            // بازگردانی دکمه به حالت اولیه
            submitBtn.html(submitBtn.data('original-html'));
            submitBtn.prop('disabled', false);
            return;
        }
        
        let url = form.attr('action'); // آدرس اکشن
        let formData = new FormData(this); // جمع‌آوری داده‌های فرم
        
        $.ajax({
            url: url,
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                // در صورت موفقیت، صفحه ریدایرکت می‌شود
                window.location.href = response.success_url;
            },
            error: function(xhr) {
                // نمایش فرم با پیام‌های خطا
                $('#ware-form-container').html(xhr.responseText);
                alert('خطایی در ثبت کالا به وجو آمده است. لطفا پس از اصلاح خطا‌ها دوباره روی ثبت کلیک نمایید.');
                
                // بازگردانی دکمه به حالت اولیه در صورت خطا
                submitBtn.html(submitBtn.data('original-html'));
                submitBtn.prop('disabled', false);
            },
            complete: function() {
                // این تابع در هر حالتی (موفق یا خطا) اجرا می‌شود
                // اگر ریدایرکت نشده باشد، دکمه را بازگردان
                if (!window.location.href.includes(response?.success_url)) {
                    submitBtn.html(submitBtn.data('original-html'));
                    submitBtn.prop('disabled', false);
                }
            }
        });
    });

    const deleteModal = document.getElementById('deleteModal')
    if (deleteModal) {
        deleteModal.addEventListener('show.bs.modal', event => {
            const button = event.relatedTarget;
            const pk = button.getAttribute('data-bs-pk');
            const hsCodeText = button.getAttribute('data-bs-hs');
            const deleteForm = deleteModal.querySelector('#delete-form');
            const hsCodeSpan = deleteModal.querySelector('#delete-hs-code');
            let actionURL = mainURL + `/order-registration/delete-ware/${pk}`;
            hsCodeSpan.textContent = hsCodeText;
            deleteForm.setAttribute('action', actionURL);
        })
    }

    const editModal = document.getElementById('EditModal')
    if (editModal) {
        editModal.addEventListener('show.bs.modal', event => {
            const button = event.relatedTarget;
            const pk = button.getAttribute('data-bs-ware');
            const formContainer = editModal.querySelector('#ware-edit-form-container');
            formContainer.textContent = pk;
            // let wareForm = document.getElementById('ware-edit-form-container');
            let url = `${mainURL}/order-registration/update-ware/${pk}`;
            console.log('urls is: ', url)
            $.ajax({
                url: url,
                type: 'get',
                success: function (data) {
                    $('#ware-edit-form-container').html('')
                    $('#ware-edit-form-container').html(data)
                }
            })

        })
    }

    $(document).on('submit', '#edit-ware-form', function (event) {
        event.preventDefault(); // جلوگیری از رفتار پیش‌فرض فرم

        let form = $(this); // انتخاب فرم
        let url = form.attr('action'); // آدرس اکشن
        let formData = new FormData(this); // جمع‌آوری داده‌های فرم
        if (!$('#update-technical-specifications').val() && !$('#update-standard').val()) {
            alert('مشخصات فنی و استاندارد نمی‌تواند همزمان خالی باشد. یکی از فیلدها را باید تکمیل نمایید.');
            return;
        }

        $.ajax({
            url: url,
            type: 'POST', // نوع درخواست
            data: formData,
            processData: false, // جلوگیری از پردازش داده‌ها (برای FormData)
            contentType: false, // جلوگیری از تنظیم نوع محتوا به صورت خودکار
            success: function (response) {
                //بارگذاری دوباره صفحه و اضافه شدن یک ردیف‌های فروشنده
                window.location.reload()
            },
            error: function (xhr) {
                // نمایش فرم با پیام‌های خطا
                $('#ware-edit-form-container').html(xhr.responseText);
                alert('خطایی در ثبت کالا به وجو آمده است. لطفا پس از اصلاح خطا‌ها دوباره روی ثبت کلیک نمایید.');
            }
        });
    });
    document.getElementById('remove-ware').addEventListener('click', e => {
        const table = document.getElementById('ware-table');
        const rows = table.querySelectorAll('tbody tr');
        const data = [];
        rows.forEach(row => {
            const checkboxInput = row.querySelector('input[type="checkbox"]')
            if (checkboxInput.checked) {
                console.log('test');
                const idInput = row.querySelector('input[type="hidden"]'); // انتخاب فیلد مخفی
                const id = idInput ? idInput.value : null; // گرفتن مقدار value
                data.push(id);
            }
        });
        console.log(data);
        fetch(bulkDelete, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        })
            .then(response => response.json())
            .then(result => {
                location.reload();
            })
            .catch(error => {
                alert('خطایی در حذف کالاهای پرونده رخ داده است. لطفا با پشتیبان دموی سامانه جامع تجارت تماس بگیرید.');

            });
    });
});