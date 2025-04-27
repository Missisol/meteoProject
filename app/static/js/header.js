const pathname = document.location.pathname
const href = document.location.pathname
const items = Array.from(document.querySelectorAll('.nav__item'))

const nested = document.querySelector('#menu-dropdown')
const button = document.querySelector('.nav__button')

items.forEach((item) => {
    const a = item.dataset.url.replace('sensor.', '/')
    if (a === href) {
        item.classList.add('active')
    } else {
        item.classList.remove('active')
    }
})

document.body.addEventListener('click', (e) => {
    if (nested.classList.contains('open')) {
        nested.classList.remove('open')
    } else if (e.target === button && !nested.classList.contains('open')) {
        nested.classList.add('open')
    }
})