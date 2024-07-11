document.addEventListener('DOMContentLoaded', (event) => {
    setTimeout(() => {
        // document.getElementById('intro-screen').classList.add('hidden');
        document.getElementById('input-screen').classList.remove('hidden');
    }, 1000);
});

function submitName() {
    const name = document.getElementById('user-name').value;
    window.location.href = `story.html?name=${name}`;
}

function startStory() {
    window.location.href = 'story.html';
}

function enterCave() {
    window.location.href = 'cave.html';
}

function goToVillage() {
    window.location.href = 'village.html';
}

function solveRiddle() {
    window.location.href = 'riddle.html';
}

function exploreFurther() {
    window.location.href = 'explore.html';
}

