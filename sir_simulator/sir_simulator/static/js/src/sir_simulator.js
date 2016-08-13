/* Javascript for SIRSimulatorXBlock. */
function SIRSimulatorXBlock(runtime, element) {

    function updateCount(result) {
        $('.count', element).text(result.count);
    }

    var handlerUrl = runtime.handlerUrl(element, 'increment_count');

    $('p', element).click(function(eventObject) {
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify({"hello": "world"}),
            success: updateCount
        });
    });

    $(function ($) {
        
        
      // go get highcharts? or use addjavascript or whatever.  
        
        
        function configureChart(timeSeries) {
  jQuery('#SIRSimulatonGraph').highcharts({
    chart: {
      type: 'column'
    },
    title: {
      text: ''
    },
    subtitle: {
      text: ''
    },
    yAxis: {
      min: 0,
      title: {
        text: 'Infected over time'
      },
      labels: {
        formatter: function() {
          return this.value + '%';
        }
      }
    },
    legend: {
      enabled: false
    },
    tooltip: {
      pointFormat: "Total infected: <b>{point.I}</b>"
    },
    series: [{
      name: 'Infected',
      data: timeSeries,
      dataLabels: {
        enabled: true,
        rotation: 0,
        color: '#FFFFFF',
        align: 'right',
        format: '{point.y:.0f}% ', // the trailing space is padding. Forgive me.
        x: 0
      }
    }]
  });
};

function runSimulation(N,b) {
      var max_t = 20;
      var I = 1;
      var S = N-1;
      var timeSeries = [{t:0, I:I}];
      for (t = 1; t < max_t; t++) {
          var p_inf = 1.0-Math.exp(-b*I/N);
          var new_I = 0;
          for (i = 0; i < S; i++) {
              if (Math.random() < p_inf) {
                  new_I++;
              }
          }
          if (new_I == 0) {
              break;
          }
          incidence.push({t:t, I:new_I});
          S -= new_I;
          I = new_I;
      }
      return(timeSeries);
  }

// actually do the things
  timeSeries = runSimulation(50, 1.5);
  configureChart(timeSeries);
        
        
        
        
    });
}
