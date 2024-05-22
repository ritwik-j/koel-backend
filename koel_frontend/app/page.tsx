"use client"
import React, { useEffect, useState } from 'react';
import { fetchAnimals, fetchUsers } from './lib/dataFetching';

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
    </div>
  );
};

export default HomePage;