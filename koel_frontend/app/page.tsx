"use client"
import React, { useEffect, useState } from 'react';
import { fetchAnimals, fetchUsers } from './lib/dataFetching';
import Image from 'next/image';

const HomePage: React.FC = () => {
  const [animals, setAnimals] = useState<any[]>([]);
  const [users, setUsers] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  
  const fetchData = async () => {
    setLoading(true);
    const fetchedAnimals = await fetchAnimals();
    const fetchedUsers = await fetchUsers();
    setAnimals(fetchedAnimals);
    setUsers(fetchedUsers);
    setLoading(false);
    };


    
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [fetchedImg, setFetchedImg] = useState(null);

  const handleFileChange = (event:any) => {
    const file = event.target.files[0];
    setSelectedFile(file);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
      setUploading(true);
      const response = await fetch('http://127.0.0.1:8000/api/predict', {
            method: 'POST',
            body: formData,
      });
  
      const data = await response.json();
      console.log('response data:', data);
      
      return data;

    } catch (error) {
      console.error('Error detecting:', error);
      return []

    } finally {
      setUploading(false);
    }
  };  

  return (
    <div>
      <h1>Welcome to the Main Page</h1>
      <button onClick={fetchData} disabled={loading}>
        {loading ? 'Fetching Data...' : 'Fetch Data'}
      </button>
      <h2>Animals:</h2>
      <ul>
        {animals.map(animal => (
          <li key={animal.id}>{animal.species_name}</li>
        ))}
      </ul>
      <h2>Users:</h2>
      <ul>
        {users.map(user => (
          <li key={user.id}>{user.username}</li>
        ))}
      </ul>
      <div>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={uploading}>
        {uploading ? 'Detecting...' : 'Detect'}
      </button>
    </div>
    </div>
  );
};

export default HomePage;