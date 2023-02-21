import { useState } from 'react';
import axios from 'axios';
import { useReactTable, createColumnHelper, Row, ColumnDef, getCoreRowModel, flexRender } from "@tanstack/react-table"
import { FaGithub } from 'react-icons/fa';
import '../css/api.css';
import '../css/dropdown.css';

type InterestingAircraft = {
  hex: string
  flight: string
  r: string
  t: string
  squawk: string
};

type AircraftCount = {
  type: string
  value: number
};

const inter = createColumnHelper<InterestingAircraft>()
const ac_count = createColumnHelper<AircraftCount>()

const interColumns = (): ColumnDef<InterestingAircraft, unknown>[] => {
  const columns = [
    inter.display({
      id: 'hex',
      header: 'Hex',
      cell: ({ row }: { row: Row<InterestingAircraft> }) => (
        <span>{row.original.hex}</span>
      ),
    }),
    inter.display({
      id: 'flight',
      header: 'Callsign',
      cell: ({ row }: { row: Row<InterestingAircraft> }) => (
        <span>{row.original.flight}</span>
      ),
    }),
    inter.display({
      id: 'r',
      header: 'Reg',
      cell: ({ row }: { row: Row<InterestingAircraft> }) => (
        <span>{row.original.r}</span>
      ),
    }),
    inter.display({
      id: 't',
      header: 'Aircraft Type',
      cell: ({ row }: { row: Row<InterestingAircraft> }) => (
        <span>{row.original.t}</span>
      ),
    }),
    inter.display({
      id: 'squawk',
      header: 'Squawk',
      cell: ({ row }: { row: Row<InterestingAircraft> }) => (
        <span>{row.original.squawk}</span>
      ),
    })
  ];

  console.log(columns); // here for debuging will remove for production

  return columns;
}



const countColumns = (): ColumnDef<AircraftCount, unknown>[] => {
  const columns = [
    ac_count.display({
      id: 'type',
      header: 'Aircraft Type',
      cell: ({ row }: { row: Row<AircraftCount> }) => (
        <span>{row.original.type}</span>
      ),
    }),
    ac_count.display({
      id: 'value',
      header: 'Count',
      cell: ({ row }: { row: Row<AircraftCount> }) => (
        <span>{row.original.value}</span>
      ),
    })
  ];

  console.log(columns); // here for debuging will remove for production

  return columns;
}

function Api() {
  const [date, setDate] = useState('');
  const [specified_file, setSpecifiedFile] = useState('');
  const [output, setOutput] = useState<any>({});
  const [tableVar, setTableVar] = useState<any[]>([]);
  const [lastClickedTime, setLastClickedTime] = useState<number>(0);
  const [color, setColor] = useState('gray');
  const url = `http://127.0.0.1:5000/${date}/${specified_file}`

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
    if (JSON.stringify(result.data) === '{"hex":"No aircraft found"}') {
      alert('No aircraft found for this date.');
      setOutput([]);
    }
    else {
      setOutput(result.data);
    }
  };

  const handleClick = () => {
    const currentTime = Date.now();
    if (specified_file === 'Select an option...') {
      alert('Please select an option.');
      clearTimeout(currentTime);
      setTableVar([]);
      if (currentTime - lastClickedTime < 10000) {
      } else {
        alert('Please wait 10 seconds before fetching again.');
      }
    } else {
      setLastClickedTime(currentTime);
      setTableVar(specified_file === 'stats' ? countColumns() : interColumns());
      fetchData();
    }
  };


  const table = useReactTable({
    columns: tableVar,
    data: output,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    <div className="container">
      <h1 className="title">ADS-B Military Analytics</h1>
      <div className="form">
        <input className="input" type="text" placeholder='Enter a date...eg 2023-02-20' value={date} onChange={e => setDate(e.target.value)} />
        <select style={{ color: color }} className="dropdown" value={specified_file} onChange={handleChange}>
          <option>Select an option...</option>
          <option value="stats">Aircraft Count</option>
          <option value="inter">Interesting Aircraft</option>
        </select>
        <button className="button" onClick={handleClick}>Fetch Data</button>
      </div>
      <div className="output">
        <table className='table' onChange={handleChange}>
          <thead>
            {table.getHeaderGroups().map(headerGroup => (
              <tr key={headerGroup.id}>
                {headerGroup.headers.map(header => (
                  <th key={header.id}>
                    {header.isPlaceholder
                      ? null
                      : flexRender(
                        header.column.columnDef.header,
                        header.getContext()
                      )}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody className='td'>
            {table.getRowModel().rows.map(row => (
              <tr key={row.id}>
                {row.getVisibleCells().map(cell => (
                  <td key={cell.id}>
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
          <tfoot>
            {table.getFooterGroups().map(footerGroup => (
              <tr key={footerGroup.id}>
                {footerGroup.headers.map(header => (
                  <th key={header.id}>
                    {header.isPlaceholder
                      ? null
                      : flexRender(
                        header.column.columnDef.footer,
                        header.getContext()
                      )}
                  </th>
                ))}
              </tr>
            ))}
          </tfoot>
        </table>
      </div>
      <div className="footer">
        <a href="https://github.com/EMcNugget/adsb_mil_data" target="_blank" rel="noopener noreferrer">
          <FaGithub className="icon" />
          GitHub
        </a>
        <p className="copy">&copy;2023 ADSB-Military-Analytics.</p>
      </div>
    </div>
  );
}

export default Api;