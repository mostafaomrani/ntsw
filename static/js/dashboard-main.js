
//show user avatar after select file
function previewUploadingImage(inputId, ImgId) {
    const chooseFile = document.getElementById(inputId);
    const imgPreview = document.getElementById(ImgId);
    chooseFile.addEventListener("change", function () {
        getImgData();
    });
    function getImgData() {
        const files = chooseFile.files[0];
        if (files) {
            const fileReader = new FileReader();
            fileReader.readAsDataURL(files);
            fileReader.addEventListener("load", function () {
                imgPreview.src = this.result
            });
        }
    }
}

function deleteSelectizeOption(id) {
    var selectizeInstance = $('#' + id)[0]?.selectize;
    if (!selectizeInstance) {
        console.error('Selectize instance not found!');
        return;
    }

    // پاک کردن گزینه‌ها
    selectizeInstance.clearOptions();
}

// RUN MESSAGE MODAL
const MessageModal = document.getElementById('MessageModal')
if (MessageModal) {
    MessageModal.addEventListener('show.bs.modal', event => {
        // Button that triggered the modal
        const button = event.relatedTarget
        // Extract info from data-bs-* attributes
        const title = button.getAttribute('data-bs-title');
        const content = button.getAttribute('data-bs-content');
        // If necessary, you could initiate an Ajax request here
        // and then do the updating in a callback.

        // Update the modal's content.
        const modalTitle = MessageModal.querySelector('.modal-title')
        const modalBodyInput = MessageModal.querySelector('.modal-body p')

        modalTitle.textContent = title
        modalBodyInput.textContent = content
    })
}



// UPDATE TIME
let countdown = document.getElementById("countdown");
let timeout = countdown.dataset.timeout * 1000; // تبدیل به میلی ثانیه
let remainingTime = timeout / 1000; // تبدیل به ثانیه

function autoLogout() {
    location.reload();
    console.log('invoke redirect to logout');
}

function updateCountdown() {
    let minutes = Math.floor(remainingTime / 60);
    let seconds = remainingTime % 60;
    countdown.textContent =
        `${minutes}:${seconds.toString().padStart(2, '0')}`;
    if (remainingTime > 0) {
        remainingTime--;
    } else {
        autoLogout();
    }
}

// اجرای شمارش معکوس هر ثانیه
let countdownInterval = setInterval(updateCountdown, 1000);

function resetTimer() {
    clearTimeout(timer);
    clearInterval(countdownInterval);
    remainingTime = timeout / 1000; // بازنشانی زمان باقی‌مانده
    timer = setTimeout(autoLogout, timeout);
    countdownInterval = setInterval(updateCountdown, 1000);
}

let timer = setTimeout(autoLogout, timeout);
document.addEventListener("click", resetTimer);
document.addEventListener("submit", resetTimer);
document.addEventListener("ajaxSend", resetTimer);

// Get the button
let mybutton = document.getElementById("go-top");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function () { scrollFunction() };

function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        mybutton.style.display = "block";
    } else {
        mybutton.style.display = "none";
    }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}


function generateRandomCode(length) {
    const characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'; // کاراکترهای مجاز
    let code = '';
    for (let i = 0; i < length; i++) {
        const randomIndex = Math.floor(Math.random() * characters.length);
        code += characters[randomIndex]; // اضافه کردن کاراکتر تصادفی به کد
    }
    return code;
}

function generateRandomEightDigitNumber() {
    const min = 10000000; // کوچکترین عدد ۸ رقمی (۱۰۰۰۰۰۰۰)
    const max = 99999999; // بزرگترین عدد ۸ رقمی (۹۹۹۹۹۹۹۹)
    return Math.floor(Math.random() * (max - min + 1)) + min;
}


function generateMultipleCodes(count, length) {
    const codes = [];
    for (let i = 0; i < count; i++) {
        codes.push(generateRandomCode(length)); // تولید کد و اضافه کردن به آرایه
    }
    return codes;
}


