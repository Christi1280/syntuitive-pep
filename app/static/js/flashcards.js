document.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector("#flashcards");
  if (!container) return;

  const cards = [...container.querySelectorAll(".flashcard-data [data-question]")];
  const text = container.querySelector("#flash-text");
  const label = container.querySelector("#flash-label");
  const hint = container.querySelector("#flash-hint");
  const counter = container.querySelector("#flash-index");
  const cardButton = container.querySelector("#flashcard");
  let index = 0;
  let flipped = false;

  const renderCard = () => {
    const card = cards[index].dataset;
    text.textContent = card[flipped ? "answer" : "question"];
    label.textContent = flipped ? "ANSWER" : "QUESTION";
    hint.textContent = flipped ? "Select to see the question" : "Select to reveal the answer";
    counter.textContent = String(index + 1);
    cardButton.setAttribute("aria-pressed", String(flipped));
  };

  cardButton.addEventListener("click", () => {
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
