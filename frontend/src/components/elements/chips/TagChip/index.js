import { Chip } from '@mui/material';
import React from 'react';

export default function TagChip({ label }) {
  return (
    <Chip
      label={label}
      sx={{
        p: '4px 16px',
        color: '#fff',
        background: 'var(--color-primary)',
        fontFamily: 'inherit',
        flexShrink: 0,
        fontWeight: 400,
        fontSize: '14px',
        lineHeight: '16px',

        '& span': {
          p: 0,
        },
      }}
    />
  );
}
