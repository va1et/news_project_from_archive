import { Stack } from '@mui/system';
import React from 'react';
import NewsCard from '../../../elements/cards/NewsCard';

export default function NewsGroup({ news }) {
  return (
    <Stack
      sx={{
        gap: '32px',
      }}>
      {news.map(row => (
        <NewsCard key={row.guid} news={row} />
      ))}
    </Stack>
  );
}
