import { useState } from 'react';
import axios from 'axios';
import './css/api.css';


function Api() {
  const [date, setDate] = useState('');
  const [specified_file, setSpecifiedFile] = useState('');
  const [output, setOutput] = useState('')

  const url = `http://127.0.0.1:8000/${date}/${specified_file}`

  const fetchData = async () => {
    const result: string = await axios.get(url)
    setOutput(result)
  };
  
  return (
    <div className="container">
      <h1 className="title">ADSB Military Analytics</h1>
      <div className="form">
        <input className="input" type="text" placeholder='Enter a date' value={date} onChange={e => setDate(e.target.value)} />
        <input className="input" type="text" placeholder='Enter a file' value={specified_file} onChange={e => setSpecifiedFile(e.target.value)} />
        <button className="button" onClick={fetchData}>Fetch Data</button>
      </div>
      {output && <p className="output">{output}</p>}
    </div>
  );
};


export default Api