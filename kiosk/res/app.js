/*
Function to toggle 
*/
function toggleTheme() {
    // Get the toggle element
    toggleButton = document.getElementById("themeToggleButton");
    // Get class list
    bodyClasses = document.body.classList;
    // Check if light theme is enabled
    if (bodyClasses.contains('light')) {
        bodyClasses.remove('light');
        toggleButton.textContent = 'Light Theme';
        // Add theme cookie for persistence
        document.cookie = "theme=dark;";
    } else {
        bodyClasses.add('light');
        toggleButton.textContent = 'Dark Theme';
        // Add theme cookie for persistence
        document.cookie = "theme=light;";
    }
}

function cart_page() {
    var items = Array.from(document.getElementsByClassName("order-item"));

    items.forEach(element => {
        element.addEventListener("mouseup", (e, id = element.id) => {location.href = "/cart/" + id;});
    });
}

function disableImgDrag() {
    var imgs = Array.from(document.querySelectorAll('img:not(.img-exempt)'));

    imgs.forEach(element => {
        element.addEventListener("dragstart", (e) => {e.preventDefault();});
    });
}

function expandCheckboxes() {
    var checkboxes = Array.from(document.querySelectorAll('checkbox'));

    checkboxes.forEach(element => {
        console.log("Attemping to expand checkbox " + element.name);
        // Create the wrapping label, set value to current element value
        label = document.createElement("label");
        label.textContent = element.textContent;
        label.classList = ["check-label"];
        // Create the checkbox (Used for redundancy)
        check = document.createElement("input");
        check.type = "checkbox";
        // Replace values
        check.checked = element.checked;
        tmp = element.id;
        tmp2 = element.name;
        delete element.id, element.name;
        check.id = tmp;
        check.name = tmp2;
        delete tmp, tmp2;
        label.appendChild(check);
        // Create the span which will represent the actual checkbox
        span = document.createElement("span");
        span.classList = ["checkmark"];
        label.appendChild(span);
        // Replace the element with the expansion
        element.parentNode.replaceChild(label, element);
        console.log("Attempted to expand checkbox " + check.name);
    });
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById("themeToggleButton").addEventListener("mouseup", toggleTheme);
    if (document.cookie.match(/.*theme\s*=\s*light;?.*/)) {
        toggleTheme();
    }

    disableImgDrag();
    expandCheckboxes();

    if (location.pathname == "/cart") {
        cart_page();
    }
});