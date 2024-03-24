// ToastManager.js
import React, { useEffect } from 'react';
import { toast, ToastContainer, Flip } from 'react-toastify';

const ToastManager = () => {
  useEffect(() => {
    const message = localStorage.getItem('toastMessage');
    if (message) {
      toast.success(message, {
            position: "top-center",
            autoClose: 2000,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            progress: undefined,
            theme: "dark",
            transition: Flip,
      });
      localStorage.removeItem('toastMessage'); // Clear the message after showing it
    }
  }, []);

  return <ToastContainer />;
};

export default ToastManager;