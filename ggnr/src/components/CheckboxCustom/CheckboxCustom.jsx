import React from "react";
import "./CheckboxCustom.css"; // Import the CSS file

const CheckboxCustom = ({ checked, onChange }) => {
	return (
		<div className="custom-checkbox-wrapper">
			<input type="checkbox" checked={checked} onChange={onChange} />
			<svg viewBox="0 0 21.36 21.36">
				<circle className="custom-background" cx="10.68" cy="10.68" r="10.68" />
				<circle className="custom-stroke" cx="10.68" cy="10.68" r="8.622" />
				<polyline
					className="custom-check"
					points="7.068 10.872 9.33 13.338 15.102 7.722"
				/>
			</svg>
		</div>
	);
};

export default CheckboxCustom;
