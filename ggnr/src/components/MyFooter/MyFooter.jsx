import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faFacebookF, faYoutube, faInstagram, faTwitter } from '@fortawesome/free-brands-svg-icons';
import './MyFooter.css';

function MyFooter() {
  return (
    <footer className="text-center text-lg-start custom-footer">
      <div className="container d-flex justify-content-center py-3">
        <button type="button" className="btn btn-primary btn-lg btn-floating mx-2" style={{ backgroundColor: '#003049' }}>
          <FontAwesomeIcon icon={faFacebookF} />
        </button>
        <button type="button" className="btn btn-primary btn-lg btn-floating mx-2" style={{ backgroundColor: '#003049' }}>
          <FontAwesomeIcon icon={faYoutube} />
        </button>
        <button type="button" className="btn btn-primary btn-lg btn-floating mx-2" style={{ backgroundColor: '#003049' }}>
          <FontAwesomeIcon icon={faInstagram} />
        </button>
        <button type="button" className="btn btn-primary btn-lg btn-floating mx-2" style={{ backgroundColor: '#003049' }}>
          <FontAwesomeIcon icon={faTwitter} />
        </button>
      </div>
      <div className="text-center text-white p-1" style={{ backgroundColor: '#003049' }}>
        © 2024 Copyright: GGNR.
        </div>
    </footer>
  );
}

export default MyFooter;
