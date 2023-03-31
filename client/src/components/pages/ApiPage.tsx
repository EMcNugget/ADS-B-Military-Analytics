/* eslint-disable @typescript-eslint/no-explicit-any */
import { useState, useEffect } from "react";
import axios from "axios";
import Footer from "../libs/footer";
import { FaRegQuestionCircle, FaArrowRight, FaArrowLeft } from "react-icons/fa";
import { Alert, Tooltip } from "@mui/material";
import { LoadingButton } from "@mui/lab";
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

const CreateInterestingAircraftColumns = (
  id: string,
  header: any,
  accessor: keyof InterestingAircraft,
  cursor = "text",
  onClick?: (row: Row<InterestingAircraft>) => void
) => {
  return inter.display({
    id,
    header,
    cell: ({ row }: { row: Row<InterestingAircraft> }) => (
      <span style={{ cursor: cursor }} onClick={() => onClick?.(row)}>
        {row.original[accessor]}
      </span>
    ),
  });
};

const InterestingAircraftColumns = (): ColumnDef<
  InterestingAircraft,
  unknown
>[] => {
  return [
    CreateInterestingAircraftColumns(
      "hex",
      <Tooltip title="Click to view on ADSB Exchange" placement="top-start">
        <span>
          Hex <FaRegQuestionCircle />
        </span>
      </Tooltip>,
      "hex",
      "pointer",
      (row) => {
        hexHandler(row.original.hex);
      }
    ),
    CreateInterestingAircraftColumns("flight", "Callsign", "flight"),
    CreateInterestingAircraftColumns("r", "Reg", "r"),
    CreateInterestingAircraftColumns("t", "Aircraft Type", "t"),
    CreateInterestingAircraftColumns("squawk", "Squawk", "squawk"),
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

const AircraftCountHelper = createColumnHelper<AircraftCount>();

const CreateAircraftCountColumn = (
  id: string,
  header: string,
  accessor: keyof AircraftCount
) => {
  return AircraftCountHelper.display({
    id,
    header,
    cell: ({ row }: { row: Row<AircraftCount> }) => (
      <span>{row.original[accessor]}</span>
    ),
  });
};

const AircraftCountColumns = (): ColumnDef<AircraftCount, unknown>[] => {
  return [
    CreateAircraftCountColumn("type", "Aircraft Type", "type"),
    CreateAircraftCountColumn("value", "Aircraft Count", "value"),
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
  };
  mean: number;
};

const StatisticsHelper = createColumnHelper<Stats>();

const StatisticsColumns = (): ColumnDef<Stats, unknown>[] => {
  return [
    StatisticsHelper.group({
      id: "max",
      header: "Max",
      columns: [
        StatisticsHelper.display({
          id: "type",
          header: "Aircraft Type",
          cell: ({ row }: { row: Row<Stats> }) => (
            <span>{row.original.max.type}</span>
          ),
        }),
        StatisticsHelper.display({
          id: "value",
          header: "Aircraft Count",
          cell: ({ row }: { row: Row<Stats> }) => (
            <span>{row.original.max.value}</span>
          ),
        }),
      ],
    }),
    StatisticsHelper.group({
      id: "sum",
      header: "Sum",
      columns: [
        StatisticsHelper.display({
          id: "type",
          header: "Date",
          cell: ({ row }: { row: Row<Stats> }) => (
            <span>{row.original.sum.date}</span>
          ),
        }),
        StatisticsHelper.display({
          id: "value",
          header: "Total Aircraft",
          cell: ({ row }: { row: Row<Stats> }) => (
            <span>{row.original.sum.value}</span>
          ),
        }),
      ],
    }),
    StatisticsHelper.display({
      id: "mean",
      header: "Mean",
      cell: ({ row }: { row: Row<Stats> }) => <span>{row.original.mean}</span>,
    }),
  ];
};

// Hashmap for selecting the correct table

interface TableMap {
  [key: string]: ColumnDef<any, unknown>[];
}

const tableMap: TableMap = {
  inter: InterestingAircraftColumns(),
  stats: AircraftCountColumns(),
  eow: StatisticsColumns(),
  eom: StatisticsColumns(),
};

function Api() {
  const [date, setDate] = useState("");
  const [specified_file, setSpecifiedFile] = useState("Select an option...");
  const [loading, setLoading] = useState(false);
  const [output, setOutput] = useState<any[]>([]);
  const [errors, setErrors] = useState<any>([]);
  const [tableDef, settableDef] = useState<ColumnDef<any, unknown>[]>([]);
  const [lastClickedTime, setLastClickedTime] = useState<number>(0);
  const [color, setColor] = useState("gray");
  const url = `https://unified-dragon-378823.uc.r.appspot.com//${date}/${specified_file}`;

  useEffect(() => {
    if (output.length === 0 || output.length > 0) {
      setLoading(false);
    }
  }, [output]);

  const ApiButton = () => {
    const isDisabled = specified_file === "Select an option..." || date === "";

    return (
      <LoadingButton
        variant="contained"
        className="button_data"
        onClick={handleClick}
        loading={loading}
        disabled={isDisabled}
      >
        <span>Fetch Data</span>
      </LoadingButton>
    );
  };

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
        setErrors(`Oops there was an error: ${result.status}`);
        setOutput([]);
      }
      if (result.status === 404) {
        setErrors(`Oops there was an error: ${result.status}`);
        setOutput([]);
      }
      if (
        result.data === null ||
        JSON.stringify(result.data) === '{"hex":"No aircraft found"}'
      ) {
        setErrors(`No aircraft found for ${date}.`);
        setOutput([]);
      }
      if (result.status === 200) {
        setOutput(result.data);
      }
    } catch (error: any) {
      setErrors(`Oops there was an error: ${error}`);
      setOutput([]);
      if (error.request.response === "") {
        setErrors(`There was an error fetching data. Please try again later. If the
        problem persists, please contact support@adsbmilanalytics.com`);
        setOutput([]);
      }
    }
  };

  const handleClick = () => {
    const currentTime = Date.now();
    if (currentTime - lastClickedTime < 10000) {
      setErrors("Please wait 10 seconds before fetching data again.");
    } else {
      settableDef(tableMap[specified_file]);
      fetchData();
      setLoading(true);
      setLastClickedTime(currentTime);
      table.setPageIndex(0);
      table.setPageSize(12);
    }
  };

  const table = useReactTable({
    columns: tableDef,
    data: output,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
  });

  return (
    <div className="container">
      {errors.length > 0 && (
        <Alert
          severity="error"
          style={{
            position: "absolute",
            top: 0,
            width: "40%",
            marginTop: "0.45rem",
          }}
        >
          {errors}
        </Alert>
      )}
      <Header />
      <h2>Historical Data</h2>
      <div className="input">
        <input
          aria-label="Date"
          className="inputdate"
          type="date"
          min="2023-03-09"
          max={new Date().toISOString().split("T")[0]}
          onChange={(e) => setDate(e.target.value)}
        />
        <select
          aria-label="Select an option"
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
      <ApiButton />
      <div className="output">
        {output.length > 0 && (
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
              aria-label="Previous Page"
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
              aria-label="Next Page"
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
