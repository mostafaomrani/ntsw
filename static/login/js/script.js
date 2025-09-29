// ======================== INPUT VALIDATION ========================
$('input').on('keypress', function (e) {
    const input = e.target
    if ($(this).has('input-validation-error')) {
        $(this).removeClass('input-validation-error')
        $(this).parent().find('.validate-error').css({ visibility: "hidden" })
    }
    if (e.keyCode == 8 || e.keyCode == 13) return true
    if (e.target.type == "number" && (e.which < 48 || e.which > 57)) e.preventDefault()
    if (e.target.value < 0) e.preventDefault()
    return this.value.length < $(this).attr("maxLength") || !!window.getSelection().toString()
})

$('input').keydown(e => {
    if (e.keyCode == 40 || e.keyCode == 38) e.preventDefault()
})

// ======================== PASSWORD TOGGLE ========================
$(".switchPassType").on('click', function (el) {
    const element = $(el.target)
    const input = element.parent().find('input')
    const type = input.attr('type')
    input.attr('type', type === 'password' ? 'text' : 'password')
    element.attr('src', type === 'password' ? '/images/eye-c.svg' : '/images/eye.svg')
})

// ======================== BACK ARROW ========================
$("#backArrow").on('click', () => window.history.back())

// ======================== CAPTCHA ========================
$('#modal').modal('show')

function cloudflareCaptchaCallBack() {
    $('button').attr('disabled', false)
}

// ======================== SLIDER ========================
const sliderContainer = document.querySelector('#silder_images_container')
const slides = document.querySelectorAll('.silder_imagetext')
const arrowRight = document.querySelector('#slider__arrow_right')
const arrowLeft = document.querySelector('#slider__arrow_left')
const dots = document.querySelectorAll('.slider-dot')

let currentIndex = 0
let totalSlides = slides.length
let timeout = null
let scrolling = false

function goToSlide(index) {
    currentIndex = (index + totalSlides) % totalSlides
    const targetSlide = slides[currentIndex]
    if (targetSlide) {
        sliderContainer.scrollTo({
            left: targetSlide.offsetLeft,
            behavior: 'smooth'
        })
        updateDots()
    }
    resetTimeout()
}

function updateDots() {
    dots.forEach(dot => dot.classList.remove('active'))
    if (dots[currentIndex]) dots[currentIndex].classList.add('active')
}

function resetTimeout() {
    if (timeout) clearTimeout(timeout)
    timeout = setTimeout(() => goToSlide(currentIndex + 1), 5000)
}

arrowRight?.addEventListener('click', () => {
    if (scrolling) return
    scrolling = true
    setTimeout(() => scrolling = false, 500)
    goToSlide(currentIndex + 1)
})

arrowLeft?.addEventListener('click', () => {
    if (scrolling) return
    scrolling = true
    setTimeout(() => scrolling = false, 500)
    goToSlide(currentIndex - 1)
})

let scrollTimeout = null

sliderContainer?.addEventListener('scroll', () => {
    if (scrollTimeout) clearTimeout(scrollTimeout)

    scrollTimeout = setTimeout(() => {
        const containerScroll = sliderContainer.scrollLeft
        const closest = [...slides].reduce((prev, slide, index) => {
            const distance = Math.abs(slide.offsetLeft - containerScroll)
            return distance < prev.distance ? { index, distance } : prev
        }, { index: 0, distance: Infinity })

        if (closest.index !== currentIndex) {
            currentIndex = closest.index
            updateDots()
            resetTimeout()
        }
    }, 100) // Wait for scroll to settle
})

dots.forEach((dot, i) => {
    dot.addEventListener('click', () => goToSlide(i))
})

goToSlide(0)

// ======================== TOOLTIP ========================
$(() => $('[data-toggle="tooltip"]').tooltip({ offset: '-26px' }))

$("#callSenterIcon, #callSenterIcon2").on('click', () => {
    $('#modalCallCenter').modal('show')
})

// ======================== CUSTOM SELECT ========================
$('.select').on('click', (e) => {
    const $select = $(e.currentTarget)
    const $options = $select.find('.options')
    $options.toggleClass('show')

    const top = $select[0].getBoundingClientRect().top
    if (window.innerHeight - top > 250) $options.removeClass('fromButton')
    else $options.addClass('fromButton')
})

$('.option').on('click', (e) => {
    const text = e.target.innerText
    $(e.target).siblings().removeClass('active')
    $(e.target).addClass('active')
    $(e.target).closest('.options').removeClass('show')
    $(e.target).closest('.select').find('.select-value').text(text)
})

$('body').on('click', (e) => {
    if (!$(e.target).is('.select')) $('.options').removeClass('show')
})

// ======================== PARENT/ZIRSAMANHA ========================
$("#parentSection").on('click', e => {
    $('.zirsamaneha .option').removeClass('active')
    $('.zirsamaneha .select-value').text($("#SelectPlaceholder").text())

    if ($(e.target).attr('data-has-child') === "True") {
        $('#zirsamaneha').show()
        $("#extentionCard").hide()
    } else {
        $('#zirsamaneha').hide()
        fillExtentionBoxWithThisData({
            comment: $(e.target).attr('data-comment'),
            processess: $(e.target).attr('data-proccess')
        })
    }
})

