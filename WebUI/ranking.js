
let search_entries_container = jQuery("#search-entries-container");
let prev_button = jQuery("#prev_page_button");
let next_button = jQuery("#next_page_button");
let page = 1;
let perPage = 10;

function handleSearch()
{
    let query = jQuery("#search-bar").val();
    console.log("searching for " + query);
    jQuery.ajax({
        url: "http://ec2-34-219-99-245.us-west-2.compute.amazonaws.com:9000/search",
        dataType: "json",
        data: {
            "query": query,
            "page": page,
            "perPage": perPage
        },
        success: (data) => processData(data),
        error: function() {
            console.log("error in ajax call to web API")
        }
    })
}

function processData(data)
{
    search_entries_container.clear();
    for(let i = 0; i < data["urls"].length; ++i)
    {
        let row = "\n" +
            "<div class='document-info'>\n" +
            "<p> " + url + " </p>\n" +
            "</div>\n";
        search_entries_container.append(row);
    }
}

function handlePrev()
{
    if(page <= 1)
    {
        return;
    }

    --page;
    handleSearch();
}

function handleNext()
{
    // TODO: see if it is possible to check for max page number

    ++page;
    handleSearch();
}

// prev_button.onclick(handlePrev);
// next_button.onclick(handleNext);
