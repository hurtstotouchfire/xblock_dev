/* Javascript for SIRSimulatorXBlock. */
function SIRSimulatorXBlock(runtime, element) {

  /**
   * Configures chart using highcharts and inserts it in the page.
   *
   * @param {highcharts series} timeSeries - The data to display in the chart.
   * Must be in one of the acceptable highcharts series formats. Currently
   * an array of objects, each of which gives an x and y value in the form:
   * [{t:0, y:1}, {t:1, y:5}]
   *
   * @param {Number} xMax - The max x axis value
   * @param {Number} yMax - The max y axis value
   * Max for x and y axes is fixed rather than fitting the data to facilitate
   * visually comparing between the results of different simulation parameters.
   */
  function configureChart(timeSeries, xMax, yMax) {
    $('#js-sir-simulaton-graph').highcharts({
      chart: {
        type: 'column'
      },
      title: {
        text: ''
      },
      xAxis: {
        min: 0,
        max: xMax
      },
      yAxis: {
        min: 0,
        max: yMax,
        title: {
          text: 'Infected population',
          align: 'high'
        },
        labels: {
          overflow: 'justify'
        }
      },
      plotOptions: {
        bar: {
          dataLabels: {
            enabled: true
          }
        }
      },
      credits: {
        enabled: false
      },
      series: [{
        name: 'Infections over time',
        data: timeSeries
      }]
    });
  };
  
  /**
   * Runs the simulation and kicks off the chart building when it's done.
   *
   * @param {Integer} population - the total population for the simulation.
   * Regardless of total population, there will be only 1 Patient Zero.
   * For run time practicality, this should be limited to 10-100.
   * @param {Float} rNum - The basic reproduction number of the virus. 
   * To be realistic, this should be limited to 0-10.
   * See https://en.wikipedia.org/wiki/Basic_reproduction_number
   *
   * @param {Function} chartCallback - the function to build the chart.
   */
  function runSimulation(population, rNum, chartCallback) {
    // simulation parameters
    var max_t = population;
    var I = 1; // initial infected person
    var S = population - 1; // initial susceptible population
    var timeSeries = [{t:0, y:I}]; // initial time point
    
    // simulation helpers
    function infectionProbability(currentlyInfected) {
      return 1.0 - Math.exp(-rNum*currentlyInfected/population);
    };
    
    function newInfectionsPerTimePoint(p_inf) {
      var new_I = 0;
      for (i = 0; i < S; i++) {
        if (Math.random() < p_inf) { new_I++; };
      };
      return new_I;
    };
    
    // run simulation 
    for (t = 1; t < max_t; t++) {
      var p_inf = infectionProbability(I);
      var newlyInfected = newInfectionsPerTimePoint(p_inf);
      if (newlyInfected == 0) {
        // stop creating timepoints when no one is infected
        break;
      };
      timeSeries.push({t:t, y:newlyInfected});
      // remove newly infected from the susceptible population
      S -= newlyInfected;
      // update infected count for next time step
      I = newlyInfected;
    };
    
    chartCallback(timeSeries, 0.6 * population, 0.6 * population);
  };
  
  /**
   * Gathers simulation parameters from the page and runs simulation
   * @param {Function} populationGetter - gets the current population parameter
   * from the loaded page.
   * @param {Function} rNumGetter - gets the current rNum parameter from the
   * loaded page.
   */
  function displaySimulation(populationGetter, rNumGetter) {
    // Run the simulation and build the graph
    var population = populationGetter();
    var rNum = rNumGetter();
    runSimulation(population, rNum, configureChart);
  };

  /**
   * Serializes form elements
   * @param {JQuery object} $form - The form to serialize
   * @returns {String} Stringified JSON in the format:
   * {form-element-name: form-element-value}
   * Form elements must be uniquely named.
   */
  function formtoJSON($form) {
    var obj = {};
    $form.serializeArray().map(function(elem){obj[elem.name] = elem.value;});
    return JSON.stringify(obj);
  }

  /**
   * does success things
   * @param {object} response - The ajax response
   */
  function descriptionSubmitted(response) {
    console.log(response);
  }

  /***************************************************************************** 
   * Handler for submitting simulation description
   ****************************************************************************/  

  var handlerUrl = runtime.handlerUrl(element, 'simulation_description');

  $('#js-sir-form').on('submit', function(eventObject) {
    eventObject.preventDefault();
    $.ajax({
      type: "POST",
      url: handlerUrl,
      data: formtoJSON($(this)),
      success: descriptionSubmitted
    });
  });

  /***************************************************************************** 
   * After page load:
   * * define getters
   * * run simulation with current params
   ****************************************************************************/  

  $(function ($) {
    // Define getters
    function getReproductionNum() { 
      var currentValue = $('#reproduction_num')[0].value;
      return Number(currentValue); 
    };
    function getPopulation() {
      var currentValue = $('#population')[0].value;
      return Number(currentValue); 
    };   

    // Add click behavior to "Run simulation" button
    $('.js-run-simulation').click(function(eventObject) {
      displaySimulation(getPopulation, getReproductionNum);
    });

    // Run simulation with current values
    displaySimulation(getPopulation, getReproductionNum);
  });
}
