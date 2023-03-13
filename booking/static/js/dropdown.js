document.addEventListener("click", (e) => {
    const isDropdownButton = e.target.matches("[data-dropdown-button]");
  
    console.log(isDropdownButton, "out of if");
    console.log(e.target.closest("[data-dropdown]"));
    if (!isDropdownButton && e.target.closest("[data-dropdown]") != null) {
      return;
    }
  
    let currentDropdown;
    if (isDropdownButton) {
      currentDropdown = e.target.closest("[data-dropdown]");
      console.log(currentDropdown);
      console.log("inside 2 if");
      currentDropdown.classList.toggle("active");
    }
    document.querySelectorAll("[data-dropdown]").forEach((dropdown) => {
      if (dropdown == currentDropdown) {
        console.log("inside 3rd if");
        return;
      }
      dropdown.classList.remove("active");
      console.log("out of if statement");
    });
  });
  
  function filterCheck() {
    const genre = [];
    let submitOk = false;
    const language = [];
    const rating = [];
  
    const filterChecked = document
      .querySelectorAll(".filterCheckbox")
      .forEach((box) => {
        if (box.checked == true) {
          if (box.name == "Genre") {
            genre.push(box.value);
            console.log(genre, "this is the genre");
          } else if (box.name == "Language") {
            language.push(box.value);
            console.log(language, "this is language");
          } else if (box.name == "Ratings") {
            rating.push(box.value);
            console.log(rating, "this is rating");
          }
        }
      });
  
    const myFilter = [];
    myFilter.push(genre);
    myFilter.push(language);
    myFilter.push(rating);
    console.log(myFilter);
    let array = [1];
    let loop = 0;
    for (let i = 0; i < myFilter.length; i++) {
      if (myFilter[i].length == 0) {
        loop++;
      }
    }
    console.log("intermediate");
  
    if (loop == 3) {
      alert("select atleast One filter");
      return submitOk;
    } else {
      jsonFilter = JSON.stringify(myFilter);
      sendJson = document.getElementById("submitButton");
      sendJson.value = jsonFilter;
      console.log(sendJson, "inside else bolck");
      submitOk = true;
      return submitOk;
    }
  }
  
  function boxChecked() {
    document.querySelectorAll(".filterCheckbox").forEach((box) => {
      if (box.name == "Genre") {
        let memoryFilter = returnJson[0].includes(box.value);
        if (memoryFilter == true) {
          box.checked = true;
        }
      }
      if (box.name == "Language") {
        let memoryFilter = returnJson[1].includes(box.value);
        if (memoryFilter == true) {
          box.checked = true;
        }
      }
      if (box.name == "Ratings") {
        let memoryFilter = returnJson[2].includes(box.value);
        if (memoryFilter == true) {
          box.checked = true;
        }
      }
    });
  }
  const memoryData = document.getElementById("jsonId").value;
  console.log(memoryData);
  const returnJson = JSON.parse(memoryData);
  console.log(returnJson);
  boxChecked();
  