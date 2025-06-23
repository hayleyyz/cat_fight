const form = document.getElementById('fighter-form');
const videoFileInput = document.getElementById('video-file');
const inputSection = document.getElementById('input-section');
const loadingSection = document.getElementById('loading-section');
const resultSection = document.getElementById('result-section');
const errorSection = document.getElementById('error-section');
const errorMessage = document.getElementById('error-message');

form.addEventListener('submit', async (event) => {
    event.preventDefault(); 
    
    const videoFile = videoFileInput.files[0];
    if (!videoFile) {
        displayError("Please select a video file first.");
        return;
    }
    console.log(`Form submitted. Video File: ${videoFile.name}`);

    const formData = new FormData();
    formData.append('video', videoFile);

    inputSection.classList.add('hidden');
    resultSection.classList.add('hidden');
    errorSection.classList.add('hidden');
    loadingSection.classList.remove('hidden');

    try {
        console.log('Sending request to backend /generate-profile endpoint...');
        const response = await fetch('/generate-profile', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! Status: ${response.status}`);
        }

        const profiles = await response.json();
        console.log('Successfully received data from backend:', profiles);
        
        if (profiles.length === 0) {
            throw new Error("No cats could be detected in the provided video.");
        }

        displayResults(profiles);

    } catch (error) {
        console.error('An error occurred:', error);
        displayError(error.message);
    }
});

function createCharacterCardHTML(profile, index) {
    return `
        <div class="card character-card" style="animation-delay: ${index * 0.2}s;">
            <h2 id="cat-name-${index}">${profile.name.toUpperCase()}</h2>
            <div class="vs-style-image">
                <img id="cat-image-${index}" src="data:image/jpeg;base64,${profile.image_frame}" alt="Fighter: ${profile.name}">
            </div>
            <div class="stats-grid">
                <div class="stat-item">
                    <span class="stat-label">ATTACK</span>
                    <div class="stat-bar"><div id="attack-bar-${index}" class="stat-bar-fill"></div></div>
                    <span id="attack-value-${index}" class="stat-value">${profile.attack}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">DEFENSE</span>
                    <div class="stat-bar"><div id="defense-bar-${index}" class="stat-bar-fill"></div></div>
                    <span id="defense-value-${index}" class="stat-value">${profile.defense}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">SPEED</span>
                    <div class="stat-bar"><div id="speed-bar-${index}" class="stat-bar-fill"></div></div>
                    <span id="speed-value-${index}" class="stat-value">${profile.speed}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">AGILITY</span>
                    <div class="stat-bar"><div id="agility-bar-${index}" class="stat-bar-fill"></div></div>
                    <span id="agility-value-${index}" class="stat-value">${profile.agility}</span>
                </div>
            </div>
            <div class="special-move">
                <h3>SPECIAL MOVE</h3>
                <p id="special-move-name-${index}">${profile.special_move}</p>
            </div>
            <div class="catchphrase">
                <p id="cat-catchphrase-${index}">"${profile.catchphrase}"</p>
            </div>
        </div>
    `;
}

function displayResults(profiles) {
    console.log('Rendering results for', profiles.length, 'fighters...');
    
    resultSection.innerHTML = '';
    
    profiles.forEach((profile, index) => {
        const cardHTML = createCharacterCardHTML(profile, index);
        resultSection.insertAdjacentHTML('beforeend', cardHTML);
    });

    loadingSection.classList.add('hidden');
    resultSection.classList.remove('hidden');

    setTimeout(() => {
        console.log('Animating all stat bars...');
        profiles.forEach((profile, index) => {
            document.getElementById(`attack-bar-${index}`).style.width = `${profile.attack}%`;
            document.getElementById(`defense-bar-${index}`).style.width = `${profile.defense}%`;
            document.getElementById(`speed-bar-${index}`).style.width = `${profile.speed}%`;
            document.getElementById(`agility-bar-${index}`).style.width = `${profile.agility}%`;
        });
    }, 100);
}

function displayError(message) {
    loadingSection.classList.add('hidden');
    errorMessage.textContent = message;
    errorSection.classList.remove('hidden');
}
