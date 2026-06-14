// Telegram Bot Configuration
const BOT_TOKEN = "PUT_BOT_TOKEN_HERE";
const CHAT_ID = "PUT_CHAT_ID_HERE";

// Services Data (Using Emojis)
const servicesData = [
    {
        id: "install",
        title: "تركيب سبلت جديد",
        emoji: "🔧",
        pricing: [
            { desc: "شد سبلت 2 طن", price: "50,000 دينار عراقي" },
            { desc: "شد سبلت 3 طن كنتوري أو جداري", price: "75,000 دينار عراقي" }
        ]
    },
    {
        id: "clean",
        title: "غسل وتنظيف",
        emoji: "🧼",
        pricing: [
            { desc: "غسل سبلت 2 طن جداري موقعي", price: "35,000 لسبلت واحد / 25,000 لأكثر من سبلت" },
            { desc: "غسل سبلت 2 طن جداري تفصيخ", price: "50,000 دينار عراقي" },
            { desc: "غسل سبلت كنتوري 3 طن فقط الراديتر والأجزاء المهمة", price: "35,000 دينار عراقي" },
            { desc: "غسل سبلت كنتوري 3 طن تفصيخ", price: "65,000 دينار عراقي" }
        ]
    },
    {
        id: "move",
        title: "نقل (فتح وشد)",
        emoji: "🚚",
        pricing: [
            { desc: "فتح وشد سبلت 2 طن جداري لنفس المكان", price: "75,000 دينار عراقي" },
            { desc: "فتح وشد + غسل سبلت 2 طن جداري لنفس المكان", price: "85,000 دينار عراقي" },
            { desc: "فتح وشد + غسل ونقل سبلت 2 طن جداري لمكان آخر", price: "90,000 دينار عراقي" },
            { desc: "فتح وشد سبلت 3 طن كنتوري", price: "100,000 دينار عراقي" },
            { desc: "فتح وشد + غسل ونقل سبلت 3 طن كنتوري لمكان آخر", price: "125,000 دينار عراقي" }
        ]
    },
    {
        id: "gas",
        title: "شحن غاز",
        emoji: "❄️",
        pricing: [
            { desc: "شحن غاز 2 طن (غاز 22)", price: "80,000 دينار عراقي" },
            { desc: "شحن غاز 2 طن (غاز 410)", price: "90,000 دينار عراقي" },
            { desc: "شحن غاز 3 طن كنتوري (غاز 22)", price: "110,000 دينار عراقي" },
            { desc: "شحن غاز 3 طن كنتوري (غاز 410)", price: "125,000 دينار عراقي" }
        ]
    },
    {
        id: "maintenance",
        title: "صيانة",
        emoji: "🛠️",
        pricing: [],
        customNote: "يتم تحديد سعر الصيانة حسب الحالة بعد الفحص."
    }
];

// DOM Elements
const servicesList = document.getElementById('servicesList');

// Modals
const serviceModal = document.getElementById('serviceModal');
const profileModal = document.getElementById('profileModal');
const openProfileBtn = document.getElementById('openProfileBtn');
const closeServiceModalBtn = document.querySelector('.close-service-modal');
const closeProfileModalBtn = document.querySelector('.close-profile-modal');

// Service Modal Elements
const modalTitle = document.getElementById('modalTitle');
const modalEmoji = document.getElementById('modalEmoji');
const modalPricing = document.getElementById('modalPricing');

// Accordion
const accordionBtn = document.getElementById('accordionBtn');
const accordionContent = document.getElementById('accordionContent');

// Form
const selectedServiceInput = document.getElementById('selectedService');
const requestForm = document.getElementById('requestForm');
const submitBtn = document.getElementById('submitBtn');
const successOverlay = document.getElementById('successOverlay');

// Extras
const copyPhoneBtn = document.getElementById('copyPhoneBtn');
const toast = document.getElementById('toast');
const currentYearSpan = document.getElementById('currentYear');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    currentYearSpan.textContent = new Date().getFullYear();
    renderServices();

    // Event Listeners for Modals
    openProfileBtn.addEventListener('click', () => openModal(profileModal));
    closeProfileModalBtn.addEventListener('click', () => closeModal(profileModal));
    closeServiceModalBtn.addEventListener('click', () => closeModal(serviceModal));
    
    // Close modals on clicking outside
    window.addEventListener('click', (e) => {
        if (e.target === serviceModal) closeModal(serviceModal);
        if (e.target === profileModal) closeModal(profileModal);
    });

    // Other Event Listeners
    accordionBtn.addEventListener('click', toggleAccordion);
    copyPhoneBtn.addEventListener('click', copyPhoneNumber);
    requestForm.addEventListener('submit', handleFormSubmit);
});

// Render Services
function renderServices() {
    servicesList.innerHTML = '';
    
    servicesData.forEach(service => {
        const card = document.createElement('div');
        card.className = 'service-card';
        card.onclick = () => openServiceModal(service);
        
        card.innerHTML = `
            <div class="service-emoji">${service.emoji}</div>
            <div class="service-details">
                <h3 class="service-title">${service.title}</h3>
            </div>
            <div class="service-action">
                <i class="fa-solid fa-chevron-left"></i>
            </div>
        `;
        
        servicesList.appendChild(card);
    });
}

