import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const AnalysisResult = ({ result }) => {
  if (!result || !result.output) return null;

  const { type, data } = result.output;
  const explanation = result.explanation;

  const isTabular = type === "table" && Array.isArray(data) && data.length > 0;

  // Automatically pick x and y keys for chart
  const numericKeys = isTabular
    ? Object.keys(data[0]).filter((key) => typeof data[0][key] === "number")
    : [];

  const xKey = isTabular ? Object.keys(data[0])[0] : null;
  const yKey = numericKeys[0] !== xKey ? numericKeys[0] : numericKeys[1];

  return (
    <div className="mt-6 p-4 bg-white rounded shadow">
      <h2 className="text-lg font-semibold mb-2 text-gray-800">Result:</h2>

      {isTabular ? (
        <>
          {/* Table */}
          <div className="overflow-x-auto mb-6">
            <table className="table-auto border-collapse w-full">
              <thead>
                <tr>
                  {Object.keys(data[0]).map((key) => (
                    <th
                      key={key}
                      className="px-4 py-2 border-b border-gray-300 bg-gray-100 text-left"
                    >
                      {key}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {data.map((row, idx) => (
                  <tr key={idx}>
                    {Object.values(row).map((value, i) => (
                      <td key={i} className="px-4 py-2 border-b">
                        {value}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Chart */}
          {xKey && yKey && (
            <div className="w-full h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey={xKey} />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey={yKey} stroke="#8884d8" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}

          {/* Explanation */}
          {explanation && (
            <div className="mt-4 text-sm text-gray-600">
              <strong>Explanation:</strong> {explanation}
            </div>
          )}
        </>
      ) : type === "text" ? (
        // For text type, only show explanation (ignore data)
        explanation ? (
          <div className="mt-2 p-3 bg-gray-50 border rounded text-gray-700 whitespace-pre-wrap">
            <strong>Explanation:</strong> {explanation}
          </div>
        ) : (
          <p>No explanation available.</p>
        )
      ) : (
        <p className="text-red-500">Unknown result type: {type}</p>
      )}
    </div>
  );
};

export default AnalysisResult;
