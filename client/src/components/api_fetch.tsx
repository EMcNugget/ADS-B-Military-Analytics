import { useState } from 'react';
import axios from 'axios';
import '../css/api.css';
import '../css/dropdown.css';


function Api() {
  const [date, setDate] = useState('');
  const [specified_file, setSpecifiedFile] = useState('');
  const [output, setOutput] = useState<any[]>([]);
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

  const inter = () => {
    return (
      <table className="output">
        <thead>
          <tr>
            <th>Hex</th>
            <th>Flight</th>
            <th>Reg</th>
            <th>Aircraft</th>
            <th>Squawk</th>
          </tr>
        </thead>
        <tbody>
          {output.map((item, index) => (
            <tr key={index}>
              <td>{item.hex}</td>
              <td>{item.flight}</td>
              <td>{item.r}</td>
              <td>{item.t}</td>
              <td>{item.squawk}</td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

  const ac_count = () => {
    return (
      <table className="output">
        <thead>
          <tr>
            <th>Aircraft</th>
            <th>Amount</th>
          </tr>
        </thead>
        <tbody>
          {output.map((item, index) => (
            <tr key={index}>
              <td>{item.aircraft}</td>
              <td>{item.count}</td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

  const tableSelect = () => {
    if (specified_file === 'inter') {
      return inter();
    } else if (specified_file === 'stats') {
      return ac_count();
    }
    else {
      return null;
    }
  };

  const fetchData = async () => {
    const result = await axios.get(url);
    setOutput(
      result.data.map((item: any) => {
        return {
          hex: item.hex,
          flight: item.flight,
          r: item.reg,
          t: item.aircraft,
          squawk: item.squawk,
        }
      })
    );
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
        <input className="input" type="text" placeholder='Enter a date...eg 2023-02-13' value={date} onChange={e => setDate(e.target.value)} />
        <select style={{ color: color }} className="dropdown" value={specified_file} onChange={handleChange}>
          <option>Select an option...</option>
          <option value="stats">Aircraft Count</option>
          <option value="inter">Interesting Aircraft</option>
        </select>
        <button className="button" onClick={handleClick}>Fetch Data</button>
      </div>
      {tableSelect()}
    </div>
  );
};

export default Api