// Modal Logic
function openModal(modalEl) {
    modalEl.style.display = 'block';
    setTimeout(() => modalEl.classList.add('show'), 10);
    document.body.style.overflow = 'hidden';
}

function closeModal(modalEl) {
    modalEl.classList.remove('show');
    setTimeout(() => {
        modalEl.style.display = 'none';
        // Reset specific elements if it's the service modal
        if (modalEl === serviceModal) {
            requestForm.reset();
            accordionBtn.classList.remove('active');
            accordionContent.style.maxHeight = null;
        }
    }, 400); // Matches CSS transition time
    document.body.style.overflow = 'auto';
}

function openServiceModal(service) {
    modalTitle.textContent = service.title;
    modalEmoji.textContent = service.emoji;
    selectedServiceInput.value = service.title;
    
    // Reset Accordion
    accordionBtn.classList.remove('active');
    accordionContent.style.maxHeight = null;
    
    // Render Pricing
    let pricingHTML = '';
    if (service.pricing && service.pricing.length > 0) {
        service.pricing.forEach(item => {
            pricingHTML += `
                <div class="price-item">
                    <span class="price-desc">${item.desc}</span>
                    <span class="price-val">${item.price}</span>
                </div>
            `;
        });
    } else if (service.customNote) {
        pricingHTML = `
            <div class="pricing-note">
                <i class="fa-solid fa-circle-info"></i> ${service.customNote}
            </div>
        `;
    }
    modalPricing.innerHTML = pricingHTML;
    
    openModal(serviceModal);
}

// Accordion Logic
function toggleAccordion() {
    accordionBtn.classList.toggle('active');
    if (accordionContent.style.maxHeight) {
        accordionContent.style.maxHeight = null;
    } else {
        accordionContent.style.maxHeight = accordionContent.scrollHeight + "px";
        
        // Robust scrolling for mobile: explicitly scroll the modal body container
        setTimeout(() => {
            const modalBody = document.querySelector('#serviceModal .modal-body');
            const pricingWrapper = document.querySelector('.pricing-wrapper');
            
            // Calculate the position of the pricing wrapper relative to the modal body
            // We subtract a small padding (15px) so it looks neat
            const scrollTarget = pricingWrapper.offsetTop - 15;
            
            modalBody.scrollTo({
                top: scrollTarget,
                behavior: 'smooth'
            });
        }, 300); // 300ms delay to let the CSS accordion animation begin smoothly
    }
}

// Copy Phone Number
function copyPhoneNumber() {
    navigator.clipboard.writeText('07703906521').then(() => {
        showToast('تم نسخ رقم الهاتف بنجاح!', 'success');
    }).catch(err => {
        showToast('حدث خطأ أثناء النسخ', 'error');
    });
}

// Form Submission & Telegram Integration
async function handleFormSubmit(e) {
    e.preventDefault();
    
    if (BOT_TOKEN === "PUT_BOT_TOKEN_HERE" || CHAT_ID === "PUT_CHAT_ID_HERE") {
        showToast('يرجى إعداد بيانات البوت أولاً في الكود.', 'error');
        return;
    }

    const formData = new FormData(requestForm);
    const data = {
        service: formData.get('selectedService'),
        name: formData.get('customerName'),
        phone: formData.get('customerPhone'),
        notes: formData.get('customerNotes') || "لا يوجد"
    };

    const now = new Date();
    const dateStr = now.toLocaleDateString('ar-IQ');
    const timeStr = now.toLocaleTimeString('ar-IQ');

    const message = `
🔔 *طلب خدمة جديد*

🛠 *الخدمة:* ${data.service}
👤 *الاسم:* ${data.name}
📱 *الهاتف:* ${data.phone}
📝 *ملاحظات:* ${data.notes}

🕒 *الوقت:* ${dateStr} - ${timeStr}
    `;

    // Loading State
    const originalBtnContent = submitBtn.innerHTML;
    submitBtn.innerHTML = '<span>جاري الإرسال...</span> <i class="fa-solid fa-circle-notch fa-spin"></i>';
    submitBtn.disabled = true;

    try {
        const response = await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                chat_id: CHAT_ID,
                text: message,
                parse_mode: 'Markdown'
            })
        });

        const result = await response.json();

        if (result.ok) {
            // Show Success Overlay Animation
            successOverlay.classList.add('show');
            requestForm.reset();
            
            // Close everything after 2.5 seconds
            setTimeout(() => {
                successOverlay.classList.remove('show');
                closeModal(serviceModal);
            }, 2500);

        } else {
            throw new Error(result.description);
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('حدث خطأ. يرجى المحاولة مرة أخرى.', 'error');
    } finally {
        submitBtn.innerHTML = originalBtnContent;
        submitBtn.disabled = false;
    }
}

// Toast Notification
function showToast(message, type = 'success') {
    toast.textContent = message;
    toast.className = 'toast';
    toast.classList.add(type);
    
    void toast.offsetWidth; // Reflow
    toast.classList.add('show');
    
    setTimeout(() => toast.classList.remove('show'), 3000);
}
