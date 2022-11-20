let search_form = jQuery("#search-form");

function handleSearch(searchEvent)
{
    console.log("handling search");
    searchEvent.preventDefault();
    let queryUrl = "ranking.html?" + search_form.serialize();
    window.location.assign(queryUrl);
}

search_form.submit(handleSearch);
