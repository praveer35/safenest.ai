import React, { useEffect, useState } from 'react';
import { ReactGoogleChartEvent, Chart } from 'react-google-charts';
import axios from 'axios';
import './Charter.css';

export const vitalsOptions = {
  title: 'Baby Vitals',
  titleTextStyle: {color: 'white'},
  hAxis: {
    title: "Time",
    textStyle: {color: 'white'}
  },
  vAxis: {
    title: "Value",
    textStyle: {color: 'white'},
    viewWindowMode: 'explicit',
    viewWindow: {
        max: 125,
        min: 75,
        interval: 1,
    }
  },
  legend: {
    textStyle: {color: 'white'}
  },
  series: {
    0: {
      curveType: "function"
    },
    1: {
      curveType: "function"
    },
    2: {
      type: "scatter",
      visibleInLegend: false
    }
  },
  backgroundColor: 'black'
};

export const aiOptions = {
  title: 'Baby Danger Level',
  titleTextStyle: {color: 'white'},
  hAxis: {
    title: "Time",
    textStyle: {color: 'white'}
  },
  vAxis: {
    title: "Danger",
    textStyle: {color: 'white'},
    viewWindowMode: 'explicit',
    viewWindow: {
        max: 100,
        min: 0,
        interval: 1,
    }
  },
  legend: {
    textStyle: {color: 'white'}
  },
  series: {
    0: {
      curveType: "function"
    },
    1: {
      curveType: "function"
    },
    2: {
      curveType: "function"
    },
    3: {
      curveType: "function"
    },
    4: {
      curveType: "function"
    },
    5: {
      curveType: "function"
    },
    6: {
      curveType: "function"
    },
    7: {
      type: "scatter",
      visibleInLegend: false
    }
  },
  backgroundColor: 'black'
};

export const chartEvents: ReactGoogleChartEvent[] = [
  {
    eventName: "select",
    callback: ({ chartWrapper }) => {
      const chart = chartWrapper.getChart();
      const selection = chart.getSelection();
      if (selection.length === 1) {
        const [selectedItem] = selection;
        const dataTable = chartWrapper.getDataTable();
        const { row, column } = selectedItem;
        if (column === 3) {
          alert("You selected:" + 
            row + " " +
            column + " " +
            dataTable?.getValue(row, column)
          );
        }
      }
    },
  },
];

const Charter: React.FC = () => {
  const [vitalsData, setVitalsData] = useState<any[]>([]);
  const [aiData, setAIData] = useState<any[]>([]);

  // useEffect(() => {
  //   fetch('http://127.0.0.1:1601/data')
  //     .then(response => response.json())
  //     .then(data => setData(data))
  //     .catch(error => console.error('Error fetching data:', error));
  // }, []);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:1601/vitals-data');
        //alert(response.data);
        setVitalsData(response.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
      try {
        const response = await axios.get('http://localhost:1601/ai-data');
        //alert(response.data);
        setAIData(response.data);
      } catch(error) {
        console.error('Error fetching data:', error);
      }
    };

    setTimeout(function() { fetchData() }, 1000);

    //fetchData(); // Initial fetch

    const intervalId = setInterval(fetchData, 1000); // Fetch data every 5 seconds

    return () => clearInterval(intervalId); // Cleanup on unmount
  }, []);

  return (
    <div>
      {/* <h1>Line Chart from Python Backend</h1> */}
      {vitalsData.length > 0 ? (
        <Chart
          chartType="LineChart"
          width="100%"
          height="400px"
          data={vitalsData}
          options={vitalsOptions}
          chartEvents={chartEvents}
        />
      ) : (
        <p>Vital data loading...</p>
      )}
      {aiData.length > 0 ? (
        <Chart
          chartType="LineChart"
          width="100%"
          height="400px"
          data={aiData}
          options={aiOptions}
          chartEvents={chartEvents}
        />
      ) : (
        <p>AI data loading...</p>
      )}
    </div>
  );
};

export default Charter;