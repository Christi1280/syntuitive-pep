document.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector("#flashcards");
  if (!container) return;

  const cards = [
    ["What is a numerator?", "The top number in a fraction."],
    ["What is evaporation?", "The process in which liquid changes into gas."],
    ["What is a synonym?", "A word with the same or nearly the same meaning as another."],
  ];
  let index = 0;
  let flipped = false;
  const text = container.querySelector("#flash-text");
  const hint = container.querySelector("#flash-hint");
  const counter = container.querySelector("#flash-index");

  const renderCard = () => {
    text.textContent = cards[index][flipped ? 1 : 0];
    counter.textContent = String(index + 1);
    hint.textContent = `Tap card to ${flipped ? "see the question" : "reveal the answer"}`;
  };

  container.querySelector("#flashcard").addEventListener("click", () => {
    flipped = !flipped;
    renderCard();
  });
  container.querySelector("#flash-previous").addEventListener("click", () => {
    index = (index + cards.length - 1) % cards.length;
    flipped = false;
    renderCard();
  });
  container.querySelector("#flash-next").addEventListener("click", () => {
    index = (index + 1) % cards.length;
    flipped = false;
    renderCard();
  });
});
