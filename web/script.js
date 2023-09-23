document.getElementById("predictButton").addEventListener("click", function() {
    const data = {
        Pclass: parseInt(document.getElementById("Pclass").value, 10),
        Sex: document.getElementById("Sex").value,
        Age: parseFloat(document.getElementById("Age").value),
        SibSp: parseInt(document.getElementById("SibSp").value, 10),
        Parch: parseInt(document.getElementById("Parch").value, 10),
        Fare: parseFloat(document.getElementById("Fare").value),
        Embarked: document.getElementById("Embarked").value
    };

    fetch("http://127.0.0.1:8000/Titanic/", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("result").textContent = data.Survived ? "Survived" : "Did not survive";
    })
    .catch(error => {
        console.error("There was an error!", error);
    });
});
