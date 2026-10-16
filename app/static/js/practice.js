document.addEventListener("DOMContentLoaded", () => {
  const quiz = document.querySelector("#demo-quiz");
  if (!quiz) return;

  const correctIndex = Number(quiz.dataset.correctIndex);
  const answers = [...quiz.querySelectorAll("[data-answer]")];
  const submitButton = quiz.querySelector("#submit-answer");
  const tryAgainButton = quiz.querySelector("#try-again");
  const result = quiz.querySelector("#quiz-result");
  const progress = quiz.querySelector("#quiz-progress");
  let selectedIndex = null;
  let submitted = false;

  const reset = () => {
    selectedIndex = null;
    submitted = false;
    answers.forEach((answer) => answer.classList.remove("selected", "correct", "wrong"));
    result.classList.add("hidden");
    result.classList.remove("error");
    result.textContent = "";
    progress.style.width = "20%";
    submitButton.classList.remove("hidden");
    submitButton.disabled = true;
    tryAgainButton.classList.add("hidden");
  };

  answers.forEach((answer) => {
    answer.addEventListener("click", () => {
      if (submitted) return;
      selectedIndex = Number(answer.dataset.answer);
      answers.forEach((item) => item.classList.toggle("selected", item === answer));
      submitButton.disabled = false;
    });
  });

  submitButton.addEventListener("click", () => {
    if (selectedIndex === null || submitted) return;
    submitted = true;
    const isCorrect = selectedIndex === correctIndex;
    answers[correctIndex].classList.add("correct");
    if (!isCorrect) answers[selectedIndex].classList.add("wrong");

    const attempts = Number(localStorage.getItem("pep_attempts") || 0) + 1;
    const correct = Number(localStorage.getItem("pep_correct") || 0) + Number(isCorrect);
    localStorage.setItem("pep_attempts", String(attempts));
    localStorage.setItem("pep_correct", String(correct));

    result.classList.remove("hidden");
    result.classList.toggle("error", !isCorrect);
    result.innerHTML = `<b>${isCorrect ? "Correct! 🎉" : "Not quite. The correct answer is B."}</b><p>To add ½ and ¼, rewrite ½ as 2/4. Then 2/4 + 1/4 = 3/4.</p>`;
    progress.style.width = "100%";
    submitButton.classList.add("hidden");
    tryAgainButton.classList.remove("hidden");
  });

  tryAgainButton.addEventListener("click", reset);
});
