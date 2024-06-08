"use client";
import React, { useEffect, useState } from 'react';
import { fetchAnimals, fetchUsers } from '@/app/lib/dataFetching';
import Map from "@/app/Components/map/map";
import Filters from "@/app/Components/Filter/map_filter"

const GISMap: React.FC = () => {

    return (
      <div>
        <h1>Welcome to GIS Page</h1>

        <div className="w-1/2">
            hellos <div>
            <Filters>
              <Map>

                
              </Map>
              </Filters>
              
              
              </div>
            
            
            
          </div>

      </div>
    );
  };
  
  export default GISMap;