// auth.js
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('signin-form');
    const profileBtn = document.getElementById('profile-btn');
    const profileInfo = document.querySelector('.profile-info');
    const apsitWikiFeature = document.querySelector('.feature-block[href="http://127.0.0.1:8000/"]');
    
    // Check if user is logged in on page load
    if (sessionStorage.getItem('isLoggedIn') === 'true') {
        displayLoggedInState();
    } else {
        hideAPSITWikiFeature();
    }

    form?.addEventListener('submit', function (event) {
        event.preventDefault();
        // Simulate authentication (Replace with actual Moodle authentication logic)
        const moodleId = form.elements['Moodle Id'].value;
        const password = form.elements['password'].value;
        
        if (moodleId && password) { // Dummy check; replace with real validation
            sessionStorage.setItem('isLoggedIn', 'true');
            sessionStorage.setItem('moodleId', moodleId);
            window.location.href = 'dashboard.html'; // Redirect to dashboard after login
        } else {
            alert('Invalid credentials');
        }
    });

    profileBtn?.addEventListener('click', function () {
        if (sessionStorage.getItem('isLoggedIn') === 'true') {
            displayLoggedInState();
        } else {
            window.location.href = 'signin.html';
        }
    });

    function displayLoggedInState() {
        profileBtn.textContent = sessionStorage.getItem('moodleId');
        apsitWikiFeature.style.display = 'block'; // Show APSITwiki feature
        profileInfo.innerHTML = `<p>${sessionStorage.getItem('moodleId')}</p>`;
    }

    function hideAPSITWikiFeature() {
        apsitWikiFeature.style.display = 'none'; // Hide APSITwiki feature
    }

    document.getElementById('close-btn')?.addEventListener('click', function () {
        sessionStorage.clear(); // Clear session on signout
        window.location.href = 'signin.html'; // Redirect to sign-in page
    });
});
