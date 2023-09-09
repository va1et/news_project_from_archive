import { Stack } from '@mui/material';
import React, { useContext, useEffect, useState } from 'react';
import { MainContext } from '../../../context/MainContextProvider';
import EditNewsDrawer from '../../elements/drawer/EditNewsDrawer';
import NewsTable from '../../elements/tables/NewsTable';
import API from '../../../api';

export default function PanelLayout() {
  const { isEditDrawerOpen, setIsEditDrawerOpen } = useContext(MainContext);
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const getNews = async () => {
      const result = await API.get(`/news`, { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` } });
      setNews(result.data);
      setLoading(false);
    };
    getNews();
  }, []);

  return (
    loading ? <div>Loading...</div> :
      <>
        <Stack sx={{ gap: '32px', m: '64px auto', maxWidth: 'var(--max-width)' }}>
          <NewsTable rows={news} />
        </Stack>
        <EditNewsDrawer
          open={isEditDrawerOpen}
          onClose={() => setIsEditDrawerOpen(false)}
        />
      </>
  );
}
