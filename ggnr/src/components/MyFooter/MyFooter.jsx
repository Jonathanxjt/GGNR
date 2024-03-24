import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faFacebookF, faYoutube, faInstagram, faTwitter } from '@fortawesome/free-brands-svg-icons';
import './MyFooter.css';

function MyFooter() {
  return (
    <footer className="text-center text-lg-start custom-footer">
      <div className="container d-flex justify-content-center py-3">
      <ul>
      <li>
        <a href="#">
          <FontAwesomeIcon icon={faTwitter} className="icon" />
        </a>
      </li>
      <li>
        <a href="#">
          <FontAwesomeIcon icon={faInstagram} className="icon" />
        </a>
      </li>
      <li>
        <a href="#">
          <FontAwesomeIcon icon={faYoutube} className="icon" />
        </a>
      </li>
    </ul>
      </div>
      <div className="text-center text-white p-1" style={{ backgroundColor: '#003049' }}>
        © 2024 Copyright: GGNR.
        </div>
    </footer>
  );
}

export default MyFooter;
