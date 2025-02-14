import  { useState } from 'react';

const AnimatedSelect = ({selectOption,setSelectOption}) => {
  //const [selectedOption, setSelectedOption] = useState("");

  const handleChange = (e) => {
    setSelectOption(e.target.value);
  };

  return (
    <div className="flex justify-center items-center">
      <div className="relative">
        <select
          value={selectOption}
          onChange={handleChange}
          className="block appearance-none w-64 p-3 pr-8 rounded-lg border-2 border-gray-300 bg-white text-gray-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all duration-300 ease-in-out text-center"
        >
          <option value="">Select a level</option>
          <option value="high">High</option>
          <option value="medium-high">Medium-High</option>
          <option value="medium">Medium</option>
          <option value="medium-low">Medium-Low</option>
          <option value="low">Low</option>
          <option value="dont-provide">Don't Provide</option>
        </select>
        
        <div className="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
          <svg
            className="w-5 h-5 text-gray-500"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M19 9l-7 7-7-7"
            ></path>
          </svg>
        </div>
      </div>
    </div>
  );
};

export default AnimatedSelect;
