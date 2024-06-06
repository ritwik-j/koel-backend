import { ReactNode } from "react";
// import Sidebar from "./SideBar";
import Header from "@/app/Components/Header";
import SideBar from "@/app/SideBar";

interface Props {
    children:ReactNode | ReactNode[];

}

export default function BaseLayout ({children} : Props)
{
    return(
        <div className="layout">
            <Header/>
            <SideBar/> 
            <div className="pt-20 pl-28">
                {children}
            </div>
            
        </div>
    );
}