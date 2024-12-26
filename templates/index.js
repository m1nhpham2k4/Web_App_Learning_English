

function getdata(randome) {
    fetch(`http://127.0.0.1:5000/generate-vocab/${randome}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    }).then(data => {
        slideIndex = 1
        console.log('----------')
        console.log(data.length)
        displayshow(data)
        // do something with the data
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });

}

getdata(randome = 0)
let slideIndex = 1;
function displayshow(data_vocab){
    let slideshowContainer = document.getElementsByClassName("slideshow-container")[0];
    let dotsContainer = document.getElementsByClassName("slide")[0];
    // Loại bỏ tất cả các phần tử con trong thẻ slideshowContainer
    slideshowContainer.innerHTML = "";

    // Loại bỏ tất cả các phần tử con trong thẻ dotsContainer
    dotsContainer.innerHTML = "";

    for (let i = 0; i < data_vocab.length; i++) {
    
        // Create a new slide
        let slide = document.createElement("div");
        slide.className = "mySlides_fade";
        slide.style.display = "none";

        // Create the number text
        let numberText = document.createElement("div");
        numberText.className = "numbertext";
        numberText.textContent = `${i + 1} / ${data_vocab.length}`;
        slide.appendChild(numberText);

        // Create the image
        let vocab = document.createElement("div");
        vocab.className = "vocab";
        // vocab.textContent =  data_vocab[i].vocab
        let text_vocab = document.createElement("p");
        text_vocab.textContent = data_vocab[i].vocab
        vocab.appendChild(text_vocab);

        slide.appendChild(vocab);

        let phonetic_vocab = document.createElement("div");
        phonetic_vocab.className = "phonetic";
        phonetic_vocab.textContent = data_vocab[i].phonetic_vocab
        slide.appendChild(phonetic_vocab);

        let example = document.createElement("div");
        example.className = "example";
        example.textContent = data_vocab[i].example
        slide.appendChild(example);

        let mean = document.createElement("div");
        mean.className = "mean";
        mean.textContent = data_vocab[i].mean
        slide.appendChild(mean);

        // Create the <audio> elements
        const soundVocab = document.createElement('audio');
        const soundExample = document.createElement('audio');
        // Set the class attribute for styling
        soundVocab.setAttribute('class', 'sound-icon-vocab');
        // soundVocab.setAttribute('id', "sound-icon-vocab");
        soundExample.setAttribute('class', 'sound-icon-example');

        // Set the controls attribute to allow user interaction
        soundVocab.setAttribute('controls', '');

        soundExample.setAttribute('controls', '');

        // Create the <source> elements and set their attributes
        const sourceVocab = document.createElement('source');
        sourceVocab.setAttribute('src', data_vocab[i].audio_vocab);
        sourceVocab.setAttribute('type', 'audio/mp3');

        const sourceExample = document.createElement('source');
        sourceExample.setAttribute('src', data_vocab[i].audio_example);
        sourceExample.setAttribute('type', 'audio/mp3');

        // Append the <source> elements to the <audio> elements
        soundVocab.appendChild(sourceVocab);
        soundExample.appendChild(sourceExample);

        slide.appendChild(soundVocab)
        slide.appendChild(soundExample)
        let image = document.createElement("img");
        image.src = "./image/vocab.jpg";
        image.style.width = "100%";
        slide.appendChild(image);



        // Add the slide to the slideshow container
        slideshowContainer.appendChild(slide);
        // Create a new dot
        let dot = document.createElement("span");
        dot.className = "dot";
        dot.onclick = function () { currentSlide(i + 1); };
        dotsContainer.appendChild(dot);
    }
    
    // Set the initial slide
    slideshowContainer.children[0].style.display = "block";
    dotsContainer.children[0].className += " active";
    showSlides(slideIndex);

}

// Initialize the slide index and the slide show function

function plusSlides(n) {
    showSlides(slideIndex += n);
}
function speak() {
    // Create a SpeechSynthesisUtterance
    const utterance = new SpeechSynthesisUtterance("Welcome to this tutorial!");
  
    // Select a voice
    const voices = speechSynthesis.getVoices();
    utterance.voice = voices[0]; // Choose a specific voice
  
    // Speak the text
    speechSynthesis.speak(utterance);
  }
function currentSlide(n) {
    
    showSlides(slideIndex = n);
}

function showSlides(n) {
    let i;
    let slides = document.getElementsByClassName("mySlides_fade");
    console.log(slides.length)
    let dots = document.getElementsByClassName("dot");
    if (n > slides.length) { slideIndex = 1 }
    if (n < 1) { slideIndex = slides.length }
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex - 1].style.display = "block";
    dots[slideIndex - 1].className += " active";
    
}


function handleFileUpload(event) {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('csv_file', file);

    fetch('http://127.0.0.1:5000/load_data/', {
        method: 'POST',
        body: formData
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Server response:', data);
            // Handle the server response as needed
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}
const form = document.getElementById("myForm");

form.addEventListener("submit", (event) => {
  event.preventDefault();

  const formData = new FormData(form);
  const vocab = formData.get("vocab");
  const mean = formData.get("mean");
  const example = formData.get("example");

  fetch("http://127.0.0.1:5000/add_data/", {
    method: "POST",
    body: JSON.stringify({ vocab, mean, example }),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      
      return response.json();
    })
    .then((data) => {
      console.log("Server response:", data);
      // Handle the server response as needed
      alert(response['Status']);
    })
    .catch((error) => {
      console.error("There was a problem with the fetch operation:", error);
    });
});

const randome_buttons = document.getElementsByClassName("randome_button");
const randome_buttons1 = document.getElementsByClassName("randome_button_1");
const randome_buttons2 = document.getElementsByClassName("randome_button_2");

// Lặp qua từng nút và gắn sự kiện cho mỗi nút
Array.from(randome_buttons).forEach(button => {
    button.addEventListener('click', () => {
        // Gọi hàm getdata() khi nút được nhấn
        getdata(1);
    });
});

// Lặp qua từng nút và gắn sự kiện cho mỗi nút
Array.from(randome_buttons1).forEach(button => {
    button.addEventListener('click', () => {
        // Gọi hàm getdata() khi nút được nhấn
        getdata(2);
    });
});

// Lặp qua từng nút và gắn sự kiện cho mỗi nút
Array.from(randome_buttons2).forEach(button => {
    button.addEventListener('click', () => {

        // Gọi hàm getdata() khi nút được nhấn
        getdata(3);
    });
});
const startButton = document.getElementById('startButton');
const outputDiv = document.getElementById('output');

const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition || window.mozSpeechRecognition || window.msSpeechRecognition)();
recognition.lang = 'en-US';

recognition.onstart = () => {
    startButton.textContent = 'Listening...';
};

recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    outputDiv.textContent = transcript;
};

recognition.onend = () => {
    startButton.textContent = 'Start Voice Input';
};

startButton.addEventListener('click', () => {
    recognition.start();
});