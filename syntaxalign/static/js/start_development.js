let currentStep = 1;
const totalSteps = 3;

// Initialize form on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeForm();
    setupEventListeners();
});

function initializeForm() {
    // Show first step
    showStep(1);
    updateProgressBar();
}

function setupEventListeners() {
    // Project type selection
    const projectTypeRadios = document.querySelectorAll('input[name="project_type"]');
    projectTypeRadios.forEach(radio => {
        radio.addEventListener('change', handleProjectTypeChange);
    });

    // Navigation buttons
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const submitBtn = document.getElementById('submitBtn');

    if (prevBtn) prevBtn.addEventListener('click', () => changeStep(-1));
    if (nextBtn) nextBtn.addEventListener('click', () => changeStep(1));
    if (submitBtn) submitBtn.addEventListener('click', handleSubmit);

    // Form input validation
    setupInputValidation();
}

function setupInputValidation() {
    const inputs = document.querySelectorAll('input[type="email"], input[type="text"], textarea, select');
    inputs.forEach(input => {
        input.addEventListener('blur', () => validateField(input));
        input.addEventListener('focus', () => clearFieldError(input));
    });
}

function handleProjectTypeChange(e) {
    const projectType = e.target.value;
    const businessFields = document.getElementById('businessFields');
    const personalFields = document.getElementById('personalFields');

    if (projectType === 'business') {
        if (businessFields) businessFields.style.display = 'block';
        if (personalFields) personalFields.style.display = 'none';
    } else if (projectType === 'personal') {
        if (businessFields) businessFields.style.display = 'none';
        if (personalFields) personalFields.style.display = 'block';
    }
}

