/* eslint-disable @typescript-eslint/no-explicit-any */
import { useState } from "react";
import axios from "axios";
import Footer from "./footer";
import { FaRegQuestionCircle, FaArrowRight, FaArrowLeft } from "react-icons/fa";
import { getSunday, getMonth } from "../util/date";
import {
  useReactTable,
  createColumnHelper,
  Row,
  ColumnDef,
  getCoreRowModel,
  getPaginationRowModel,
  flexRender,
} from "@tanstack/react-table";
import "../scss/api.scss";

type InterestingAircraft = {
  hex: string;
  flight: string;
  r: string;
  t: string;
  squawk: string;
};

type AircraftCount = {
  type: string;
  value: number;
};

const inter = createColumnHelper<InterestingAircraft>();
const ac_count = createColumnHelper<AircraftCount>();

const createInterColumn = (
  id: string,
  header: any,
  accessor: keyof InterestingAircraft,
  cursor: string,
  onClick: (row: Row<InterestingAircraft>) => void
) => {
  return inter.display({
    id,
    header,
    cell: ({ row }: { row: Row<InterestingAircraft> }) => (
      <span style={{ cursor: cursor }} onClick={() => onClick(row)}>
        {row.original[accessor]}
      </span>
    ),
  });
};

const hexHandler = (hex: string) => {
  window.open(`https://globe.adsbexchange.com/?icao=${hex}`, "_blank");
};

const interColumns = (): ColumnDef<InterestingAircraft, unknown>[] => {
  return [
    createInterColumn(
      "hex",
      <div className="tooltip">
        Hex <FaRegQuestionCircle />
        <span className="tooltiptext">
          Click on a hex to view the aircraft on ADS-B Exchange.
        </span>
      </div>,
      "hex",
      "pointer",
      (row) => {
        hexHandler(row.original.hex);
      }
    ),
    createInterColumn("flight", "Callsign", "flight", "text", () => {
      null;
    }),
    createInterColumn("r", "Reg", "r", "text", () => {
      null;
    }),
    createInterColumn("t", "Aircraft Type", "t", "text", () => {
      null;
    }),
    createInterColumn("squawk", "Squawk", "squawk", "text", () => {
      null;
    }),
  ];
};

const createCountColumn = (
  id: string,
  header: string,
  accessor: keyof AircraftCount
) => {
  return ac_count.display({
    id,
    header,
    cell: ({ row }: { row: Row<AircraftCount> }) => (
      <span>{row.original[accessor]}</span>
    ),
  });
};

const countColumns = (): ColumnDef<AircraftCount, unknown>[] => {
  return [
    createCountColumn("type", "Aircraft Type", "type"),
    createCountColumn("value", "Aircraft Count", "value"),
  ];
};

function Api() {
  const [date, setDate] = useState("");
  const [specified_file, setSpecifiedFile] = useState("");
  const [output, setOutput] = useState<any>({});
  const [tableVar, setTableVar] = useState<any[]>([]);
  const [lastClickedTime, setLastClickedTime] = useState<number>(0);
  const [color, setColor] = useState("gray");
  const url = `https://unified-dragon-378823.uc.r.appspot.com//${date}/${specified_file}`;

  const handleChange = (event: any) => {
    setSpecifiedFile(event.target.value);
    if (event.target.value === "eow") {
      setDate(getSunday(date));
    }
    if (event.target.value === "eom") {
      setDate(getMonth(date));
    }
    if (event.target.value !== "Select an option...") {
      setColor("white");
    } else {
      setColor("gray");
    }
  };

  const fetchData = async () => {
    try {
      const result = await axios.get(url);
      if (
        result.status === 500 ||
        result.status === 400 ||
        result.status === 406
      ) {
        alert(result.request.response);
        setOutput([]);
      }
      if (result.status === 404) {
        alert(`No data found for ${date}.`);
        setOutput([]);
      }
      if (
        result.data === null ||
        JSON.stringify(result.data) === '{"hex":"No aircraft found"}' // eslint-disable-line
      ) {
        alert("No aircraft found for this date.");
        setOutput([]);
      } else {
        setOutput(result.data);
      }
    } catch (error: any) {
      alert(error.request.response);
      if (error.request.response === "") {
        alert(
          "There was an error fetching data. Please try again later. If the problem persists, please contact support@adsbmilanalytics.com"
        );
      }
    }
  };

  const handleClick = () => {
    const currentTime = Date.now();
    if (specified_file === "Select an option...") {
      alert("Please select an option.");
      clearTimeout(currentTime);
      setTableVar([]);
      if (currentTime - lastClickedTime < 10000) {
        alert("Please wait 10 seconds before fetching again.");
      }
    } else {
      setTableVar(specified_file === "stats" ? countColumns() : interColumns());
      fetchData();
      setLastClickedTime(currentTime);
      table.setPageIndex(0);
      table.setPageSize(12);
    }
  };

  const table = useReactTable({
    columns: tableVar,
    data: output,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
  });

  return (
    <div className="container">
      <h1>ADS-B Military Analytics</h1>
      <div className="input">
        <input
          className="inputdate"
          type="date"
          min="2023-03-09"
          max={new Date().toISOString().split("T")[0]}
          value={date}
          onChange={(e) => setDate(e.target.value)}
        />
        <select
          style={{ color: color }}
          className="inputdropdown"
          value={specified_file}
          onChange={handleChange}
        >
          <option>Select an option...</option>
          <option value="stats">Amount of Aircraft</option>
          <option value="inter">Interesting Aircraft</option>
          <option value="eow">Weekly Stats</option>
          <option value="eom">Monthly Stats</option>
        </select>
        <button className="button_data" onClick={handleClick}>
          Fetch Data
        </button>
      </div>
      <div className="output">
        {output.length > 2 && (
          <table className="outputtable" onChange={handleChange}>
            <thead>
              {table.getHeaderGroups().map((headerGroup) => (
                <tr key={headerGroup.id}>
                  {headerGroup.headers.map((header) => (
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
            <tbody>
              {table.getRowModel().rows.map((row) => (
                <tr key={row.id}>
                  {row.getVisibleCells().map((cell) => (
                    <td key={cell.id}>
                      {flexRender(
                        cell.column.columnDef.cell,
                        cell.getContext()
                      )}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
            <tfoot>
              {table.getFooterGroups().map((footerGroup) => (
                <tr key={footerGroup.id}>
                  {footerGroup.headers.map((header) => (
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
        )}
      </div>
      <div>
        {output.length > 2 && (
          <div className="page">
            <button
              className="pagebutton"
              onClick={() => table.previousPage()}
              disabled={!table.getCanPreviousPage}
            >
              <FaArrowLeft />
            </button>
            <span className="pagebutton">
              <strong>
                Page {table.getState().pagination.pageIndex + 1} of{" "}
                {table.getPageCount()}
              </strong>
            </span>
            <button
              className="pagebutton"
              onClick={() => table.nextPage()}
              disabled={!table.getCanNextPage()}
            >
              <FaArrowRight />
            </button>
          </div>
        )}
      </div>
      <Footer />
    </div>
  );
}

export default Api;
