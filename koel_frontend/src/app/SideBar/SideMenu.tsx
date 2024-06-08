import React, { useContext } from "react";
import { useState } from "react";
import Image from "next/image";
import HamburgerIcon from "@/app/Icons/burgermenu.svg";
import "./SideBar.css";
import "@/app/globals.css";
import DashboardIcon from "@/app/Icons/DashBoard-Home.svg";
import Upload from "@/app/Icons/upload-icon.svg"

import Link from "next/link";

const sidebarItems = [
  {
    name: "Home",
    href_var: "/",
    icon: (
      <Image
        src={DashboardIcon}
        className="sidebar_icon_sub"
        alt="Home Icon"
      />
    ),
  },
  {
    name: "Upload",
    href_var: "/UploadPage",
    icon: <Image src={Upload} className="sidebar_icon_sub" alt="UploadIcon" />,
  },

  
];

const SideMenu = () => {
  // const { isCollapsedSidebar, toggleSidebarCollapseHandler } = useContext(SidebarContext);

  const [isCollapsedSidebar, setIsCollapsedSidebar] = useState<boolean>(true);

  const toggleSidebarCollapseHandler = () => {
    setIsCollapsedSidebar((prev) => !prev);
  };

  return (
    <div className="sidebar_wrapper">
      <div className="sidebar" data-collapse={isCollapsedSidebar.toString()}>
        <div className="pl-1">
          <button onClick={toggleSidebarCollapseHandler}>
            <Image
              src={HamburgerIcon}
              className="sidebar_logo"
              alt="Hamburger Icon"
              width={50}
              height={50}
            />
          </button>

        </div>

        
        
        <ul className="sidebar_list">
          {sidebarItems.map(({ name, href_var, icon: icons }) => (
            <li className="sidebar_item" key={name}>
              <Link href={href_var} className="sidebar_link">
                <div className="sidebar_icon">{icons}</div>
                <span className="sidebar_name">{name}</span>
              </Link>
            </li>
          ))}
        </ul>
      </div>
      
      {/* <aside className="sidebar2" data-collapse={isCollapsedSidebar.toString()}>

      </aside> */}
  <aside className="sidebar2">

</aside>
    </div>



  );
};

export default SideMenu;
