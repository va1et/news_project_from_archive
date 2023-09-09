import React from 'react';
import AppLayout from '../../components/layouts/AppLayout';
import NewsLayout from '../../components/layouts/NewsLayout';

export default function Home() {
  return (
    <AppLayout>
      <NewsLayout />
    </AppLayout>
  );
}
