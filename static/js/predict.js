fileInput = document.getElementById("files");
image = document.getElementById("image");
result = document.getElementById("result");
form = document.getElementById("form");
submitBtn = document.getElementById("submitBtn");
spinner = document.querySelector('.spinner');
solutionContainer = document.querySelector('.solutions');
causesContainer = document.querySelector('.causes');

spinner.style.display = 'none';
submitBtn.style.display = 'none';

fileInput.onchange = () => {
    result.innerHTML = '';
    solutionContainer.textContent = '';
    causesContainer.textContent = '';
    renderImage();
}

form.onsubmit = (e) => {
    e.preventDefault();
    submitBtn.style.display = 'none';
    apiCall();
}

function renderImage() {
    render = new FileReader();
    console.log(fileInput.files[0]);

    render.readAsDataURL(fileInput.files[0]);

    render.onload = function() {
        image.setAttribute('src', render.result);
    }

    submitBtn.style.display = 'block';
}

function apiCall() {
    formData = new FormData(form);

    spinner.style.display = 'block';

    fetch('/disease-api/disease-prediction', {
        method: 'POST',
        body: formData
    })
    .then((res) => res.json())
    .then((data) => {
        spinner.style.display = 'none';
        console.log(data);
        showResult(data);
        showSolutions(data);
        showCauses(data);
    })
    .catch((e) => console.log(e));
}

function showResult(data) {
    
    result.innerHTML = `<p>Disease : ${data.class}</p>
                        <p>Score : ${data.score}</p>`;
}

function showSolutions(data) {
    let solutions = data.solutions;
    h3 = document.createElement('h3');
    h3.innerHTML = 'solutions';

    solutionContainer.appendChild(h3);

    ul = document.createElement("ul");

    for(let i = 0; i < solutions.length; i++) {
        li = document.createElement("li");
        li.innerHTML = solutions[i];
        
        ul.appendChild(li);
    }

    solutionContainer.appendChild(ul);
}

function showCauses(data) {
    let solutions = data.causes;
    h3 = document.createElement('h3');
    h3.innerHTML = 'Causes';

    causesContainer.appendChild(h3);

    ul = document.createElement("ul");

    for(let i = 0; i < solutions.length; i++) {
        li = document.createElement("li");
        li.innerHTML = solutions[i];
        
        ul.appendChild(li);
    }

    causesContainer.appendChild(ul);
}
