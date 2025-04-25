const pathname = document.location.pathname
const href = document.location.pathname
const items = Array.from(document.querySelectorAll('.nav__item'))

items.forEach((item) => {
    const a = item.dataset.url.replace('sensor.', '/')
    if (a === href) {
        item.classList.add('active')
    } else {
        item.classList.remove('active')
    }
})


