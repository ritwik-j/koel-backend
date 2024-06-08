import React, { useRef, useState, ReactNode } from "react";
import scss from "./Map_filter.module.scss";
import Image from "next/image";
import filterIcon from "@/app/Icons/filter-svgrepo-com.svg"
import layerIcon from "@/app/Icons/layer-svgrepo-com.svg"

interface Props {
    children:ReactNode | ReactNode[];

}

const Filter = ({children} : Props) => {
    return (
        <div>
            
            <div style={{ position: 'absolute', zIndex: 100, right:15 }}>
            
            <div style={{top: 40, right:15, padding:5 }}>            
                    <button style={{ backgroundColor: 'white', border: 'none', padding: 2, borderRadius: '5px'}}>
                        <Image
                            src={layerIcon}
                            className="filter_icon_sub"
                            alt="filter_icon_Icon"
                            style={{ width: '40px', height: '40px' }}
                        />
                    </button>

                </div>



                <div style={{bottom: 40, left:15, padding:5  }}>           
                    <button style={{ backgroundColor: 'white', border: 'none', padding: 2, borderRadius: '5px'}}>
                        <Image
                            src={filterIcon}
                            className="filter_icon_sub"
                            alt="filter_icon_Icon"
                            style={{ width: '40px', height: '40px' }}
                        />
                    </button>
                </div>

                
                
                


            
            </div>
            
            
            <div style={{ zIndex: 99 }}>{children}</div>
        
        
        
        </div>
        
    );
};

export default Filter;