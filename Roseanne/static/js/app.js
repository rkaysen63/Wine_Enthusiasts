// from data.json
var tableData = {}; 

d3.json("static/json/data.json", function(data) {
  tableData = data;
  buildTable(tableData);
  console.log(tableData);
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

// Create an empty 'filters' variable to keep track of all the filters as an object.
// Use 'filters' variable in step 5 to store the property id.
var filters = {};

// Use this function to update the filters. 
function updateFilters() {

    // Save the element that was changed as a variable.
    // Initializes an array to store the value and id
    let changedElement = d3.select(this);

    // Save the value that was changed as a variable.
    let elementValue = changedElement.property("value");
    console.log(elementValue);

    // Save the id of the filter that was changed as a variable.
    // id of the id attribute that has changed
    let filterId = changedElement.attr("id");
    console.log(filterId);
  
    // If a filter value was entered then add that filterId and value
    // to the filters list. Otherwise, clear that filter from the filters object.
    if (elementValue) {
      filters[filterId] = elementValue;
    }
    else {
      delete filters[filterID];
    }
    console.log(filters);
    // Call function to apply all filters and rebuild the table
    filterTable();

  }
  
  // Use this function to filter the table when data is entered.
  function filterTable() {
  
    // Set the filtered data to the tableData.
    let filteredData = tableData;
  
    // Loop through all of the filters and keep any data that matches the filter values
    // Object.entries() returns array of a given object's own enumerable string-keyed
    // property [key, value] pairs

    Object.entries(filters).forEach(function([kee, val]) {
      // if the value is not empty then filteredData = data set that matches filters
      if (val != "") {
        // points filter will return points or anything above
        if (kee === "points"){
          console.log("POINTS FILTER");
          const valNum2 = Number(val);
          filteredData = filteredData.filter(row => (Number(row[kee]) >= valNum2));
        }
        // price filter will return price and/or -$5
        else if (kee === "price"){
          console.log("PRICE FILTER");
          const valNum = Number(val);
          filteredData = filteredData.filter(row => ((Number(row[kee]) >= valNum - 5) && (Number(row[kee]) <= valNum + 5)));
        }        
        else {
          // Test to see if key (kee): value(val) pairs show up
          console.log([kee, val]);
          // test to see if tableData comes up before the filter
          console.log(filteredData);
          filteredData = filteredData.filter(row => String(row[kee]) === String(val));
        }
      }
    });

    // Finally, rebuild the table using the filtered data
    buildTable(filteredData); 
    // Check to see if anything is in filteredData after filters entered.
    console.log(filteredData); 
  };
  
  // Attach an event to listen for changes to each filter
  d3.selectAll("input").on("change", updateFilters);
  
  // Build the table when the page loads
  buildTable(tableData);
