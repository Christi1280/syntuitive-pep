document.addEventListener("DOMContentLoaded", () => {
  const test = document.querySelector("#practice-test");
  if (!test) return;

  const questions = [...test.querySelectorAll(".test-question")];
  const optionsByQuestion = questions.map((question) =>
    [...question.querySelectorAll(".answer")]
  );
  const numberButtons = [...test.querySelectorAll(".question-number")];
  const previous = test.querySelector("#previous-question");
  const next = test.querySelector("#next-question");
  const currentQuestion = test.querySelector("#current-question");
  const submit = test.querySelector("#submit-test");
  const retry = test.querySelector("#retry-test");
  const result = test.querySelector("#test-result");
  let currentIndex = 0;
  let submitted = false;

  const selectedAnswers = () => questions.map((question) =>
    question.querySelector(".answer.selected")
  );

  const renderQuestion = () => {
    const selections = selectedAnswers();
    questions.forEach((question, index) => {
      question.hidden = index !== currentIndex;
    });
    numberButtons.forEach((button, index) => {
      button.classList.toggle("current", index === currentIndex);
      button.classList.toggle("answered", Boolean(selections[index]));
      button.setAttribute("aria-current", index === currentIndex ? "step" : "false");
    });
    currentQuestion.textContent = `Question ${currentIndex + 1} of ${questions.length}`;
    previous.disabled = currentIndex === 0;
    next.disabled = currentIndex === questions.length - 1;
  };

  const updateSubmitState = () => {
    submit.disabled = submitted || selectedAnswers().some((selection) => !selection);
  };

  optionsByQuestion.forEach((answers, questionIndex) => {
    answers.forEach((answer) => {
      answer.addEventListener("click", () => {
        if (submitted) return;
        answers.forEach((option) => {
          const selected = option === answer;
          option.classList.toggle("selected", selected);
          option.setAttribute("aria-pressed", String(selected));
        });
        numberButtons[questionIndex].classList.add("answered");
        updateSubmitState();
      });
    });
  });

  previous.addEventListener("click", () => {
    if (currentIndex > 0) {
      currentIndex -= 1;
      renderQuestion();
    }
  });

  next.addEventListener("click", () => {
    if (currentIndex < questions.length - 1) {
      currentIndex += 1;
      renderQuestion();
    }
  });

  numberButtons.forEach((button) => {
    button.addEventListener("click", () => {
      currentIndex = Number(button.dataset.questionIndex);
      renderQuestion();
    });
  });

  submit.addEventListener("click", () => {
    const selections = selectedAnswers();
    if (submitted || selections.some((selection) => !selection)) return;
    submitted = true;
    let score = 0;

    questions.forEach((question, index) => {
      const selected = selections[index];
      const correctAnswer = question.dataset.correctAnswer;
      const isCorrect = selected.dataset.answer === correctAnswer;
      if (isCorrect) score += 1;

      const answers = optionsByQuestion[index];
      const correctOption = answers.find((answer) => answer.dataset.answer === correctAnswer);
      correctOption.classList.add("correct");
      if (!isCorrect) selected.classList.add("wrong");
      answers.forEach((answer) => {
        answer.disabled = true;
        answer.setAttribute("aria-disabled", "true");
      });

      const feedback = question.querySelector(".question-feedback");
      const correctText = correctOption.querySelector("span:last-child").textContent;
      const letter = correctOption.querySelector(".answer-letter");
      const answerText = letter ? `${letter.textContent}. ${correctText}` : correctText;
      const outcome = isCorrect ? "Correct." : `Correct answer: ${answerText}.`;
      feedback.textContent = `${outcome} ${question.dataset.explanation}`.trim();
      feedback.hidden = false;
      feedback.classList.toggle("incorrect", !isCorrect);
    });

    result.textContent = `Your score: ${score} out of ${questions.length}.`;
    result.hidden = false;
    submit.hidden = true;
    retry.hidden = false;
  });

  retry.addEventListener("click", () => {
    submitted = false;
    currentIndex = 0;
    questions.forEach((question, index) => {
      optionsByQuestion[index].forEach((answer) => {
        answer.disabled = false;
        answer.removeAttribute("aria-disabled");
        answer.setAttribute("aria-pressed", "false");
        answer.classList.remove("selected", "correct", "wrong");
      });
      const feedback = question.querySelector(".question-feedback");
      feedback.hidden = true;
      feedback.classList.remove("incorrect");
      feedback.textContent = "";
    });
    result.hidden = true;
    result.textContent = "";
    submit.hidden = false;
    retry.hidden = true;
    renderQuestion();
    updateSubmitState();
  });

  renderQuestion();
  updateSubmitState();
});
