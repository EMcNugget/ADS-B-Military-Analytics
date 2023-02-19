import { useState } from 'react';
import ReactJson from 'react-json-view';
import axios from 'axios';
import '../css/api.css';
import '../css/dropdown.css';


function Api() {
  const [date, setDate] = useState('');
  const [specified_file, setSpecifiedFile] = useState('');
  const [output, setOutput] = useState(null);
  const [lastClickedTime, setLastClickedTime] = useState<number>(0);
  const [color, setColor] = useState('gray');
  const url = `http://api.adsbmilanalytics.com/${date}/${specified_file}`

  const handleChange = (event: any) => {
    setSpecifiedFile(event.target.value);
    if (event.target.value !== 'Select an option...') {
      setColor('black');
    } else {
      setColor('gray');
    }
  };

  const fetchData = async () => {
    const result = await axios.get(url);
    setOutput(result.data);
  };

  const outputTheme = {
    base00: 'white',
    base01: '#ddd',
    base02: '#ddd',
    base03: '#444',
    base04: 'purple',
    base05: '#444',
    base06: '#444',
    base07: 'black',
    base08: '#cc6600',
    base09: '#ff9900',
    base0A: '#ffcc00',
    base0B: '#99cc00',
    base0C: '#3399cc',
    base0D: '#339999',
    base0E: '#cc99cc',
    base0F: '#666699',
    defaultValue: {
      string: '""',
      null: 'null',
      number: '0',
      boolean: 'false',
      array: '[]',
      object: '{}',
    },
    types: {
      number: ({ displayValue }: { displayValue: string }) => <span>{displayValue}</span>,
    },
  };


  const handleClick = () => {
    const currentTime = Date.now();
    if (currentTime - lastClickedTime < 10000) {
      alert('Please wait 10 seconds before fetching again.');
    } else {
      setLastClickedTime(currentTime);
      if (specified_file === 'Select an option...') {
        alert('Please select an option.');
      } else {
        fetchData();
      }
    }
  };

  return (
    <div className="container">
      <h1 className="title">ADS-B Military Analytics</h1>
      <div className="form">
        <input className="input" type="text" placeholder='Enter a date...' value={date} onChange={e => setDate(e.target.value)} />
        <select style={{color: color}} className="dropdown" value={specified_file} onChange={handleChange}>
          <option>Select an option...</option>
          <option value="stats">Aircraft Count</option>
          <option value="inter">Interesting Aircraft</option>
        </select>
        <button className="button" onClick={handleClick}>Fetch Data</button>
      </div>
      {output && (
        <div className="output">
          <ReactJson src={output} theme={outputTheme} />
        </div>
      )}
    </div>
  );
};

export default Api