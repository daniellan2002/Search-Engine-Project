// TODO: test if this actually works

let search_form = jQuery("#search-form");
let search_entries_container = jQuery("#search-entries-container");
let prev_button = jQuery("#prev_page_button");
let next_button = jQuery("#next_page_button");
let allRows;
let page_number = 0;
const MAX_ENTRIES_PER_PAGE = 10;

function handleSearch(searchEvent)
{
    let query = jQuery("#search-bar").val();
    console.log("searching for " + query);
    // TODO direct ajax call to appropriate url
    jQuery.ajax({
        // url: python url
        dataType: "text",
        success: (data) => processData(data),
        error: console.log("error during ajax call to csv")
    })
}

function processData(data) {
    allRows = data.split(/\r?\n|\r/);
    page_number = 0;
    populateData();
}

function populateData()
{
    search_entries_container.clear();
    for(let i = page_number * MAX_ENTRIES_PER_PAGE; i < (page_number + 1) * MAX_ENTRIES_PER_PAGE; ++i)
    {
        // TODO: change row variables to reflect csv format
        let url = allRows[i];
        let title = allRows[i];
        let row = "\n" +
            "<div class='document-info'>\n" +
            "<p> " + url + " </p>\n" +
            "<a class='document-title' href='" + url + "'>" + title + "</a>\n" +
            "</div>\n";
        search_entries_container.append(row);
    }

}

function handlePrev()
{
    if(page_number <= 0)
    {
        return;
    }

    --page_number;
    populateData();
}

function handleNext()
{
    // TODO: see if it is possible to check for max page number

    ++page_number;
    populateData();
}

prev_button.onclick(handlePrev);
next_button.onclick(handleNext);
search_form.submit(handleSearch);