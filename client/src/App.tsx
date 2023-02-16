import { useState } from 'react'
import axios from 'axios'


function App() {
  const [date, setData] = useState('')
  const [specified_file, setSpecifiedFile] = useState('')
  const url = `http://127.0.0.1:8000/${date}/${specified_file}`

  const fetchData = async () => {
    const result = await axios.get(url)
    return result
  }
  
  return (
    <div>
      <input type="text" value={date} onChange={e => setData(e.target.value)} />
      <input type="text" value={specified_file} onChange={e => setSpecifiedFile(e.target.value)} />
      <button onClick={fetchData}>Fetch Data</button>
    </div>
  )
}

export default App