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
