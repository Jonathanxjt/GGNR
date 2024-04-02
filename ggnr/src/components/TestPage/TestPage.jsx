import React from "react";
import placeholder from "../../assets/placeholder.jpg";
import  CheckboxCustom  from "../CheckboxCustom/CheckboxCustom";
import { MyNavbar } from "../MyNavbar/MyNavbar";
import MyFooter from "../MyFooter/MyFooter";

const TestPage = () => {
  return (
    <div>
      <h1>Test Page</h1>
      <p>This is a test page for React.</p>
      <img src="https://i.ibb.co/VLB3xff/fn.png"></img>
      <div>
        <CheckboxCustom
        /> Free entry

      </div>
      <img src={placeholder}></img>
      <MyFooter />

    </div>
  );
};

export default TestPage;
