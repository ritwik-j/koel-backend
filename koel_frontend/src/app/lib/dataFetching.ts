export async function fetchAnimals(): Promise<any[]> {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/animals/');
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching animals:', error);
      return [];
    }
  }
  
  export async function fetchUsers(): Promise<any[]> {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/users/');
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching users:', error);
      return [];
    }
  }