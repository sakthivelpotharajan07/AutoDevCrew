const apiEndpoint = '/api/live-scores';
const sportsTypes = ['football', 'basketball', 'tennis'];

let currentSport = sportsTypes[0];

function getLiveScores() {
    fetch(apiEndpoint)
        .then(response => response.json())
        .then(data => {
            const scoresContainer = document.getElementById('live-scores');
            scoresContainer.innerHTML = '';
            data.forEach(score => {
                if (score.sport === currentSport) {
                    const scoreElement = document.createElement('div');
                    scoreElement.textContent = `${score.homeTeam} ${score.homeScore} - ${score.awayScore} ${score.awayTeam}`;
                    scoresContainer.appendChild(scoreElement);
                }
            });
        });
}

function changeSport(sport) {
    currentSport = sport;
    getLiveScores();
}

document.addEventListener('DOMContentLoaded', () => {
    getLiveScores();
    const sportButtons = document.querySelectorAll('.sport-button');
    sportButtons.forEach(button => {
        button.addEventListener('click', event => {
            changeSport(event.target.textContent.toLowerCase());
        });
    });
});