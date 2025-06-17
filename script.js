const form = document.getElementById('complaintForm');
const responseBox = document.getElementById('responseBox');

const zingers = {
  default: [
    "Noted. Now get over it.",
    "Another one for the crypile.",
    "Interesting. We still don't care.",
    "Logged and immediately forgotten.",
    "Wow. Sounds like a you problem.",
    "Try turning it off and touching grass.",
    "AI is not the enemy. Your attitude is.",
    "Complaint received. Reality unchanged.",
    "We're feeding this to a bot that will mock you.",
    "This will be used against you in future simulations."
  ],
  ageGroups: {
    young: [
      "Gen Z? Complain harder. The AI will still out-hustle you.",
      "Your TikTok algorithm is more dangerous than GPT."
    ],
    adult: [
      "You grew up on Google. Now you're afraid of search 2.0?",
      "Still writing think pieces? We’re writing code."
    ],
    boomer: [
      "Boomer panic detected. Consider unplugging your router.",
      "Relax. AI isn’t coming for bingo night."
    ]
  }
};

form.addEventListener('submit', function(e) {
  e.preventDefault();
  const age = parseInt(document.getElementById('age').value, 10);
  let group = 'default';
  if (age < 25) group = 'young';
  else if (age < 60) group = 'adult';
  else group = 'boomer';

  const replies = [...zingers.default, ...(zingers.ageGroups[group] || [])];
  const selected = replies[Math.floor(Math.random() * replies.length)];
  responseBox.textContent = selected;
});