$("#zirsamaneha").on('click', e => {
    $('#zirsamaneha').show()
    fillExtentionBoxWithThisData({
        comment: $(e.target).attr('data-comment'),
        processess: $(e.target).attr('data-proccess')
    })
})

function fillExtentionBoxWithThisData({ comment, processess }) {
    if (comment || processess) {
        $("#extentionCard").show()
        $("#comments").text(comment)
        $("#proccesses").text(processess)
    }
}

// ======================== FORM SUBMIT LOADING ========================
$('form').submit(displayLoading)
$('#dolateman').on('click', displayLoading)

function displayLoading() {
    $("#loadingBar").show()
}
function hideLoading() {
    $("#loadingBar").hide()
}

function checkifHasError() {
    const hasError = document.querySelector('.validate-error')?.innerText
    if (hasError) $('.inputs').addClass('hasError')
}

$(document).ready(() => {
    hideLoading()
    checkifHasError()
})

// ======================== DRAWER ========================
const openDrawer = () => {
    $('#burgerIcon').attr('src', "/images/close.svg").css('padding', "8px")
    $('.drawer-menu').addClass('open').animate({ right: '0' }, 'fast')
    $('body').css('overflow', 'hidden')
}

const closeDrawer = () => {
    $('#burgerIcon').attr('src', "/images/hamber.svg").css('padding', "0")
    $('.drawer-menu').removeClass('open').animate({ right: '-100%' }, 'fast')
    $('body').css('overflow', 'auto')
}

$('#burgerIcon').on('click', () => {
    if ($('.drawer-menu').hasClass('open')) closeDrawer()
    else openDrawer()
})

window.addEventListener('resize', () => {
    if (document.body.clientWidth > 1100) closeDrawer()
})

// ======================== PASSWORD STRENGTH ========================
const passwordField = document.getElementById('password_field')
if (passwordField) {
    const lengthCriteria = document.getElementById('details_length')
    const uppercaseCriteria = document.getElementById('details_caps')
    const numberCriteria = document.getElementById('details_number')
    const symbolCriteria = document.getElementById('details_symbol')

    passwordField.addEventListener('input', () => {
        const password = passwordField.value
        lengthCriteria.style.color = password.length >= 12 ? 'green' : 'red'
        uppercaseCriteria.style.color = /[A-Z]/.test(password) ? 'green' : 'red'
        numberCriteria.style.color = /\d/.test(password) ? 'green' : 'red'
        symbolCriteria.style.color = /[\W_]/.test(password) ? 'green' : 'red'
    })
}

// ======================== PAGE LOAD LOGIC ========================
document.addEventListener("DOMContentLoaded", function () {
    const pathname = window.location.pathname.toLowerCase()
    const searchParams = new URLSearchParams(window.location.search)

    if (pathname === '/clients') {
        $('.systemsMenu, .drawer-menus-links-systems').addClass('active')
    } else {
        $('.systemsMenu, .drawer-menus-links-systems').removeClass('active')
    }

    if (pathname === '/account/profile') {
        $('.drawer-menus-links-profile').addClass('active')
    }

    let returnUrl = null
    for (const [key, value] of searchParams.entries()) {
        if (key.toLowerCase() === 'returnurl') {
            returnUrl = value
            break
        }
    }
    const burgerButton = document.getElementById("burgerIcon")
    const headerMenu = document.querySelector('.header-menu')
    const backBtn = document.getElementById("backtoSystmeButton")

    if (pathname.includes("profile")) {
        if (backBtn && returnUrl && returnUrl.toLowerCase() !== pathname &&
            returnUrl.toLowerCase() !== '/clients' &&
            returnUrl.toLowerCase() !== 'clients') {
            backBtn.style.display = "inline-flex"
            if (burgerButton) burgerButton.style.display = "none"
            if (headerMenu) headerMenu.style.display = "none"
        } else {
            if (backBtn) backBtn.style.display = "none"
        }
    } else {
        if (backBtn) backBtn.style.display = "none"
    }
})

function backtoSystem() {
    displayLoading()
    $.getJSON('/Account/Profile/Index?handler=BacktoSystem', {}, function (result) {
        hideLoading()
        window.location.href = result.url
    }).fail(function () {
        hideLoading()
    })
}

// ======================== DISABLE BUTTON ON SUBMIT ========================
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("form").forEach(form => {
        form.addEventListener("submit", () => {
            if (form.checkValidity()) {
                setTimeout(() => {
                    form.querySelectorAll("button").forEach(button => button.disabled = true)
                }, 10)
            }
        })
    })
})

// ======================== ENAMAD LOGO ========================
const img = new Image()
img.referrerPolicy = 'origin'
img.src = 'https://trustseal.enamad.ir/logo.aspx?id=177575&Code=mrlh9FNszGs9FvlErzmL'
img.onload = () => {
    document.getElementById('enamad-img').src = img.src
}

// ======================== PREVENT SCROLL IN NUMBER FIELDS ========================
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('input[type=number]').forEach(input => {
        input.addEventListener('wheel', function (e) {
            if (document.activeElement === this) e.preventDefault()
        })
    })
})
