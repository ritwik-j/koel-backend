// Types that would be returned from database

export interface Animal {
    id: number;
    species_name: string;
    description: string;
    habitat: string;
    size: string;
    extinction_status: string;
  }
  
  export interface User {
    id: number;
    username: string;
    email: string;
    level: number;
    identified_animals: Animal[];
    friends: User[];
  }