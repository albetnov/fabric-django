"use strict";
const d = document;

async function confirmDelete(title) {
    const response = await Swal.fire({
        title,
        showCancelButton: true,
        showDenyButton: false,
        confirmButtonText: 'Yes, delete it!',
        cancelButtonText: 'No, cancel!',
    })

    return response.isConfirmed;
}

const resolveUcFirst = () => d.querySelectorAll('[x-ucfirst]').forEach((el) => {
    el.innerText = el.innerText.charAt(0).toUpperCase() + el.innerText.slice(1);
});

const resolveAllQueries = () => {
    console.log('Resolving all queries...');
    d.querySelectorAll('[x-action]').forEach((el) => {
        el.classList.add('d-flex', 'gap-2', 'justify-content-center');

        const [editUrl, deleteUrl] = el.getAttribute('x-action').split('|');

        let inner = `<a href="${editUrl}" class="btn btn-info btn-sm"><i class="fa-solid fa-pen-to-square"></i> Edit</a>`;
        inner += `<a href="${deleteUrl}" class="btn btn-danger btn-sm" x-deletable><i class="fa-solid fa-trash"></i> Delete</a>`;

        el.innerHTML = inner;
    });

    d.querySelectorAll('[x-action-edit]').forEach((el) => {
        const url = el.getAttribute('x-action-edit');

        el.innerHTML = `<a href="${url}" class="btn btn-info btn-sm"><i class="fa-solid fa-pen-to-square"></i> Edit</a>`;
    });

    d.querySelectorAll('[x-action-delete]').forEach((el) => {
        const url = el.getAttribute('x-action-delete');

        el.innerHTML = `<a href="${url}" class="btn btn-danger btn-sm" x-deletable></a>`;
    });

    d.querySelectorAll('[x-deletable]').forEach((el) => {
        el.innerHTML = '<i class="fa-solid fa-trash"></i> Delete';

        el.addEventListener('click', (e) => {
            e.preventDefault();

            const title = el.getAttribute('x-deletable');
            const url = el.getAttribute('href');

            confirmDelete(title === '' ? 'Are you sure you want to delete this item?' : title).then((result) => {
                if (result) {
                    window.location.href = url;
                }
            })
        })
    });

    d.querySelectorAll('[x-addable]').forEach((el) => {
        el.innerHTML = `<i class="fa-solid fa-plus"></i> Add ${el.getAttribute('x-addable')}`;
        el.classList.add('btn', 'btn-primary', 'btn-sm');
    });

    d.querySelectorAll('[x-form-actions]').forEach((el) => {
        const url = el.getAttribute('x-form-actions');

        el.innerHTML = `
            <button type="submit" class="btn btn-primary" form="form"><i class="fa-solid fa-floppy-disk"></i> Save</button>
            <a href="${url}" class="btn btn-secondary"><i class="fa-solid fa-arrow-left"></i> Back</a>
        `;
    });

    resolveUcFirst();
}

