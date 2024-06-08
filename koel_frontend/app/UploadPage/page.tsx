"use client";
import React, { useEffect, useState } from 'react';
import { fetchAnimals, fetchUsers } from '@/app/lib/dataFetching';
import Map from "@/app/Components/map/map";
import Filters from "@/app/Components/Filter/map_filter"
import BaseLayout from '@/app/Components/BaseLayout/BaseLayout';
import "./Upload.css"
import AudioPlayer from '@/app/Components/AudioPlayer/AudioPlayer';
import SearchIcon from "@/app/Icons/search-icon.svg"
import Image from 'next/image';
import AniSpecies from '@/app/Components/AniSpecies/AniSpecies';


const UploadPage: React.FC = () => {
  // const audioUrl = '/STRAW-HEADED BULBUL.mp3'; 
  const [fileName, setFileName] = useState("");
  const [loading, setLoading] = useState(false);
  
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [fetchedImg, setFetchedImg] = useState(null);
  const [uploadComplete, setUploadComplete] = useState(false);
  const [animalSpec, setanimalSpec] = useState({});

  // const animalspec  = {"Straw-Headed BulBul":{0:1,1:1,2:0,3:0,4:1,5:1},"Koel":{0:0,1:0,2:0,3:0,4:1,5:0},"Pigeon":{0:1,1:0,2:0,3:0,4:0,5:0}}

  const handleFileChange = (event:any) => {
    const file = event.target.files[0];
    setSelectedFile(file);
    console.log(file);
    setFileName(file.name);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('audio', selectedFile);
    
    // setUploadComplete(true);

    try {
      setUploading(true);
      const response = await fetch('http://127.0.0.1:8000/api/predict_audio', {
            method: 'POST',
            body: formData,
      });
  
      const data = await response.json();
      console.log('response data:', data);
      setanimalSpec(data.scores)

      setUploadComplete(true);

      return data;

    } catch (error) {
      console.error('Error detecting:', error);
      return []

    } finally {
      setUploading(false);
    }
  };  

  const handleDownload = async () => {
    setLoading(true);
    try {
        const response = await fetch('http://127.0.0.1:8000/api/predict_with_csv', {
            method: 'POST',
        });

        const blob = await response.blob(); // Convert response to blob

        // Create a URL for the blob object
        const url = URL.createObjectURL(blob);

        // Create a link element to trigger the download
        const link = document.createElement('a');
        link.href = url;
        link.download = 'csv_outputs.csv'; // Specify the filename here
        document.body.appendChild(link);

        // Click the link to start the download
        link.click();

        // Clean up
        URL.revokeObjectURL(url);

        return;

    } catch (error) {
        console.error('Error detecting:', error);
        return [];

    } finally {
        setLoading(false);
    }
  };

  const handleSearch = () => {
    // Implement upload functionality here
    console.log('Search button clicked');
  };




  return (
    <div>
      <BaseLayout>
      <div>
        <div className="text-5xl font-bold mb-10">Recording Page</div>
        <div className="">
          <div className="FileExplorer flex items-center">
          <div className="SearchForm">
            <div className="SearchBar">
              <p className="text-lg">{fileName}</p>
              

            </div>

            </div>
            <div className="ml-4 flex justify-center items-center">
            <label className="button_search">
                <input type="file" hidden accept="audio/*" onChange={handleFileChange}/> 
                <Image src={SearchIcon} className="search_logo" alt="Hamburger Icon"/>
            </label>

              <button className="button" onClick={handleUpload} disabled={uploading}>
                {uploading ? 'Detecting...' : 'Detect'}
              </button>
              
              <button 
                className="button"
                onClick={handleDownload}
              >
                Download CSV
              </button>
          </div>

          </div>

        </div>

        <div className='AudioPlayer'>
          <div>
          

          {selectedFile && <AudioPlayer audioUrl={URL.createObjectURL(selectedFile)} />}

          </div>


          <div>
            {uploadComplete && <AniSpecies animalspec={animalSpec} />}
          </div>
        </div>
        </div>
      </BaseLayout>
    </div>
  );
};

  
  export default UploadPage;