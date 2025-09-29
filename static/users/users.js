let togglePassword = document.getElementById('toggle-password');
if (togglePassword) {
    togglePassword.addEventListener('click', e => {

        let password = document.getElementById('id_password');
        if (password) {
            if (password.type === 'password') {
                password.type = 'text';
            } else {
                password.type = 'password';
            }
        }

    });
}


let togglePasswordRepeat = document.getElementById('toggle-password-repeate');
if (togglePasswordRepeat) {
    console.log('ok');
    togglePasswordRepeat.addEventListener('click', e => {
        let passwordRepeat = document.getElementById('id_password2');
        if (passwordRepeat) {
            if (passwordRepeat.type === 'text') {
                passwordRepeat.type = 'password';
            } else {
                passwordRepeat.type = 'text';
            }
        }
    });
}



let togglePassword1 = document.getElementById('toggle-password1');
if (togglePassword1) {
    togglePassword1.addEventListener('click', e => {
        let password1 = document.getElementById('id_password1');
        if (password1) {
            if (password1.type === 'text') {
                password1.type = 'password';
            } else {
                password1.type = 'text';
            }
        }
    });
}


let newPassword = document.getElementById('toggle-new-password');
console.log('ok', newPassword);
if (newPassword) {
    newPassword.addEventListener('click', e => {
        let password1 = document.getElementById('id_new_password');
        if (password1) {
            if (password1.type === 'text') {
                password1.type = 'password';
            } else {
                password1.type = 'text';
            }
        }
    });
}


let confirmPassword = document.getElementById('toggle-password-repeate');
if (confirmPassword) {
    confirmPassword.addEventListener('click', e => {
        let password1 = document.getElementById('id_confirm_password');
        if (password1) {
            if (password1.type === 'text') {
                password1.type = 'password';
            } else {
                password1.type = 'text';
            }
        }
    });
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
                در حال ارسال ...
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