// اعتبارسنجی فرم
const forms = document.querySelectorAll('.needs-validation');
Array.from(forms).forEach(form => {
    form.addEventListener('submit', event => {
        let isFormValid = true;

        // بررسی اعتبارسنجی پیش‌فرض فرم
        if (!form.checkValidity()) {
            isFormValid = false;
        }
        // اگر فرم معتبر نباشد، ارسال نشود
        if (!isFormValid) {
            event.preventDefault();
            event.stopPropagation();
        }
        form.querySelectorAll('select.selectized').forEach(select => {
            const selectizeInstance = $(select)[0].selectize; // دسترسی به نمونه Selectize
            if (!selectizeInstance) {
                console.error('Selectize مقداردهی نشده است:', select);
                return;
            }
            validateSelectize(selectizeInstance);

            if (!selectizeInstance.getValue()) {
                isFormValid = false;
            }
            // مثال: دریافت مقدار فعلی
            console.log('مقدار فعلی:', selectizeInstance.getValue());

        })

        // اضافه کردن کلاس was-validated به فرم
        form.classList.add('was-validated');
    }, false);
});

// تابع اعتبارسنجی
function validateSelectize(selectizeInstance) {
    const control = selectizeInstance.$control[0];
    console.log(control);
    if (!control || !control.parentElement) {
        console.error('والد کنترل selectize یافت نشد.', control)
    }
    if (!selectizeInstance.getValue() || selectizeInstance.getValue().length === 0) {
        control.parentElement.classList.add('is-invalid');
    } else {
        control.parentElement.classList.remove('is-invalid');
    }
}
// پیدا کردن تمام Selectizeهای موجود
$('select.selectized').each(function () {
    const selectizeInstance = this.selectize;
    if (!selectizeInstance) {
        console.error('Selectize مقداردهی نشده است:', this);
        return;
    }
    // افزودن رویداد onChange برای اعتبارسنجی
    selectizeInstance.on('change', function () {
        validateSelectize(selectizeInstance);
    });

    // افزودن رویداد onBlur برای اعتبارسنجی
    selectizeInstance.on('blur', function () {
        validateSelectize(selectizeInstance);
    });
});


var loadOptions = function (url, id) {
    return function (e) {
        i = '#' + id;
        let shippingTypeSelectize = $(i)[0]?.selectize;
        if (!shippingTypeSelectize) {
            console.error('shipping type selectize not found');
            alert('خطایی در ارتباط با پایگاه داده به وجود آمده است. لطفا با پشتیبانی دمو تماس بگیرید');
            return
        }
        if (!e) {
            return
        }
        let queryParams = '';
        let q = '';
        if (Array.isArray(e)) {
            queryParams = '?' + $.param({ ids: e })
        } else {
            q = e;
        }
        $.get(url + q + queryParams,
            function (data, status) {
                if (status === 'success') {
                    console.log('id: ', data);
                    let options = data.map(value => ({
                        id: value.id ? value.id : value.pk,
                        text: value.title
                    }));
                    shippingTypeSelectize.enable();
                    shippingTypeSelectize.clear();
                    shippingTypeSelectize.clearOptions();
                    shippingTypeSelectize.addOption(options);
                    shippingTypeSelectize.refreshOptions(false);  // به‌روزرسانی Selectize

                } else {
                    console.error('get error:', status)
                    alert('خطای دریافت اطلاعات از پایگاه داده با پشتیبان دموی سامانه جامع تجارت تماس بگیرید.');

                }

            });

    };

}
// تابع برای دریافت توکن CSRF در Django
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// غیر فعال کردن دکمه‌ی سابمیت بعد از کلیک جهت جلوگیری ارسال دوباره‌ی فرم

document.addEventListener('submit', function(e) {
    if (e.target.matches('form') && e.target.querySelector('.btn-submit')) {
        const form = e.target;
        const submitBtns = form.querySelectorAll('.btn-submit');
        
        // جلوگیری از ارسال پیش‌فرض
        e.preventDefault();
        
        // ذخیره محتوای اصلی همه دکمه‌ها
        const originalContents = Array.from(submitBtns).map(btn => {
            const original = btn.innerHTML;
            btn.dataset.originalHtml = original; // ذخیره در dataset
            return original;
        });
        
        // نمایش اسپینر برای همه دکمه‌ها
        submitBtns.forEach(btn => {
            btn.innerHTML = `
                <span class="spinner-grow spinner-grow-sm" aria-hidden="true"></span>
                در حال ذخیره...
            `;
            btn.disabled = true;
        });
        
        // تاخیر کوتاه برای اطمینان از بروزرسانی UI
        setTimeout(() => {
            // ارسال فرم
            form.submit();
            
            // بازگردانی دکمه‌ها پس از بارگذاری مجدد
            window.addEventListener('pageshow', () => {
                submitBtns.forEach((btn, index) => {
                    btn.innerHTML = originalContents[index];
                    btn.disabled = false;
                });
            });
        }, 100);
    }
}, true); // استفاده از capture phase برای اطمینان از اجرا