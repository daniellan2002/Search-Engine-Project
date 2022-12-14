let search_entries_container = jQuery("#search-entries-container");
let prev_button = jQuery("#prev_page_button");
let next_button = jQuery("#next_page_button");
let page = 1;
let perPage = 10;


function search()
{
    let query = new URLSearchParams(location.search).get("query")
    console.log("searching for " + query)
    jQuery.ajax({
        url: "search",
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
    search_entries_container.empty();
    search_entries_container.append(`<p>${data["resultNum"]} results for: "${data["query"]}"</p>`);
    search_entries_container.append(`<p style="color: gray; font-size: 80%">Took: ${data["queryTime"]} milliseconds</p>`);
    for(let i = 0; i < data["urls"].length; ++i)
    {
        let row = "\n" +
            "<div class='document-info'>\n" +
            `<a target='_blank' href=${data["urls"][i]}> ` + data["urls"][i] + " </a>\n" +
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
    search();
}

function handleNext()
{
    // TODO: see if it is possible to check for max page number

    ++page;
    search();
}

prev_button.click(handlePrev);
next_button.click(handleNext);
search();