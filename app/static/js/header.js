const pathname = document.location.pathname
const href = document.location.pathname.replace('/', 'sensor.')

const items = Array.from(document.querySelectorAll('.nav__item'))

items.forEach((item) => {
    const a = item.dataset.url
    if (a.includes(href)) {
        item.classList.add('active')
    } else {
        item.classList.remove('active')
    }
})


