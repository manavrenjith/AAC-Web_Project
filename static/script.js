function speak(text) {

    let speech = new SpeechSynthesisUtterance(text);

    speech.lang = "ml-IN";  // Malayalam language

    speech.rate = 1;
    speech.pitch = 1;

    speechSynthesis.speak(speech);

}