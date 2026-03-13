
AOS.init();




const toggle = document.getElementById("themeToggle");
const icon = toggle.querySelector("i");

toggle.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");

    // Toggle the icon
    if (document.body.classList.contains("dark-mode")) {
        icon.classList.replace("bi-moon", "bi-sun");
        toggle.classList.replace("btn-outline-dark", "btn-outline-light");
    } else {
        icon.classList.replace("bi-sun", "bi-moon");
        toggle.classList.replace("btn-outline-light", "btn-outline-dark");
    }
});

// Educational Modules Popover Logic
const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
const popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl, {
        placement: 'top'
    })
})

// Toast Notification Logic
const toastContainer = document.getElementById('toastContainer');

function showToast(title, message, iconClass = 'bi-info-circle') {
    if (!toastContainer) return;

    const toast = document.createElement('div');
    toast.className = 'custom-toast';
    toast.innerHTML = `
        <i class="bi ${iconClass}"></i>
        <div class="custom-toast-content">
            <h6>${title}</h6>
            <p>${message}</p>
        </div>
    `;

    toastContainer.appendChild(toast);

    // Force reflow and show
    setTimeout(() => {
        toast.classList.add('show');
    }, 10);

    // Remove after 4 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 400);
    }, 4000);
}

// Support Links Event Listeners
const supportLinks = {
    'helpCenter': { title: 'Help Center', message: 'Our experts are available 24/7 to assist you with any financial queries.' },
    'privacyPolicy': { title: 'Privacy Policy', message: 'Your data security is our top priority. We use bank-grade encryption.' },
    'termsOfUse': { title: 'Terms of Use', message: 'By using Money Mentor, you agree to our standard terms of financial service.' },
    'careers': { title: 'Careers', message: 'We are looking for talented developers and financial analysts to join our team!' }
};

Object.entries(supportLinks).forEach(([id, info]) => {
    const el = document.getElementById(id);
    if (el) {
        el.addEventListener('click', (e) => {
            e.preventDefault();
            showToast(info.title, info.message);
        });
    }
});


