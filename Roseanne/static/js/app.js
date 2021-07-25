// from data.js
const tableData = data;

d3.json("static/json/data.json", function(data) {
  console.log(data);
});

// get table references
var tbody = d3.select("tbody");

function buildTable(data) {
  // First, clear out any existing data
  tbody.html("");

  if (Object.keys(data).length === 0) {
    tbody.html("Try one filter.  Then refine search.  Case matters.");
    return;
  }

  // Next, loop through each object in the data
  // and append a row and cells for each value in the row
  data.forEach((dataRow) => {
    // Append a row to the table body
    let row = tbody.append("tr");

    // Loop through each field in the dataRow and add
    // each value as a table cell (td)
    Object.values(dataRow).forEach((val) => {
      let cell = row.append("td");
      cell.text(val);
    });
  });
}

// 1. Create an empty 'filters' variable to keep track of all the filters as an object.
// Use 'filters' variable in step 5 to store the property id.
var filters = {};

// 3. Use this function to update the filters. 
function updateFilters() {

    // 4a. Save the element that was changed as a variable.
    // Initializes an array to store the value and id
    let changedElement = d3.select(this);

    // 4b. Save the value that was changed as a variable.
    let elementValue = changedElement.property("value");
    console.log(elementValue);

    // 4c. Save the id of the filter that was changed as a variable.
    // id of the id attribute that has changed
    let filterId = changedElement.attr("id");
    console.log(filterId);
  
    // 5. If a filter value was entered then add that filterId and value
    // to the filters list. Otherwise, clear that filter from the filters object.
    if (elementValue) {
      filters[filterId] = elementValue;
    }
    else {
      delete filters[filterID];
    }
    console.log(filters);
    // 6. Call function to apply all filters and rebuild the table
    filterTable();

  }
  
  // 7. Use this function to filter the table when data is entered.
  function filterTable() {
  
    // 8. Set the filtered data to the tableData.
    let filteredData = tableData;
  
    // 9. Loop through all of the filters and keep any data that matches the filter values
    // Object.entries() returns array of a given object's own enumerable string-keyed
    // property [key, value] pairs

    Object.entries(filters).forEach(function([kee, val]) {
      // if the value is not empty then filteredData = data set that matches filters
      if (val != "") {
        // Test to see if key (kee): value(val) pairs show up
        console.log([kee, val]);
        // test to see if tableData comes up before the filter
        console.log(filteredData);
        filteredData = filteredData.filter(row => row[kee] === val);
      }
    });

    // 10. Finally, rebuild the table using the filtered data
    buildTable(filteredData); 
    // Check to see if anything is in filteredData after filters entered.
    console.log(filteredData); 
  };
  
  // 2. Attach an event to listen for changes to each filter
  d3.selectAll("input").on("change", updateFilters);
  
  // Build the table when the page loads
  buildTable(tableData);
