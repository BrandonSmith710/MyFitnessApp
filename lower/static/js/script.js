function plotRatings(ratings, num_ratings) {
    let x = [];
    for (let i = 1; i <= num_ratings; i++) {
        x.push(i)
    };
    var data = {
        x: x,
        y: ratings,
        type: 'scatter'
    };
    var layout = {
        xaxis: {range: [1, num_ratings]},
        title: 'Wellness Over the Past 15 days'
    };
    TESTER = document.getElementById('tester')
    Plotly.newPlot(TESTER,
        [data],
        layout,
        {margin: {t: 0 }});
};


function ratingsToNumbers(ratings) {
    for (let i = 0; i < ratings.length; i++) {
        let c = ratings[i];
        ratings[i] = Number(c);
    };
};

var Sentiment = require("sentiment");
var sentimentAnalyzer = new Sentiment();

