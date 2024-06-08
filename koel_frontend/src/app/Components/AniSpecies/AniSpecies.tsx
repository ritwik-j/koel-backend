import React, { useState } from 'react';
import './AniSpecies.css';
import koelPic from "@/app/Icons/Asian_koel.jpg"
import Image from 'next/image';

// Define the type for animalspec
type Animalspec = {
  [key: string]: {
    [key: number]: number;
  };
};

type Props = {
  animalspec: Animalspec;
};

export default function AniSpecies({ animalspec }: Props) {
  const species = Object.keys(animalspec);
  const [moreInfo, setMoreInfo] = useState(false) 
  const [isBoxPressed, setIsBoxPressed] = useState(false);
    // Function to toggle the state
    const handleBoxPress = () => {
      setIsBoxPressed(!isBoxPressed);
    };

  const getTimeInterval = (index: number) => {
    const start = index * 3;
    const end = start + 2;
    return `${start}-${end} seconds`;
  };

  return (
    <div className="containerMain flex">
      <div>
      <div className="header">Animal Detected</div>
      <ul onClick={handleBoxPress}>
        {species.map((speciesName, index) => (
          <li className="container" key={index}>
            <div className='flex '>
            <Image src={koelPic} className="h-16 w-12 rounded" alt="KoelIcon" />
            <div className='ml-6 text-left'>
              <div>{speciesName}</div>            
              {isBoxPressed && (
                    <ul className="text-xl mt-4">
                      {Object.entries(animalspec[speciesName]).map(([key, value], subIndex) => (
                        value === 1 && (
                          <li key={subIndex}>
                            Time Interval: {getTimeInterval(Number(key))} (Detected)
                          </li>
                        )
                      ))}
                    </ul>)}
            </div>
            </div>
            </li>
        ))}
      </ul>

      </div>

      {/* <div >
              <div className="header">Animal Detected</div>
      <ul >
        {moreInfo && species.map((speciesName, index) => (
          <li className="container" key={index}>
            <div className='flex '>
            <Image src={koelPic} className="h-16 w-12 rounded" alt="KoelIcon" />
            <div className='ml-6'>{speciesName}</div>
            </div>
            </li>
        ))}
      </ul>
      </div> */}

    </div>
    
  );
}