"use client";
import { useState } from "react";
import axios from 'axios';

export default function Home() {
  const [url, setUrl] = useState(""); // Store URL
  const [query, setQuery] = useState(""); // Store query
  const [results, setResults] = useState([]); // Store results
  const [arr, setArr] = useState(Array(10).fill(0)); // Store array of 10 elements initialized to 0
  // Handle the search
  const handleSearch = async () => {
    const data = { url, query };
    try {
        const response = await axios.get('http://127.0.0.1:8000', {
          params: { "query": query,"url":url }
        });
        setResults(JSON.parse(response.data)); // Set the results from the response
        console.log(results[0]); // Log the results for debugging
      } catch (error) {
        console.error('Error fetching:', error);
      }
  };

  return (
    <div className="flex flex-col items-center p-8 space-y-4">
      <h1 className="text-3xl font-bold">Search App</h1>

      <div className="flex flex-col items-center space-y-2">
        <label className="text-lg font-medium">Enter URL:</label>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter URL"
          className="p-2 border-2 border-gray-300 rounded-md w-64"
        />
      </div>

      <div className="flex flex-col items-center space-y-2">
        <label className="text-lg font-medium">Enter Query:</label>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter Query"
          className="p-2 border-2 border-gray-300 rounded-md w-64"
        />
      </div>

      <button
        onClick={handleSearch}
        className="bg-blue-500 text-white px-6 py-2 rounded-md hover:bg-blue-600 transition duration-200"
      >
        Search
      </button>

      {/* Display the results */}
      <div className="mt-6 w-full ">
        {results.length > 0 ? (
          results.slice(0, 10).map((result, index) => (
            <div  className="p-3 border-2  border-gray-200 mb-2 rounded-md  w-full ">
                <div className="w-full flex mb-[1%]">
                    <span>{result["text"]}</span>
                    <div className="w-[80%] flex justify-end">Score:{result["score"]}</div>
                </div>
                <button className="bg-blue-500  rounded p-[0.5%] " onClick={()=>{
                    arr[index] = arr[index] ^ 1;
                    setArr([...arr]);
                    }}> show </button>
                { arr[index] === 1  && ( <>
                       <pre>{result["dom"]}</pre> 
                </>)}
            </div>
            
          ))
        ) : (
          <p className="text-gray-500">No results to display</p>
        )}
      </div>
    </div>
  );
}
