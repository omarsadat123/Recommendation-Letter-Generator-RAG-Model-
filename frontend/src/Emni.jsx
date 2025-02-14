import React, { useState } from "react";
import { useLocation } from "react-router-dom";
import AnimatedSelect from "./AnimatedSelect";
import axios from "axios";
const Emni = () => {
  const location = useLocation();
  const { data } = location.state || {}; // Accessing the passed state
  const [selectOption,setSelectOption] = useState("");
  const [LOR,setLOR] = useState("");
  const [error,setError] = useState("");
  const handleSubmit =async (e)=>{
    

    setLOR(null);
    setError(null);
    e.preventDefault();
      if(data.user_text && selectOption)
      {

        console.log(data.user_text,selectOption);
        try {
          const response = await axios.post(
            "http://localhost:5000/emni",
            {
              userText: data.user_text,
              selectedOption:selectOption
            },
            {
              headers: { "Content-Type": "application/json" },
            }
          );
    
          console.log("emni response data",response.data.generated_lor);
          
          if(response.data.generated_lor)
          {
            setLOR(response.data.generated_lor);

          }
          else
          {
            setError(response.data.error);
          }
          
         
         
        } catch (error) {
        
          console.error("Error uploading file:", error);
        }
      }
      else{
        alert("Please select a level first!");
      }
  }

  return (
    <div>
      {data && (
        <div className="mt-6 space-y-4">

          {/* <div className="bg-blue-50 p-4 rounded-lg">
            <h4 className="font-semibold text-gray-700">User Text:</h4>
            <pre className="text-gray-600">{data.user_text}</pre>
          </div> */}
          <div className="bg-blue-50 p-4 rounded-lg">
            <h4 className="font-semibold text-gray-700">Final Rating:</h4>
            <pre className="text-gray-600">{data.final_rating}</pre>
          </div>
          <div className="bg-blue-50 p-4 rounded-lg">
            <h4 className="font-semibold text-gray-700">Predicted Level:</h4>
            <pre className="text-gray-600">{data.predicted_level}</pre>
          </div>
          <div className="bg-blue-50 p-4 rounded-lg">
            <AnimatedSelect setSelectOption={setSelectOption} selectOption={selectOption}/>
          </div>
          <div className="flex justify-center">
            <button
              onClick={handleSubmit}
              className="w-full bg-pink-600 text-white text-lg font-semibold py-2 rounded-lg hover:bg-blue-700 transition-all duration-300"
            >
              Submit
            </button>
          </div>
          {LOR && (
  <div className="bg-blue-50 p-4 rounded-lg">
    <div className="bg-white p-8 rounded-lg shadow-md max-w-2xl mx-auto font-serif">
      {/* Letterhead */}
      <div className="text-center mb-8 border-b-2 border-gray-300 pb-4">
        <div className="text-2xl font-bold text-gray-800 ">Stanford University</div>
        <div className="text-gray-600">Department of Computer Science</div>
        <div className="text-gray-600">353 Serra Mall, Stanford, CA 94305</div>
      </div>

      {/* Date */}
      <div className="text-right mb-6 text-gray-600">
        {new Date().toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'long',
          day: 'numeric'
        })}
      </div>

      {/* Recipient Address */}
      <div className="mb-8 text-gray-600 text-left">
        <div>Admissions Committee</div>
        <div>MIT Computer Science Graduate Program</div>
        <div>77 Massachusetts Avenue</div>
        <div>Cambridge, MA 02139</div>
      </div>

      {/* Salutation */}
      <div className="mb-4 text-left text-gray-800">Dear Members of the Admissions Committee,</div>

      {/* Letter Body */}
      <div className="whitespace-pre-line text-gray-800 leading-relaxed text-justify mb-8">
        {LOR}
      </div>

      {/* Closing */}
      <div className="mt-7">
        <div className="mb-1 text-left">Sincerely,</div>
        <div className="mb-1">
          <img 
            src="/signature.png" 
            alt="Signature" 
            className="text-right h-12 w-screen"
          />
        </div>
        <div className="text-gray-800 font-semibold mb-1 text-left">Dr. Jane Smith</div>
        <div className="text-gray-600 mb-1 text-left">Professor of Computer Science</div>
        <div className="text-gray-600 mb-1 text-left">Stanford University</div>
        <div className="text-gray-600 mb-1 text-left">
          Email: jsmith@stanford.edu | Phone: (650) 123-4567
        </div>
      </div>
    </div>
  </div>
)}

        </div>    
      )}
      {
        error && (
          <div className="text-red-600 text-center text-lg mb-4">
            {error}
          </div>
        )
      }
    </div>
  );
};

export default Emni;
