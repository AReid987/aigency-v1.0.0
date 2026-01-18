// Modal Management
const loginModal = document.getElementById('loginModal');
const signupModal = document.getElementById('signupModal');
const betaModal = document.getElementById('betaModal');

const loginBtn = document.getElementById('loginBtn');
const signupBtn = document.getElementById('signupBtn');
const betaBtn = document.getElementById('betaBtn');

const closeLogin = document.getElementById('closeLogin');
const closeSignup = document.getElementById('closeSignup');
const closeBeta = document.getElementById('closeBeta');

const switchToSignup = document.getElementById('switchToSignup');
const switchToLogin = document.getElementById('switchToLogin');

const heroInput = document.getElementById('heroInput');
const submitBtn = document.getElementById('submitBtn');

// Modal Toggle Functions
function openModal(modal) {
    closeAllModals();
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeModal(modal) {
    modal.classList.remove('active');
    document.body.style.overflow = '';
}

function closeAllModals() {
    [loginModal, signupModal, betaModal].forEach(modal => {
        modal.classList.remove('active');
    });
    document.body.style.overflow = '';
}

// Event Listeners for Modal Controls
loginBtn.addEventListener('click', () => openModal(loginModal));
signupBtn.addEventListener('click', () => openModal(signupModal));
betaBtn.addEventListener('click', () => openModal(betaModal));

closeLogin.addEventListener('click', () => closeModal(loginModal));
closeSignup.addEventListener('click', () => closeModal(signupModal));
closeBeta.addEventListener('click', () => closeModal(betaModal));

switchToSignup.addEventListener('click', (e) => {
    e.preventDefault();
    openModal(signupModal);
});

switchToLogin.addEventListener('click', (e) => {
    e.preventDefault();
    openModal(loginModal);
});

// Close modals when clicking outside
[loginModal, signupModal, betaModal].forEach(modal => {
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeModal(modal);
        }
    });
});

// Close modals on escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeAllModals();
    }
});

// Form Submissions
const loginForm = document.getElementById('loginForm');
const signupForm = document.getElementById('signupForm');
const betaForm = document.getElementById('betaForm');

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    // TODO: Implement actual login logic
    console.log('Login attempt:', { email, password });

    // Simulate success
    alert('Login functionality will be implemented in the beta version');
    closeModal(loginModal);
});

signupForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('signupName').value;
    const email = document.getElementById('signupEmail').value;
    const password = document.getElementById('signupPassword').value;

    // TODO: Implement actual signup logic
    console.log('Signup attempt:', { name, email, password });

    // Simulate success
    alert('Signup functionality will be implemented in the beta version');
    closeModal(signupModal);
});

betaForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('betaName').value;
    const email = document.getElementById('betaEmail').value;
    const company = document.getElementById('betaCompany').value;
    const useCase = document.getElementById('betaUseCase').value;

    // TODO: Implement actual beta signup logic
    console.log('Beta signup:', { name, email, company, useCase });

    // Simulate success
    alert('Thank you for your interest! We\'ll be in touch soon.');
    closeModal(betaModal);
});

// Hero Input Handling
submitBtn.addEventListener('click', () => {
    const input = heroInput.value.trim();
    if (input) {
        // TODO: Implement actual input handling
        console.log('Input submitted:', input);
        openModal(betaModal);
    }
});

heroInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        submitBtn.click();
    }
});

// Theme Toggle
const themeToggle = document.getElementById('themeToggle');
let isDark = true;

themeToggle.addEventListener('click', () => {
    isDark = !isDark;
    themeToggle.textContent = isDark ? '🌙' : '☀️';
    // TODO: Implement actual theme switching when light theme is designed
});

// Animation on Scroll
const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe demo section for animation
const demoSection = document.querySelector('.demo-section');
observer.observe(demoSection);
