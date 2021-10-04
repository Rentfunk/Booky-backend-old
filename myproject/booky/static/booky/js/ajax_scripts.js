// handle order and book filter

const filterForm = document.querySelector("form#filter-form")
const filterFormInputs = document.querySelectorAll("form#filter-form input[id^=id_]")
const filterFormSubmitInput = document.querySelector("form#filter-form input[type=submit]")

const filterItems = document.querySelectorAll("table tr:not(.headers)")

function toggleFilteredItems(filteredList) {
    // filteredList contains ids of orders/books, that should stay    
    Array.from(filterItems).map(( item ) => {
        // those order/books, which ids are not in filteredList are turned invisible
        item.classList.toggle("invis", !filteredList.includes(+item.firstElementChild.textContent))
    })
}

filterForm.addEventListener("submit", ( event ) => {
    event.preventDefault()

    // all inputs inside filterForms
    let filterCleanData = Array.from(event.target.elements)
    let data = {} 

    // this data structure is needed for creating QueryDict in python
    for (let i of filterCleanData) {
        data[i.name] = i.value
    }

    // django ajax requests needs X_CSRFToken header
    let CSRFToken = filterForm.firstElementChild.value 

    let url = window.location.pathname == "/booky/orders/" ? "orderFilter" : "bookFilter"

    fetch("ajax/" + url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": CSRFToken,
        },
        body: JSON.stringify(data),

    })
    .then(res => res.json())
    .then(data => toggleFilteredItems(data))
    

})
    
Array.from(filterFormInputs).forEach(( input ) => {

    //submits form, for every character you write in inputs
    input.addEventListener("input", () => {

        //form.submit() doesn't start onsubmit event, so that's why button.click() is used
        filterFormSubmitInput.click()
    })
})



