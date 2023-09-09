import { Drawer } from '@mui/material';
import React from 'react';

export default function BaseDrawer({ children, open, onClose }) {
  return (
    <Drawer anchor='right' open={open} onClose={onClose}>
      {children}
    </Drawer>
  );
}
