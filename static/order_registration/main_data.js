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
const sleep = ms => new Promise(r => setTimeout(r, ms));

const waitingModal = document.getElementById('waitingModal')
if (waitingModal) {
    waitingModal.addEventListener('show.bs.modal', async (event) => {
        const button = event.relatedTarget
        const recipient = button.getAttribute('data-bs-status')
        const location = button.getAttribute('data-bs-href');
        const statusText = waitingModal.querySelector('#status-text');
        statusText.textContent = `${recipient}`;
        await sleep(5000);
        console.log('run after 5ms');
        window.location = location;
    })
}