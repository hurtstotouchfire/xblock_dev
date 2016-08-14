/* Javascript for SIRSimulatorXBlock. */
function SIRSimulatorXBlock(runtime, element) {

  function formtoJSON(form) {
    // Returns a nice flat object like {form-element-name: form-element-value}
    // Make sure your form elements are uniquely named
    var obj = {};
    form.serializeArray().map(function(elem){obj[elem.name] = elem.value;});
    return JSON.stringify(obj);
  }

  function descriptionSubmitted(response) {
    console.log(response);
  }

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
    
    function runSimulation(population, rNum, callback) {
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
      
      callback(timeSeries, 0.6 * population, 0.6 * population);
    };
        
    function displaySimulation(populationGetter, rNumGetter) {
      // Run the simulation and build the graph
      var population = populationGetter();
      var rNum = rNumGetter();
      runSimulation(population, rNum, configureChart);
    };

  $(function ($) {
    function getReproductionNum() { 
      var currentValue = $('#reproduction_num')[0].value;
      return Number(currentValue); 
    };
    function getPopulation() {
      var currentValue = $('#population')[0].value;
      return Number(currentValue); 
    };   

    $('.js-run-simulation').click(function(eventObject) {
      displaySimulation(getPopulation, getReproductionNum);
    });

    // Run simulation with default values
    displaySimulation(getPopulation, getReproductionNum);
  });
}
