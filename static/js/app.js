function calculator(customerID) {

am4core.ready(function() {

  // Themes begin
  am4core.useTheme(am4themes_animated);
  // Themes end
  
  var chart = am4core.create("chartdiv", am4charts.XYChart);
  
  d3.json(`/_get_data/${customerID}`).then((output) => {

    var data = [];
    var churn_rate = parseFloat(d3.select("#churn h3").text());
    
    Object.entries(output).forEach(([key,value]) => {
      data.push({ category: key, open: churn_rate, close: parseFloat(value)});
      console.log(data)
    });

  
  chart.data = data;
  var categoryAxis = chart.yAxes.push(new am4charts.CategoryAxis());
  categoryAxis.renderer.grid.template.location = 0;
  categoryAxis.dataFields.category = "category";


  categoryAxis.renderer.minGridDistance = 15;
  categoryAxis.renderer.grid.template.location = 0.5;
  categoryAxis.renderer.grid.template.strokeDasharray = "1,3";
  categoryAxis.renderer.labels.template.rotation = 0;
  categoryAxis.renderer.labels.template.horizontalCenter = "left";
  categoryAxis.renderer.labels.template.location = 0.5;
  categoryAxis.renderer.inside = false;
  
  categoryAxis.renderer.labels.template.adapter.add("dy", function(dy, target) {
      return -target.maxRight / 2;
  })
  
  var valueAxis = chart.xAxes.push(new am4charts.ValueAxis());
  valueAxis.title.fontWeight = "bold";
  valueAxis.tooltip.disabled = true;
  valueAxis.renderer.ticks.template.disabled = true;
  valueAxis.renderer.axisFills.template.disabled = true;
  
  var series = chart.series.push(new am4charts.ColumnSeries());
  series.dataFields.categoryY = "category";
  series.dataFields.openValueX = "open";
  series.dataFields.valueX = "close";
  series.tooltipText = "Before: {openValueX.value} After: {valueX.value}";
  series.sequencedInterpolation = true;
  series.fillOpacity = 0;
  series.strokeOpacity = 0;
  series.columns.template.height = 0.01;
  series.tooltip.pointerOrientation = "horizontal";
  
  var openBullet = series.bullets.create(am4charts.CircleBullet);
  openBullet.locationX = 1;
  
  var closeBullet = series.bullets.create(am4charts.CircleBullet);
  
  closeBullet.fill = chart.colors.getIndex(4);
  closeBullet.stroke = closeBullet.fill;
  
  chart.cursor = new am4charts.XYCursor();
  
  // chart.scrollbarX = new am4core.Scrollbar();
  // chart.scrollbarY = new am4core.Scrollbar();
  
});

  }); // end am4core.ready()
}


function buildMetadata(customerID) {

  // Retrieve metadata of a customer ID
  d3.json(`/metadata/${customerID}`).then((data) => {
    console.log("data from /metadata/:id", data)
  
  // Use `d3.json` to fetch the metadata for a customer ID
    // Use d3 to select the panel with id of `#customer-metadata`
    var panel = d3.select("#customer-metadata");
   
    
    // Use `.html("") to clear any existing metadata
    panel.html("");
   
    // Use `Object.entries` to add each key and value pair to the panel
    Object.entries(data).forEach(([key, value]) => {
      panel.append("h6").text(`${key} : ${value}`);
    });
}); 
}
     
// function calculator(customerID) {
//   d3.json(`/_get_data/${customerID}`).then((output) => {

//     // Use d3.json to fetch get_data 
//     var tbody = d3.select("tbody");
//     var thead = d3.select("thead");

//     tbody.html("");
//     thead.html("");

//     var header = tbody.append("tr");    
//     Object.entries(output).forEach(([key,value]) => {
//       var column = header.append("th");
//       column.text(key);
//     });
    
//     var row = tbody.append("tr");

//     Object.values(output).forEach((value) => {
//       var cell = row.append("td");
//       cell.text(value);
//     });
//   });
// }
// original churn 

function churn(customerID) {
  d3.json(`/churn/${customerID}`).then((churn) => {
    console.log(" data from /churn/:id", churn)

      // Use d3.json to fetch get_data 

    var churn_value = d3.select("#churn");

    churn_value.html("");

    var churnrow = churn_value.html(`<h3 style="margin:5px">${churn}%  `);

  });
}


function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/id").then((sampleNames) => {
    // console.log(sampleNames);
    sampleNames.forEach((customerID) => {
      selector
        .append("option")
        .text(customerID)
        .property("value", customerID);
    });
    console.log("dropdown has been built")
 // Use the first sample from the list to build the initial plots
     const firstSample = sampleNames[0];
     buildMetadata(firstSample);
     churn(firstSample);
     calculator(firstSample);
  });
}

function optionChanged(newSample) {
// Fetch new data each time a new sample is selected
   buildMetadata(newSample);
   churn(newSample);
   calculator(newSample);
 }


// Initialize the dashboard
init();