function changeStep(direction) {
    const newStep = currentStep + direction;

    if (newStep < 1 || newStep > totalSteps) return;

    // Validate current step before proceeding
    if (direction > 0 && !validateStep(currentStep)) {
        showValidationErrors();
        return;
    }

    // For step 2 to step 3, populate review section
    if (currentStep === 2 && newStep === 3) {
        populateReviewSection();
    }

    currentStep = newStep;
    showStep(currentStep);
    updateProgressBar();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function showStep(stepNumber) {
    // Hide all steps
    const steps = document.querySelectorAll('.form-step');
    steps.forEach(step => {
        step.classList.remove('active');
    });

    // Show current step
    const activeStep = document.querySelector(`[data-step="${stepNumber}"]`);
    if (activeStep) {
        activeStep.classList.add('active');
    }

    // Update button visibility
    updateNavigationButtons();
}

function updateNavigationButtons() {
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const submitBtn = document.getElementById('submitBtn');

    if (prevBtn) {
        prevBtn.style.display = currentStep > 1 ? 'inline-flex' : 'none';
    }

    if (nextBtn) {
        nextBtn.style.display = currentStep < totalSteps ? 'inline-flex' : 'none';
    }

    if (submitBtn) {
        submitBtn.style.display = currentStep === totalSteps ? 'inline-flex' : 'none';
    }
}

function updateProgressBar() {
    const progressBar = document.querySelector('.progress-bar');
    const steps = document.querySelectorAll('.step');

    if (progressBar) {
        const progressWidth = (currentStep / totalSteps) * 100;
        progressBar.style.width = progressWidth + '%';
    }

    // Update step styles
    steps.forEach((step, index) => {
        if (index + 1 <= currentStep) {
            step.classList.add('active');
        } else {
            step.classList.remove('active');
        }
    });
}

function validateStep(stepNumber) {
    clearAllErrors();

    if (stepNumber === 1) {
        return validateProjectTypeStep();
    } else if (stepNumber === 2) {
        return validateDetailsStep();
    }
    return true;
}

function validateProjectTypeStep() {
    const projectTypeRadios = document.querySelectorAll('input[name="project_type"]');
    const isChecked = Array.from(projectTypeRadios).some(radio => radio.checked);

    if (!isChecked) {
        showError('Please select a project type');
        return false;
    }

    return true;
}

function validateDetailsStep() {
    let isValid = true;
    const projectType = document.querySelector('input[name="project_type"]:checked')?.value;

    // Common fields validation
    const emailInput = document.querySelector('input[name="email"]');
    const projectNameInput = document.querySelector('input[name="project_name"]');
    const descriptionInput = document.querySelector('textarea[name="description"]');
    const budgetInput = document.querySelector('select[name="budget"]');

    if (emailInput && !validateField(emailInput)) isValid = false;
    if (projectNameInput && !validateField(projectNameInput)) isValid = false;
    if (descriptionInput && !validateField(descriptionInput)) isValid = false;
    if (budgetInput && !budgetInput.value) {
        setFieldError(budgetInput, 'Please select a budget range');
        isValid = false;
    }

    // Project type specific validation
    if (projectType === 'business') {
        const companyInput = document.querySelector('input[name="company_name"]');
        const industryInput = document.querySelector('select[name="industry"]');
        if (companyInput && !validateField(companyInput)) isValid = false;
        if (industryInput && !industryInput.value) {
            setFieldError(industryInput, 'Please select an industry');
            isValid = false;
        }
    } else if (projectType === 'personal') {
        const experienceInput = document.querySelector('select[name="experience_level"]');
        if (experienceInput && !experienceInput.value) {
            setFieldError(experienceInput, 'Please select your experience level');
            isValid = false;
        }
    }

    return isValid;
}

function validateField(field) {
    if (!field) return true;

    const value = field.value.trim();
    const type = field.getAttribute('type') || field.tagName.toLowerCase();
    const name = field.getAttribute('name');
    const requiresEmail = field.type === 'email' || name === 'email';

    if (!value) {
        const label = field.getAttribute('placeholder') || field.getAttribute('name');
        setFieldError(field, `${label} is required`);
        return false;
    }

    if (requiresEmail && !isValidEmail(value)) {
        setFieldError(field, 'Please enter a valid email address');
        return false;
    }

    if (type === 'textarea' && value.length < 10) {
        setFieldError(field, 'Please enter at least 10 characters');
        return false;
    }

    clearFieldError(field);
    return true;
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function setFieldError(field, message) {
    const formGroup = field.closest('.form-group');
    if (!formGroup) return;

    formGroup.classList.add('error');
    let errorMsg = formGroup.querySelector('.error-message');
    if (!errorMsg) {
        errorMsg = document.createElement('span');
        errorMsg.className = 'error-message';
        formGroup.appendChild(errorMsg);
    }
    errorMsg.textContent = message;
}

function clearFieldError(field) {
    const formGroup = field.closest('.form-group');
    if (!formGroup) return;

    formGroup.classList.remove('error');
    const errorMsg = formGroup.querySelector('.error-message');
    if (errorMsg) {
        errorMsg.textContent = '';
    }
}

function clearAllErrors() {
    const errorFormGroups = document.querySelectorAll('.form-group.error');
    errorFormGroups.forEach(group => {
        group.classList.remove('error');
        const errorMsg = group.querySelector('.error-message');
        if (errorMsg) {
            errorMsg.textContent = '';
        }
    });
}

function showValidationErrors() {
    const errorAlert = document.createElement('div');
    errorAlert.className = 'validation-error-alert';
    errorAlert.textContent = 'Please fill in all required fields correctly.';
    errorAlert.style.cssText = `
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        color: #ef4444;
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 20px;
        font-size: 13px;
        font-weight: 600;
        animation: slideInError 0.3s ease;
    `;

    const formStep = document.querySelector('.form-step.active');
    if (!formStep) return;

    const existingAlert = formStep.querySelector('.validation-error-alert');
    if (existingAlert) existingAlert.remove();

    formStep.insertBefore(errorAlert, formStep.firstChild);

    setTimeout(() => {
        errorAlert.remove();
    }, 5000);
}

function showError(message) {
    const errorAlert = document.createElement('div');
    errorAlert.className = 'validation-error-alert';
    errorAlert.textContent = message;
    errorAlert.style.cssText = `
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        color: #ef4444;
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 20px;
        font-size: 13px;
        font-weight: 600;
        animation: slideInError 0.3s ease;
    `;

    const formStep = document.querySelector('.form-step.active');
    if (!formStep) return;

    const existingAlert = formStep.querySelector('.validation-error-alert');
    if (existingAlert) existingAlert.remove();

    formStep.insertBefore(errorAlert, formStep.firstChild);

    setTimeout(() => {
        errorAlert.remove();
    }, 5000);
}

function populateReviewSection() {
    const projectType = document.querySelector('input[name="project_type"]:checked')?.value;
    const email = document.querySelector('input[name="email"]')?.value;
    const projectName = document.querySelector('input[name="project_name"]')?.value;
    const description = document.querySelector('textarea[name="description"]')?.value;
    const budget = document.querySelector('select[name="budget"]')?.value;
    const companyName = document.querySelector('input[name="company_name"]')?.value;
    const industry = document.querySelector('select[name="industry"]')?.value;
    const experienceLevel = document.querySelector('select[name="experience_level"]')?.value;
    const timeline = document.querySelector('select[name="timeline"]')?.value;

    // Update review sections
    updateReviewSection('projectTypeReview', {
        'Project Type': projectType === 'business' ? 'Business' : 'Personal'
    });

    updateReviewSection('projectDetailsReview', {
        'Email': email,
        'Project Name': projectName,
        'Description': description?.substring(0, 100) + (description?.length > 100 ? '...' : ''),
        'Budget Range': formatBudgetText(budget),
        'Timeline': formatTimelineText(timeline)
    });

    if (projectType === 'business') {
        updateReviewSection('businessInfoReview', {
            'Company Name': companyName,
            'Industry': formatIndustryText(industry)
        });
    } else {
        updateReviewSection('personalInfoReview', {
            'Experience Level': formatExperienceText(experienceLevel)
        });
    }
}

function updateReviewSection(sectionId, data) {
    const section = document.getElementById(sectionId);
    if (!section) return;

    const content = Object.entries(data)
        .filter(([key, value]) => value && value.trim())
        .map(([key, value]) => `<p><strong>${key}:</strong> ${value}</p>`)
        .join('');

    section.innerHTML = content || '<p>No information provided</p>';
}

function formatBudgetText(budget) {
    const budgetMap = {
        'under-500': 'Under $500',
        '500-1000': '$500 - $1,000',
        '1000-5000': '$1,000 - $5,000',
        '5000-10000': '$5,000 - $10,000',
        'over-10000': 'Over $10,000'
    };
    return budgetMap[budget] || budget;
}

function formatTimelineText(timeline) {
    const timelineMap = {
        'urgent': 'Urgent (1-2 weeks)',
        'flexible': 'Flexible',
        'not-decided': 'Not decided yet',
        'asap': 'ASAP'
    };
    return timelineMap[timeline] || timeline;
}

function formatIndustryText(industry) {
    const industryMap = {
        'tech': 'Technology',
        'finance': 'Finance',
        'healthcare': 'Healthcare',
        'retail': 'Retail',
        'education': 'Education',
        'other': 'Other'
    };
    return industryMap[industry] || industry;
}

function formatExperienceText(experience) {
    const experienceMap = {
        'beginner': 'Beginner',
        'intermediate': 'Intermediate',
        'advanced': 'Advanced'
    };
    return experienceMap[experience] || experience;
}

function handleSubmit(e) {
    e.preventDefault();

    // Validate all steps one more time
    if (!validateStep(1) || !validateStep(2)) {
        showError('Please review and correct any errors');
        currentStep = 1;
        showStep(1);
        updateProgressBar();
        return;
    }

    // Get form data
    const formData = new FormData(document.getElementById('startDevForm') || document.querySelector('.dev-form'));

    // Add success message
    const form = document.querySelector('.dev-form');
    const successMessage = document.createElement('div');
    successMessage.style.cssText = `
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #10b981;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 20px;
        font-size: 14px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 10px;
        animation: slideInError 0.3s ease;
    `;
    successMessage.innerHTML = '✓ Your request has been submitted! We\'ll get back to you soon.';

    if (form) {
        form.insertBefore(successMessage, form.firstChild);
    }

    // Disable submit button
    const submitBtn = document.getElementById('submitBtn');
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = 'Submitted!';
    }

    // In a real app, you would submit to Django backend here
    console.log('Form submitted with data:', Object.fromEntries(formData));

    // Optional: Reset after delay
    setTimeout(() => {
        // window.location.href = '/'; // Redirect to home or success page
    }, 2000);
}

// Optional: Add Enter key support for form navigation
document.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && e.target.matches('input, textarea, select')) {
        if (currentStep < totalSteps) {
            const nextBtn = document.getElementById('nextBtn');
            if (nextBtn && nextBtn.style.display !== 'none') {
                e.preventDefault();
                changeStep(1);
            }
        }
    }
});
