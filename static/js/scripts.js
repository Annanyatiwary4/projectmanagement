// Toggle Between Projects and Progress Sections
const projectsTab = document.getElementById('projects-tab');
const progressTab = document.getElementById('progress-tab');
const projectsSection = document.getElementById('projects-section');
const progressSection = document.getElementById('progress-section');

// Event Listeners for Sidebar Tabs
projectsTab.addEventListener('click', () => {
    projectsSection.classList.add('active');
    progressSection.classList.remove('active');
});

progressTab.addEventListener('click', () => {
    progressSection.classList.add('active');
    projectsSection.classList.remove('active');
});
