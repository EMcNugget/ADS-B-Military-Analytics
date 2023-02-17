import { useState } from 'react';
import ReactJson from 'react-json-view';
import axios from 'axios';
import './css/api.css';


function Api() {
  const [date, setDate] = useState('');
  const [specified_file, setSpecifiedFile] = useState('');
  const [output, setOutput] = useState(null);

  const url = `http://127.0.0.1:5000/${date}/${specified_file}`

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

  return (
    <div className="container">
      <h1 className="title">ADSB Military Analytics</h1>
      <div className="form">
        <input className="input" type="text" placeholder='Enter a date' value={date} onChange={e => setDate(e.target.value)} />
        <input className="input" type="text" placeholder='Enter a file' value={specified_file} onChange={e => setSpecifiedFile(e.target.value)} />
        <button className="button" onClick={fetchData}>Fetch Data</button>
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