d.addEventListener("DOMContentLoaded", function(event) {

    const swalWithBootstrapButtons = Swal.mixin({
        customClass: {
            confirmButton: 'btn btn-primary me-3',
            cancelButton: 'btn btn-gray'
        },
        buttonsStyling: false
    });

    var themeSettingsEl = document.getElementById('theme-settings');
    var themeSettingsExpandEl = document.getElementById('theme-settings-expand');

    if (themeSettingsEl) {

        var themeSettingsCollapse = new bootstrap.Collapse(themeSettingsEl, {
            show: true,
            toggle: false
        });

        if (window.localStorage.getItem('settings_expanded') === 'true') {
            themeSettingsCollapse.show();
            themeSettingsExpandEl.classList.remove('show');
        } else {
            themeSettingsCollapse.hide();
            themeSettingsExpandEl.classList.add('show');
        }

        themeSettingsEl.addEventListener('hidden.bs.collapse', function() {
            themeSettingsExpandEl.classList.add('show');
            window.localStorage.setItem('settings_expanded', false);
        });

        themeSettingsExpandEl.addEventListener('click', function() {
            themeSettingsExpandEl.classList.remove('show');
            window.localStorage.setItem('settings_expanded', true);
            setTimeout(function() {
                themeSettingsCollapse.show();
            }, 300);
        });
    }

    // options
    const breakpoints = {
        sm: 540,
        md: 720,
        lg: 960,
        xl: 1140
    };

    var sidebar = document.getElementById('sidebarMenu')
    if (sidebar && d.body.clientWidth < breakpoints.lg) {
        sidebar.addEventListener('shown.bs.collapse', function() {
            document.querySelector('body').style.position = 'fixed';
        });
        sidebar.addEventListener('hidden.bs.collapse', function() {
            document.querySelector('body').style.position = 'relative';
        });
    }

    var iconNotifications = d.querySelector('.notification-bell');
    if (iconNotifications) {
        iconNotifications.addEventListener('shown.bs.dropdown', function() {
            iconNotifications.classList.remove('unread');
        });
    }

    [].slice.call(d.querySelectorAll('[data-background]')).map(function(el) {
        el.style.background = 'url(' + el.getAttribute('data-background') + ')';
    });

    [].slice.call(d.querySelectorAll('[data-background-lg]')).map(function(el) {
        if (document.body.clientWidth > breakpoints.lg) {
            el.style.background = 'url(' + el.getAttribute('data-background-lg') + ')';
        }
    });

    [].slice.call(d.querySelectorAll('[data-background-color]')).map(function(el) {
        el.style.background = 'url(' + el.getAttribute('data-background-color') + ')';
    });

    [].slice.call(d.querySelectorAll('[data-color]')).map(function(el) {
        el.style.color = 'url(' + el.getAttribute('data-color') + ')';
    });

    //Tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })


    // Popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl)
    })


    // Datepicker
    var datepickers = [].slice.call(d.querySelectorAll('[data-datepicker]'))
    var datepickersList = datepickers.map(function(el) {
        return new Datepicker(el, {
            buttonClass: 'btn'
        });
    })

    if (d.querySelector('.input-slider-container')) {
        [].slice.call(d.querySelectorAll('.input-slider-container')).map(function(el) {
            var slider = el.querySelector(':scope .input-slider');
            var sliderId = slider.getAttribute('id');
            var minValue = slider.getAttribute('data-range-value-min');
            var maxValue = slider.getAttribute('data-range-value-max');

            var sliderValue = el.querySelector(':scope .range-slider-value');
            var sliderValueId = sliderValue.getAttribute('id');
            var startValue = sliderValue.getAttribute('data-range-value-low');

            var c = d.getElementById(sliderId),
                id = d.getElementById(sliderValueId);

            noUiSlider.create(c, {
                start: [parseInt(startValue)],
                connect: [true, false],
                //step: 1000,
                range: {
                    'min': [parseInt(minValue)],
                    'max': [parseInt(maxValue)]
                }
            });
        });
    }

    if (d.getElementById('input-slider-range')) {
        var c = d.getElementById("input-slider-range"),
            low = d.getElementById("input-slider-range-value-low"),
            e = d.getElementById("input-slider-range-value-high"),
            f = [d, e];

        noUiSlider.create(c, {
            start: [parseInt(low.getAttribute('data-range-value-low')), parseInt(e.getAttribute('data-range-value-high'))],
            connect: !0,
            tooltips: true,
            range: {
                min: parseInt(c.getAttribute('data-range-value-min')),
                max: parseInt(c.getAttribute('data-range-value-max'))
            }
        }), c.noUiSlider.on("update", function(a, b) {
            f[b].textContent = a[b]
        });
    }

    if (d.getElementById('loadOnClick')) {
        d.getElementById('loadOnClick').addEventListener('click', function() {
            var button = this;
            var loadContent = d.getElementById('extraContent');
            var allLoaded = d.getElementById('allLoadedText');

            button.classList.add('btn-loading');
            button.setAttribute('disabled', 'true');

            setTimeout(function() {
                loadContent.style.display = 'block';
                button.style.display = 'none';
                allLoaded.style.display = 'block';
            }, 1500);
        });
    }

    var scroll = new SmoothScroll('a[href*="#"]', {
        speed: 500,
        speedAsDuration: true
    });

    if (d.querySelector('.current-year')) {
        d.querySelector('.current-year').textContent = new Date().getFullYear();
    }

    // Glide JS

    if (d.querySelector('.glide')) {
        new Glide('.glide', {
            type: 'carousel',
            startAt: 0,
            perView: 3
        }).mount();
    }

    if (d.querySelector('.glide-testimonials')) {
        new Glide('.glide-testimonials', {
            type: 'carousel',
            startAt: 0,
            perView: 1,
            autoplay: 2000
        }).mount();
    }

    if (d.querySelector('.glide-clients')) {
        new Glide('.glide-clients', {
            type: 'carousel',
            startAt: 0,
            perView: 5,
            autoplay: 2000
        }).mount();
    }

    if (d.querySelector('.glide-news-widget')) {
        new Glide('.glide-news-widget', {
            type: 'carousel',
            startAt: 0,
            perView: 1,
            autoplay: 2000
        }).mount();
    }

    if (d.querySelector('.glide-autoplay')) {
        new Glide('.glide-autoplay', {
            type: 'carousel',
            startAt: 0,
            perView: 3,
            autoplay: 2000
        }).mount();
    }

    // Pricing countup
    var billingSwitchEl = d.getElementById('billingSwitch');
    if (billingSwitchEl) {
        const countUpStandard = new countUp.CountUp('priceStandard', 99, { startVal: 199 });
        const countUpPremium = new countUp.CountUp('pricePremium', 199, { startVal: 299 });

        billingSwitchEl.addEventListener('change', function() {
            if (billingSwitch.checked) {
                countUpStandard.start();
                countUpPremium.start();
            } else {
                countUpStandard.reset();
                countUpPremium.reset();
            }
        });
    }

    resolveAllQueries();
});

