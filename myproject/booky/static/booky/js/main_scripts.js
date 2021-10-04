// hide not important form inputs

const notImportantInputs = document.querySelectorAll("input[id$='-id']")

if ( notImportantInputs ) {
    Array.prototype.map.call(notImportantInputs, (item) => { item.parentElement.style.display = "none"})
}


// handle footer

function handleFooter() {
    let footer = document.querySelector("footer")

    // if there's enough space for footer, fix it to bottom, else put it at the end of page
    footer.classList.toggle("vis", footer.getBoundingClientRect().bottom < window.innerHeight)
}

handleFooter()
window.addEventListener("resize", handleFooter)


// handle order filter

const orderFilter = document.querySelector("#filter-show")
const orderFilterForm = document.querySelector("#filter-form")

if ( orderFilter ) {
    orderFilter.addEventListener("click", () => {
        orderFilterForm.classList.toggle("invis")
    })
}


// handle teachers table coloring pattern

const teacherContentRows = document.querySelectorAll("tr.teachers-content")


if ( teacherContentRows ) {
    Array.prototype.forEach.call(teacherContentRows, (row) => {
        row.classList.add(row.previousElementSibling.classList[1] == "darker" ? "darker" : "lighter")
    })
}

// handle teachers table borders of spanned rows


const teacherSpecialContentRows = document.querySelectorAll("tr.content-special")
const teacherRows = document.querySelectorAll("table#teachers-table tr:not(.headers)")



if ( teacherSpecialContentRows ) {

    //rows whith teacher, who has 2 or more books
    let spannedTeacherRows = Array.prototype.filter.call(teacherSpecialContentRows, (item) => item.firstElementChild.rowSpan > 2)
    
    Array.prototype.forEach.call(spannedTeacherRows, (teacher) => {
        
        // position on which teacher is in all rows
        let rowIndex = Array.prototype.indexOf.call(teacherRows, teacher)
        
        let rowSpan = teacher.firstElementChild.rowSpan

        // rows on which teachers books data are -----> all rows are sliced ------> new array is: [his first book : his last book]
        let assocRows = Array.prototype.slice.call(teacherRows, rowIndex + 1, rowIndex + rowSpan )
        
        // if teacher has 2 books -> on first row delete bottom border on second delete top border
        // if teacher has more than 2 books -> on first row delete bottom border, on last delete top border, on all between delete both top and bottom border
        assocRows.map((item, i) => {

            // deletion is achieved through css classes
            item.classList.toggle("wo-bottom", i == 0)
            item.classList.toggle("wo-top", i == rowSpan - 2)
            item.classList.toggle("wo-both", i > 0 && i < rowSpan - 2)
        })
    })
}


// handle radio buttons style

const radioBtnsLabels = document.querySelectorAll("label[for^=id_typeOfOrder_]")


if ( radioBtnsLabels ) {

    Array.prototype.forEach.call(radioBtnsLabels, (btn) => {
        
        btn.addEventListener("click", () => {
            
            Array.prototype.map.call(radioBtnsLabels, ( label ) => {
                        
                // if label's input is checked, add class .checked, which changes :before element of label
                label.classList.toggle("checked", label.firstElementChild.checked )
            
            })
        })
    })
}


// replace all <select> inputs with normal text inputs with dropdown options, that changes based on what is written in text input

const selectInputs = document.querySelectorAll("select")

function insertAfter(newNode, referenceNode) {
    referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling)
}

Array.from(selectInputs).forEach(( input ) => {
    
    // gets rid of default ------------- option
    let selectInputOptions = Array.from(input.options).slice(1, -1)

    // creates array of objects with id and text of each book option
    let selectInputOptionsValues = selectInputOptions.map(( option ) => {
        return {
            id: option.value,
            text: option.textContent
        }
    })
    
    // select input label ---> needed for inserting new input element
    let selectInputLabel = input.previousElementSibling

    input.remove()


    // creating elements for autocomplete dropdown input
    let selectDiv = document.createElement("DIV")
    selectDiv.classList.add("select-div")

    let newInput = document.createElement("INPUT")
    newInput.classList.add("input-style")
    newInput.classList.add("select-input")
    newInput.name = "book"
    
    let autocompleteDiv = document.createElement("DIV")
    autocompleteDiv.classList.add("select-ac-div")

    let autocompleteUl = document.createElement("UL")
    autocompleteUl.classList.add("list-style-none")

    selectInputOptionsValues.forEach(( values ) => {
        let newLi = document.createElement("LI")
        newLi.classList.add("ac-item")
        newLi.id = values.id
        newLi.textContent = values.text
        
        autocompleteUl.appendChild(newLi)
    })

    autocompleteDiv.appendChild(autocompleteUl)

    selectDiv.appendChild(newInput)
    selectDiv.appendChild(autocompleteDiv)

    insertAfter(selectDiv, selectInputLabel)

    let autocompleteItems = autocompleteUl.children

    function filterAutocompleteItems() {
        Array.from(autocompleteItems).forEach(( item ) => {

            // for every character written in new input this function compares whats written with every LI element and filters out those, that don't match
            item.classList.toggle("invis", !item.textContent.toLowerCase().includes(newInput.value.toLowerCase()))
        })
    }

    newInput.addEventListener("input", () => {
        filterAutocompleteItems()
    })


    Array.from(autocompleteItems).forEach(( item ) => {
        item.addEventListener("click", ( event ) => {

            // when LI element is clicked, it's text content is put inside input element
            newInput.value = event.target.textContent
            newInput.setAttribute("data-book-id", event.target.id)
            filterAutocompleteItems()
            newInput.blur() 
        })
    })
    
    newInput.form.addEventListener("submit", () => {
        // puts book id as value to the newInput, so that form can be send and evaluated correctly
        newInput.value = newInput.getAttribute("data-book-id")
    })
})
