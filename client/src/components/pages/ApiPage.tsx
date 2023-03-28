/* eslint-disable @typescript-eslint/no-explicit-any */
import { useState } from "react";
import axios from "axios";
import Footer from "../libs/footer";
import { FaRegQuestionCircle, FaArrowRight, FaArrowLeft } from "react-icons/fa";
import { getSunday, getMonth } from "../libs/date";
import {
  useReactTable,
  createColumnHelper,
  Row,
  ColumnDef,
  getCoreRowModel,
  getPaginationRowModel,
  flexRender,
} from "@tanstack/react-table";
import Header from "../libs/header";
import "../../scss/api.scss";

// Main data type

type MainData = {
  hex: string;
  flight: string;
  r: string;
  t: string;
  squawk: string;
};

// ---Interesting Aircraft---

type InterestingAircraft = MainData; // Uses the same data. It's setup for clarity and future expansion

const inter = createColumnHelper<InterestingAircraft>();

const createInterColumn = (
  id: string,
  header: any, // eslint-disable-line
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

const hexHandler = (hex: string) => {
  window.open(`https://globe.adsbexchange.com/?icao=${hex}`, "_blank");
};

// ---Aircraft Count---

type AircraftCount = {
  type: string;
  value: number;
};

const ac_count = createColumnHelper<AircraftCount>();

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

// ---Stats---

type Stats = {
  max: {
    type: string;
    value: number;
  };
  sum: {
    date: string;
    value: number;
  }[];
  mean: number;
};

type orginalData = {
  max: {
    [key: string]: number;
  };
  sum: {
    [key: string]: number;
  };
  mean: number;
};

const stats = createColumnHelper<Stats>();

const statsColumns = (): ColumnDef<Stats, unknown>[] => {
  return [
    stats.group({
      id: "max",
      header: "Max",
      columns: [
        stats.display({
          id: "type",
          header: "Aircraft Type",
          cell: ({ row }: { row: Row<Stats> }) => (
            <span>{row.original.max.type}</span>
          ),
        }),
        stats.display({
          id: "value",
          header: "Aircraft Count",
          cell: ({ row }: { row: Row<Stats> }) => (
            <span>{row.original.max.value}</span>
          ),
        }),
      ],
    }),
    stats.group({
      id: "stats",
      header: "Stats",
      columns: [
        stats.display({
          id: "type",
          header: () => <span>Date</span>,
          cell: ({ row }: { row: Row<Stats> }) => (
            <span>
              {row.original.sum.map((item) => (
                <div>{item.date}</div> // eslint-disable-line
              ))}
            </span>
          ),
        }),
        stats.display({
          id: "value",
          header: "Total Aircraft",
          cell: ({ row }: { row: Row<Stats> }) => (
            <span>
              {row.original.sum.map((item) => (
                <div>{item.value}</div> // eslint-disable-line
              ))}
            </span>
          ),
        }),
        stats.display({
          id: "mean",
          header: "Mean",
          cell: ({ row }: { row: Row<Stats> }) => (
            <span>{row.original.mean}</span>
          ),
        }),
      ],
    }),
  ];
};

// Hashmap for selecting the correct table

interface TableMap {
  [key: string]: ColumnDef<any, unknown>[]; // eslint-disable-line
}

const tableMap: TableMap = {
  inter: interColumns(),
  stats: countColumns(),
  eow: statsColumns(),
  eom: statsColumns(),
};

function Api() {
  const [date, setDate] = useState("");
  const [specified_file, setSpecifiedFile] = useState("");
  const [output, setOutput] = useState<any>([]);
  const [tableVar, setTableVar] = useState<any[]>([]); // Accepts both InterestingAircraft and Stats will update to be more specific later
  const [lastClickedTime, setLastClickedTime] = useState<number>(0);
  const [color, setColor] = useState("gray");
  const url = `https://unified-dragon-378823.uc.r.appspot.com//${date}/${specified_file}`;

  function convertData(originalData: orginalData): Stats {
    const maxKey = Object.keys(originalData.max)[0];
    const maxValue = originalData.max[maxKey];
    const maxObj = { type: maxKey, value: maxValue };

    const sumData = Object.keys(originalData.sum).map((key) => ({
      date: key,
      value: originalData.sum[key],
    }));

    const mainData: Stats = {
      max: maxObj,
      sum: sumData,
      mean: originalData.mean,
    };
    return mainData;
  }

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
        result.status === 406 ||
        result.status === 403
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
      }
      if (specified_file === "eow" || specified_file === "eom") {
        setOutput(convertData(result.data));
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
      setTableVar(tableMap[specified_file]);
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
      <Header />
      <h2>Historical Data</h2>
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
      </div>
      <button className="button_data" onClick={handleClick}>
        Fetch Data
      </button>
      <div className="output">
        {output.length > 2 && (
          <table className="outputtable" onChange={handleChange}>
            <thead>
              {table.getHeaderGroups().map((headerGroup) => (
                <tr key={headerGroup.id}>
                  {headerGroup.headers.map((header) => (
                    <th key={header.id} colSpan={header.colSpan}>
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
          </table>
        )}
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
