import React, { useState } from "react";
import axios from "axios";
import AnalysisResult from "./components/AnalysisResult";

function App() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      const response = await axios.post("http://localhost:8000/analyze", {
        query: query,
      });
      console.log(response);
      setResult(response.data.result);
    } catch (error) {
      console.error("Error:", error);
      setResult({
        output: { type: "text", data: "Error occurred." },
        explanation: "",
      });
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-blue-50 flex flex-col items-center justify-start py-10 px-4">
      <div className="w-full max-w-3xl bg-white shadow-xl rounded-2xl p-8 border border-blue-200">
        <h1 className="text-3xl font-extrabold text-blue-700 mb-6 text-center">
          Air Quality Query Assistant
        </h1>

        <textarea
          rows={4}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full p-4 border border-blue-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400 transition mb-6"
          placeholder="Ask your question..."
        />

        <button
          onClick={handleAnalyze}
          disabled={loading}
          className={`w-full py-3 rounded-xl font-semibold text-white transition ${
            loading
              ? "bg-blue-400 cursor-not-allowed"
              : "bg-blue-600 hover:bg-blue-700"
          }`}
        >
          {loading ? "Analyzing..." : "Analyze"}
        </button>

        <div className="mt-8">
          <AnalysisResult result={result} />
        </div>
      </div>
    </div>
  );
}

export default App;
