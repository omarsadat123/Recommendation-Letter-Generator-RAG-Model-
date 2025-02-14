import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import AnimatedSelect from "./AnimatedSelect";

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first!");
      return;
    }

    setData(null);
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(
        "http://localhost:5000/upload",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );

      setData(response.data);
      setLoading(false);
      console.log(response.data);
     
    } catch (error) {
      setLoading(false);
      console.error("Error uploading file:", error);
    }
  };

  useEffect(() => {
    console.log(data);
    if(data)
      {
        navigate("/try",{ state: { data: data } });
      }
  }, [data]);

  return (
    <div className="flex justify-center items-center h-screen bg-gray-100 p-6">
      <div className="bg-white shadow-xl rounded-lg p-8 w-full max-w-md">
      
        <h2 className="text-2xl font-semibold text-center text-gray-800 mb-6 ">
          Upload a Text File
        </h2>
        <div className="space-y-4">
          <div className="flex justify-center">
            <div className="font-[sans-serif] max-w-md mx-auto w-full">
             
              <input
                type="file"
                accept=".txt"
                className="w-full text-gray-400 font-semibold text-sm bg-white border file:cursor-pointer cursor-pointer file:border-0 file:py-3 file:px-4 file:mr-4 file:bg-gray-100 file:hover:bg-gray-200 file:text-gray-500 rounded"
                onChange={handleFileChange}
              />
             
            </div>
          </div>
          <div className="flex justify-center">
            <button
              onClick={handleUpload}
              className="w-full bg-pink-600 text-white text-lg font-semibold py-2 rounded-lg hover:bg-blue-700 transition-all duration-300"
            >
              Upload
            </button>
          </div>
        </div>

        {loading && (
          <div className="flex justify-center mt-4">
            <div className="text-gray-600">Loading...</div>
          </div>
        )}

        {data && (
          <div className="mt-6 space-y-4">
            <div className="bg-blue-50 p-4 rounded-lg">
              <h4 className="font-semibold text-gray-700">User Text:</h4>
              <pre className="text-gray-600">{data.user_text}</pre>
            </div>
            <div className="bg-blue-50 p-4 rounded-lg">
              <h4 className="font-semibold text-gray-700">Final Rating:</h4>
              <pre className="text-gray-600">{data.final_rating}</pre>
            </div>
            <div className="bg-blue-50 p-4 rounded-lg">
              <h4 className="font-semibold text-gray-700">Predicted Level:</h4>
              <pre className="text-gray-600">{data.predicted_level}</pre>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default FileUpload;
